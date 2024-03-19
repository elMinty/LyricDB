import threading
from datetime import datetime

from src import LyricDB

data = "..\\..\\data\\unprocessed.csv"
index = "..\\..\\data\\inverted_index_final.csv"


if __name__ == "__main__":
    # Create a new LyricDB object
    lyric_db = LyricDB.LyricDB()

    # init
    lyric_db.init("localhost", 'DB')

    start = datetime.now()
    my_thread = threading.Thread(target=lyric_db.tracks_to_mongodb_bulk(data))
    my_thread.start()
    lyric_db.bulk_upsert_index(index)
    my_thread.join()

    print(datetime.now() - start)