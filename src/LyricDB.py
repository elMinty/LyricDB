import csv
import csv
import json
import threading
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
        init_albums_collection(self.db)
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
        start = datetime.now()
        # Determine number of lines in CSV to split work
        total_lines = sum(1 for _ in open(csv_file_path, 'r', encoding='utf-8')) - 1  # minus header line
        num_threads = 3  # Or any other number of threads you want to use
        lines_per_thread = total_lines // num_threads

        threads = []
        for i in range(num_threads):
            start_line = i * lines_per_thread
            end_line = (i + 1) * lines_per_thread if i != num_threads - 1 else total_lines

            thread = threading.Thread(target=self.process_csv_segment, args=(csv_file_path, start_line, end_line))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        print('details insert: ' + str(datetime.now() - start))

    def process_csv_segment(self, csv_file_path, start_line, end_line):
        tracks = []
        albums_operations = []

        with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for i, row in enumerate(reader):
                if i < start_line or i >= end_line:
                    continue

                album_cover = json.loads(row['album_cover'].replace("'", '"'))
                genres = row['genres'].split('|')
                track_link = json.loads(row['track_link'].replace("'", '"'))

                track_document = {
                    'song_id': row['song_id'],
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
                    # 'album_id': row['album_id'],
                    'album_name': row['album_name'],
                    'artist_name': row['artist_name'],
                    'release_date': self.parse_date(row['release_date']),
                    'album_cover': album_cover
                }

                # Prepare bulk operation for albums collection
                albums_operations.append(
                    UpdateOne({'album_id': row['album_id']}, {'$set': album_document}, upsert=True)
                )

        # Perform database operations
        if tracks:
            self.db.trackDetails.insert_many(tracks)
        if albums_operations:
            self.db.albums.bulk_write(albums_operations)


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
            entry = entry.rstrip(')')
            token = ''
            positions_str = ''
            try:
                token, positions_str = entry.split(', ', 1)
            except Exception:
                print(Exception)
                print(entry)


            # Convert the positions string to a list of integers
            positions = eval(positions_str)

            documents.append({
                "doc_id": token,
                "positions": positions,
                "frequency": len(positions)  # Assuming frequency is the count of positions
            })

        return documents


    def process_csv_segment_index(self, csv_file_path, start_line, end_line):
        operations = []

        with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            # Skip header if in the first chunk
            if start_line == 1:
                next(reader, None)

            for i, row in enumerate(reader, start=1):
                if i < start_line:
                    continue
                if i >= end_line:
                    break

                token, doc_pos = row
                docs = self.parse_token_string_with_quotes(doc_pos)

                operations.append(UpdateOne(
                    {"token": token},
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
                    upsert=True
                ))

        if operations:
            print(f'Updating Tokens in segment {start_line} to {end_line}....')
            self.db.index.bulk_write(operations)

    def bulk_upsert_index(self, csv_file_path):
        start_time = datetime.now()

        total_lines = sum(1 for _ in open(csv_file_path, 'r', encoding='utf-8')) - 1  # Subtract header line
        num_threads = 6  # Adjust based on your needs
        lines_per_thread = total_lines // num_threads

        threads = []
        for i in range(num_threads):
            start_line = i * lines_per_thread + 1  # +1 to account for header in the first chunk
            end_line = (
                                   i + 1) * lines_per_thread + 1 if i != num_threads - 1 else total_lines + 1  # +1 as end line is exclusive

            thread = threading.Thread(target=self.process_csv_segment_index, args=(csv_file_path, start_line, end_line))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        end_time = datetime.now()
        print(f"Index Insert in: {end_time - start_time}")

        print("Updating Frequencies...")
        self.update_frequencies()

        print("Sorting...")
        self.sort_index()


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