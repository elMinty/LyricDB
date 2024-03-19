import json
import os

from pymongo import MongoClient
from LyricDB import LyricDB

gcloud = f"mongodb://admin:3Jg92Z%C2%A3%7CHX8ow%24VT%3Dk%5D'%7BVS@35.214.80.148:27017/?authSource=admin"

if __name__ == '__main__':

    lyricDB = LyricDB()
    lyricDB.connect('','DB')

    # Read json from file and put it in the database
    lyricDB.tracks_to_mongodb_bulk("data\\unprocessed.csv")
    lyricDB.bulk_upsert_index("data\\inverted_index_final.csv")