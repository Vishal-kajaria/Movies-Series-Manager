import sqlite3


# Setting up a new connection
def create_connection(db_file):
    return sqlite3.connect(db_file)


# Creating tables for movies and series with additional fields
def create_table(conn):
    with conn:
        # Movie table with additional fields
        conn.execute('''
            CREATE TABLE IF NOT EXISTS movie(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            release_year INT NOT NULL,
            genre TEXT,
            director TEXT,
            cast TEXT
            );
        ''')

        # Series table with additional fields, including 'seasons'
        conn.execute('''
            CREATE TABLE IF NOT EXISTS series(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            release_year INT NOT NULL,
            genre TEXT,
            director TEXT,
            cast TEXT,
            seasons INT
            );
        ''')


# Adding a movie or series to the database with additional fields
def add_to_database(conn, name, release_year, genre, director, cast, table, seasons=None):
    with conn:
        if table == 'movie':
            conn.execute("INSERT INTO movie (name, release_year, genre, director, cast) VALUES (?, ?, ?, ?, ?)",
                         (name, release_year, genre, director, cast))
        elif table == 'series':
            conn.execute("INSERT INTO series (name, release_year, genre, director, cast, seasons) "
                         "VALUES (?, ?, ?, ?, ?, ?)",
                         (name, release_year, genre, director, cast, seasons))


# Retrieving a movie or series from the database
def get_from_database(conn, name, table):
    cursor = conn.execute(f"SELECT * FROM {table} WHERE name = ?", (name,))
    return cursor.fetchone()


# Displaying all movies or series
def display_all(conn, table):
    cursor = conn.execute(f"SELECT * FROM {table}")
    return cursor.fetchall()


# Updating a movie or series in the database
def update_record(conn, table, column, new_value, name):
    try:
        with conn:
            cursor = conn.execute(f"SELECT * FROM {table} WHERE name = ?", (name,))
            if cursor.fetchone():  # Check if the record exists
                conn.execute(f"UPDATE {table} SET {column} = ? WHERE name = ?", (new_value, name))
                print(f"{table.capitalize()} '{name}' updated successfully.")
            else:
                print(f"{table.capitalize()} '{name}' not found.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")


# Deleting a movie or series from the database
def delete_from_database(conn, name, table):
    try:
        with conn:
            cursor = conn.execute(f"SELECT * FROM {table} WHERE name = ?", (name,))
            if cursor.fetchone():  # Check if the record exists
                conn.execute(f"DELETE FROM {table} WHERE name = ?", (name,))
                print(f"{table.capitalize()} '{name}' deleted successfully.")
            else:
                print(f"{table.capitalize()} '{name}' not found.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")


def main():
    db_file = 'media_manager.db'
    conn = create_connection(db_file)
    create_table(conn)

    # User choice at the initial stage is 0.
    choice = 0
    print("*** Welcome to movie/series manager ***\n")

    # While choice is not 6 (i.e., quitting), it will execute.
    while choice != 6:
        print("1. I want to add a movie or series.")
        print("2. I want to get a quick review of a movie/series.")
        print("3. I want to display all movie/series.")
        print("4. I want to update a movie or series.")
        print("5. I want to delete a movie or series.")
        print("6. QUIT\n")

        choice = int(input("What do you want? "))

        # If user inputs 1:
        if choice == 1:
            print("\n1. You are adding a movie/series...")
            ask = input("\tDo you want to add a movie or series? ")

            if ask == "movie":
                movie = input("\tEnter name of the movie >>> ")
                release_year = int(input("\tEnter its release year >>> "))
                genre = input("\tEnter the genre >>> ")
                director = input("\tEnter the director >>> ")
                cast = input("\tEnter the cast >>> ")
                add_to_database(conn, movie, release_year, genre, director, cast, 'movie')

            elif ask == "series":
                series = input("\tEnter name of the series >>> ")
                release_year = int(input("\tEnter its release year >>> "))
                genre = input("\tEnter the genre >>> ")
                director = input("\tEnter the director >>> ")
                cast = input("\tEnter the cast >>> ")
                seasons = int(input("\tEnter the number of seasons >>> "))
                add_to_database(conn, series, release_year, genre, director, cast, 'series', seasons)

        # If user inputs 2:
        elif choice == 2:
            print("\n2. You want to get a quick review of a movie/series.")
            ask = input("Is it a movie or series? ")

            if ask == "movie":
                movie1 = input("\tEnter the name of the movie >>> \n")
                print("Looking for that movie...")
                movie = get_from_database(conn, movie1, 'movie')
                if movie:
                    print(movie)
                else:
                    print("Movie not found.")

            elif ask == "series":
                series1 = input("\tEnter the name of the series >>> ")
                print("Looking for that series...")
                series = get_from_database(conn, series1, 'series')
                if series:
                    print(series)
                else:
                    print("Series not found.")

        # If user inputs 3:
        elif choice == 3:
            print("\n3. Displaying all movies/series...")
            asking = input("Do you want to display movies or series? ")

            if asking == "movie":
                movies = display_all(conn, 'movie')
                for movie in movies:
                    print(movie)

            elif asking == "series":
                series_list = display_all(conn, 'series')
                for series in series_list:
                    print(series)

        # If user inputs 4:
        elif choice == 4:
            print("\n4. You want to update a movie/series...")
            ask = input("\tIs it a movie or series? ")

            if ask == "movie":
                movie = input("\tEnter the name of the movie to update >>> ")
                column = input("\tEnter the column to update (name, release_year, genre, director, cast) >>> ")
                new_value = input(f"\tEnter the new value for {column} >>> ")
                update_record(conn, 'movie', column, new_value, movie)

            elif ask == "series":
                series = input("\tEnter the name of the series to update >>> ")
                column = input("\tEnter the column to update (name, release_year, genre, director, cast, seasons) >>> ")
                new_value = input(f"\tEnter the new value for {column} >>> ")
                update_record(conn, 'series', column, new_value, series)

            # If user inputs 5:
        elif choice == 5:
            print("\n5. You want to delete a movie/series...")
            ask = input("\tIs it a movie or series? ")

            if ask == "movie":
                movie = input("\tEnter the name of the movie to delete >>> ")
                delete_from_database(conn, movie, 'movie')

            elif ask == "series":
                series = input("\tEnter the name of the series to delete >>> ")
                delete_from_database(conn, series, 'series')

                # If user inputs 6:
        elif choice == 6:
            print("\n6. Quitting out of the program... ")


print("Program Terminated!")


if __name__ == "__main__":
    main()