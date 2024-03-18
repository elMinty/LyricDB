import csv
import csv
import json
from datetime import datetime

from dateutil import parser
from pymongo import MongoClient, UpdateOne

from LyricDBinit import *
from Token import Token

csv.field_size_limit(2**30)

class LyricDB():

    def __init__(self):
        """
        Initialize the database connection details.

        :param db_uri: MongoDB connection URI string (optional).
        :param db_name: Name of the database to use (optional).
        """

        self.connected = False
        self.client = None
        self.db = None
        self.db_uri = None
        self.db_name = None

    def __str__(self):
        # Return a string representation of the database connection details and all the collections.

        if self.client:
            collection_names = self.db.list_collection_names()
            return f"Database: {self.db_name} at {self.db_uri}\nCollections: {collection_names}"

    def init(self, db_uri, db_name):
        """
        Calls initialization methods from LyricDBinit to set up the database.
        """
        self.connect(db_uri,db_name)
        init_track_details_collection(self.db)
        init_lyrics_collection(self.db)
        init_albums_collection(self.db)
        init_update_track_collection(self.db)
        init_index_collection(self.db)


    def connect(self, db_uri=None, db_name=None):
        """
        Establish a connection to the MongoDB database.

        :param db_uri: MongoDB connection URI string (optional if provided during class initialization).
        :param db_name: Name of the database to use (optional if provided during class initialization).
        """
        # Allow overriding or setting db_uri and db_name during connection
        if db_uri and db_name:
            self.db_uri = db_uri
            self.db_name = db_name
            self.client = MongoClient(self.db_uri)
            self.db = self.client[self.db_name]
            print(f"Connected to database: {self.db_name} at {self.db_uri}")
            self.connected = True

        if not self.db_uri or not self.db_name:
            raise ValueError(
                "Database URI and name must be provided either during initialization or when calling connect.")

    def tracks_to_mongodb_bulk(self, csv_file_path):
        track_details_operations = []
        albums_operations = []

        with open(csv_file_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            tracks = []
            albums = []
            for row in reader:
                album_cover = json.loads(row['album_cover'].replace("'", '"'))
                genres = row['genres'].split('|')
                track_link = json.loads(row['track_link'].replace("'", '"'))

                track_document = {
                    'added_on': self.parse_date(row['added_on']),
                    'album_id': row['album_id'],
                    'album_cover': album_cover,
                    'album_name': row['album_name'],
                    'artist_name': row['artist_name'],
                    'release_date': self.parse_date(row['release_date']),
                    'track_id': row['track_id'],
                    'track_name': row['track_name'],
                    'track_link': track_link,
                    'duration_ms': int(row['duration_ms']),
                    'explicit': row['explicit'] == 'True',
                    'danceability': float(row['danceability']),
                    'energy': float(row['energy']),
                    'genres': genres,
                    'lyrics': row['lyrics']
                }

                tracks.append(track_document)

                # # Prepare bulk operation for trackDetails collection
                # track_details_operations.append(
                #     UpdateOne({'song_id': row['song_id']}, {'$set': track_document}, upsert=True)
                # )

                album_document = {
                    'album_name': row['album_name'],
                    'artist_name': row['artist_name'],
                    'release_date': self.parse_date(row['release_date']),
                    'album_cover': album_cover
                }

                albums.append(album_document)

                # # Prepare bulk operation for albums collection
                # albums_operations.append(
                #     UpdateOne({'album_id': row['album_id']}, {'$set': album_document}, upsert=True)
                # )
        self.db.trackDetails.insertMany(tracks)
        self.db.albums.insertMany(albums)

        # if track_details_operations:
        #     # self.db.trackDetails.bulk_write(track_details_operations)
        #
        # if albums_operations:
        #     # self.db.albums.bulk_write(albums_operations)

    def parse_date(self, date_str):
        try:
            # Use dateutil's parser to automatically detect the date format
            return parser.parse(date_str).strftime('%Y-%m-%d')
        except ValueError:
            # Handle the error if the date format is unrecognized
            raise ValueError(f"Could not parse date: {date_str}")

    def parse_token_string_with_quotes(self, token_string):
        # Split the string into token entries, removing the leading and trailing double quotes
        token_entries = token_string.strip('"').split('), (')

        documents = []

        for entry in token_entries:
            # Extracting token and positions by removing the surrounding parentheses and splitting by ', '
            # The token is expected to be within single quotes, so it's directly extracted
            entry = entry.rstrip(')')
            token, positions_str = entry.split(', ', 1)
            # print(token)
            # print(positions_str)


            # Convert the positions string to a list of integers
            positions = eval(positions_str)

            documents.append({
                "doc_id": token,
                "positions": positions,
                "frequency": len(positions)  # Assuming frequency is the count of positions
            })

        return documents

    def bulk_upsert_index(self, csv_file_path):
        start_time = datetime.now()

        operations = []

        with open(csv_file_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)

            # Skip the first row
            next(reader, None)  # This advances the reader to the next row, effectively skipping the first row
            token_list = []
            for row in reader:
                token, doc_pos = row
                token_list.append(token)

                # parse doc pos to {'doc':[pos]}
                docs = self.parse_token_string_with_quotes(doc_pos)
                #print(docs)

                # docID
                operations.append(UpdateOne(
                    {"token": token},  # Condition to find the document
                    {
                        "$setOnInsert": {
                            "doc_frequency": 1,
                            "total_frequency": 1
                        },
                        "$push": {
                            "documents": {
                                "$each": docs
                            }
                        }
                    },
                    upsert=True  # Perform an insert if a document matching the condition does not exist
                ))

                # operations.append(
                #     UpdateOne(
                #         {'token': token},
                #         [
                #             {'$set': {'token': {'$ifNull': ['$token', token]}}},
                #             {'$set': {'doc_pos': {'$concat': [{'$ifNull': ['$doc_pos', '']}, ',', doc_pos]}}}
                #         ],
                #         upsert=True
                #     )
                # )


        print('Updating Tokens....')
        self.db.index.bulk_write(operations)

        print('Updating Frequencies...')
        self.update_frequencies()

        print("Sorting...")
        self.sort_index()

        print(datetime.now() - start_time)

        return token_list

    # Do update for this
    # Update Token Frequency and total items
    # Do updated Token doc_pos and doc_frequency ->
    # Sort order of documents based off of Array

    # def update_index(self, token_list):


    def update_frequencies(self):

        #Run aggregate to find frequencies
        aggregation_results = self.db.index.aggregate([
            {"$unwind": "$documents"},
            {"$group": {
                "_id": "$token",
                "total_frequency": {"$sum": "$documents.frequency"},
                "doc_frequency": {"$sum": 1}
            }}
        ])

        # Update Operations
        update_operations = []
        for result in aggregation_results:
            update_operations.append(UpdateOne(
                {"token": result["_id"]},
                {"$set": {"total_frequency": result["total_frequency"], "doc_frequency": result["doc_frequency"]}}

            ))

        if update_operations:
            self.db.index.bulk_write(update_operations)

    def retrieve_sorted_documents(self):
        sorted_documents_per_token = self.db.index.aggregate([
            {"$unwind": "$documents"},
            {"$sort": {"documents.frequency": -1}},  # Sort documents by frequency in descending order
            {"$group": {
                "_id": "$token",
                "sorted_documents": {"$push": "$documents"}
            }}
        ])
        return sorted_documents_per_token

    def sort_index(self):
        sorted_documents_per_token = self.retrieve_sorted_documents()

        update_operations = []
        for token_info in sorted_documents_per_token:
            update_operations.append(UpdateOne(
                {"token": token_info["_id"]},
                {"$set": {"documents": token_info["sorted_documents"]}}
            ))

        if update_operations:
            self.db.index.bulk_write(update_operations)


    # for ranking
    def get_token(self, token_id):
        # Query the collection for the document with the specified token ID
        document = self.db.index.find_one({"token": token_id})

        # If the document is found, create and return a Token object
        if document:
            return Token(
                id=document.get("token"),  # Assuming the 'token' field is used as an ID
                doc_frequency=document.get("doc_frequency"),
                total_frequency=document.get("total_frequency"),
                docs=document.get("documents")
            )
        else:
            return None


    # For search page
    def get_song_details(self, song_id):

        details = self.db.trackDetails.find_one({"song_id": song_id})

        if details:
            return  details
        else:
            return None