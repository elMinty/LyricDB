from pymongo import ASCENDING
from Validators import *



def init_track_details_collection(db):
    """
    Initialize the Song_Details collection with an index on 'track_id'.

    Attributes: track_id, album_id, track_name, artist_name, track_link, added_on, release_date, duration_ms, explicit, danceability, energy, genres

    """
    collection_name = 'trackDetails'
    if collection_name not in db.list_collection_names():
        collection = db.create_collection(collection_name, validator=trackDetailsValidator,
                                               validationLevel='strict', validationAction='error')

        collection.create_index([("track_id", ASCENDING)], unique=True)

        print(f"Collection '{collection_name}' initialized with an index on 'track_id'.")
    else:
        print(f"Collection '{collection_name}' already exists.")

def init_lyrics_collection(db):
    """
    Initialize the Lyrics collection with an index on 'track_id'.

    Attributes: track_id, lyrics

    """
    collection_name = 'lyrics'
    if collection_name not in db.list_collection_names():
        collection = db.create_collection(collection_name, validator=tokenIndex,
                                               validationLevel='strict', validationAction='error')

        collection.create_index([("token", ASCENDING)], unique=True)

        print(f"Collection '{collection_name}' initialized with an index on 'token'.")
    else:
        print(f"Collection '{collection_name}' already exists.")

def init_albums_collection(db):
    """
    Initialize the Albums collection with an index on 'album_id'.

    Attributes: album_id, album_name, artist_name, release_date

    """
    collection_name = 'albums'
    if collection_name not in db.list_collection_names():
        collection = db.create_collection(collection_name, validator=album_validator,
                                               validationLevel='strict', validationAction='error')

        collection.create_index([("album_id", ASCENDING)], unique=True)

        print(f"Collection '{collection_name}' initialized with an index on 'album_id'.")
    else:
        print(f"Collection '{collection_name}' already exists.")

def init_update_track_collection(db):
    """
    Initialize the Update_Track collection with an index on 'track_id'.

    Attributes: added_on, album_id, album_cover, album_name, artist_name, release_date, track_id, track_name, track_link, duration_ms, explicit, danceability, energy, genres, lyrics

    """
    collection_name = 'updateTrack'
    if collection_name not in db.list_collection_names():

        collection = db.create_collection(collection_name, validator=updateTracksValidator, validationLevel='strict', validationAction='error')

        collection.create_index([("song_id", ASCENDING)], unique=True)

        print(f"Collection '{collection_name}' initialized with an index on 'track_id'.")
    else:
        print(f"Collection '{collection_name}' already exists.")

def init_lyric_index_collection(db):
    """
    Initialize the Lyric_Index collection with an index on 'word'.

    Attributes: word, tracks : (track_id: [positions])

    """
    collection_name = 'lyricIndex'
    if collection_name not in db.list_collection_names():
        collection = db.create_collection(collection_name, lyric_indexer_validator,
                                               validationLevel='strict', validationAction='error')

        collection.create_index([("token", ASCENDING)], unique=True)

        print(f"Collection '{collection_name}' initialized with an index on 'word'.")
    else:
        print(f"Collection '{collection_name}' already exists.")


def init_index_collection(db):
    """
    Initialize the Lyrics collection with an index on 'track_id'.

    Attributes: track_id, lyrics

    """
    collection_name = 'index'
    if collection_name not in db.list_collection_names():
        collection = db.create_collection(collection_name, validator=token_doc_stats,
                                               validationLevel='strict', validationAction='error')

        collection.create_index([("token", ASCENDING)], unique=True)

        print(f"Collection '{collection_name}' initialized with an index on 'token'.")
    else:
        print(f"Collection '{collection_name}' already exists.")


