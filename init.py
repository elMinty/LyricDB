import LyricDB

if __name__ == '__main__':

    try:
        # Create a new LyricDB object
        lyric_db = LyricDB.LyricDB()

        #init
        lyric_db.init("mongodb://admin:3Jg92Z%C2%A3%7CHX8ow%24VT%3Dk%5D'%7BVS@35.214.80.148:27017/?authSource=admin",'DB')

        # Print the database connection details
        print(lyric_db)
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Exiting...")