import csv, sqlite3, sys

def main():
    """
    Main function
    :return: No return value
    :rtype: None
    """
    clear_and_load("cs50p/9.final/holy-grail-api/holy_scripts.csv", "cs50p/9.final/holy-grail-api/holy_scripts.db")

def clear_and_load(csvfile: str, dbname: str) -> None:
    """
    Asks user if they want to delete everything from the db - including top quotes table and basic scripts table.
    If y (yes) - delete all from tables scripts, tops and load into dbname.db database from csvfile.csv
    Csv file assumes to have [movie,scene_number,scene_name,type,character,text] headers
    If n (no) - return None
    :param csvfile: A string to csvfile to load into database
    :param dbname: A string of database where to load data from the csv
    :return: None
    :rtype: None
    """
    deletion = input("Do you want to delete all data (including top lists) from the database?[y/n] ").lower().strip()
    if deletion != "y":
        return None
    try:
        with open(csvfile) as f:
            # connect to the database
            database = sqlite3.connect(dbname, check_same_thread=False)
            cursordb = database.cursor()

            # empty the database before deletion
            cursordb.execute("""DELETE FROM scripts""")
            database.commit()

            cursordb.execute("""DELETE FROM tops""")
            database.commit()

            csvreader = csv.reader(f)
            next(csvreader)
            for row in csvreader:
                # insert row in scripts
                cursordb.execute("""
                    INSERT INTO scripts
                        (movie,
                        scene_number,
                        scene_name,
                        type,
                        character,
                        text)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,(row[0],row[1],row[2],row[3],row[4],row[5],))

        database.commit()
        database.close()

        print("Load completed")
    except:
        sys.exit("Error during data load into db")

    return None

if __name__ == "__main__":
    main()