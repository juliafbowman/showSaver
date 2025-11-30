import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
from pathlib import Path
import json
import datetime
from decimal import Decimal

# load dotenv for loading environment variables

env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)

print(f"*****Loading file from : {env_path}")
print(f"***** .env file exists: {env_path.exists()}")
print(f"*****DB_PASSWORD loaded:", "YES" if os.getenv('DB_PASSWORD') else "NO")

# Helper function for JSON Serialization
def json_serial(obj):
    # Serialize datetime and Decimal objects for Json
    
    if isinstance(obj,datetime.datetime):
        return obj.isoformat()
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f"Object of type {object.__class__.__name__} is not JSON serialization")

# this is used to get database from mysql connection
def get_db():
    # created tow ork with environment files, heres what is going to occur.
    # everything will default to the second parameter, so if you do not have a DB_HOST in your environment file.
    # then the default will become 'localhost'. The only thing that does not default is the password.
    
    try:
        
        return mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME', 'tvmate')
        )
    
    except Error as e:
        if "Unknown database" in str(e):
            # try the same connection but without specifying the database.
            print("Database not found, running schema setup...")
            conn = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD')
            )
            
            
            create_database_and_tables(conn)
            
            # Try to connect again
            
            conn.close()
            
            return mysql.connector.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                user=os.getenv('DB_USER', 'root'),
                password=os.getenv('DB_PASSWORD'),
                database=os.getenv('DB_NAME', 'tvmate')
            )
        else:
            print(f"Database connection error: {e}")
            return None


# automatically create database and tables for first time setup
def create_database_and_tables(connection):
    try:
        if connection:
            
            cursor = connection.cursor()
            
            # read schema file
            schema_path = Path(__file__).parent.parent / 'database' / '01_schema.sql'
            
            print(f"LOG: Reading Schema file at {schema_path}...")
            
            with open(schema_path, 'r') as file:
                schema_sql = file.read()
            
            print("LOG: Schema successfully read.")
            
            for statement in schema_sql.split(';'):
                if statement.strip():
                    cursor.execute(statement)
                
            
            connection.commit()
            
            print("LOG : Schema executed successfully.")
    except Error as e:
        print("ERROR: {e}")
    
    finally:
        cursor.close()
            
# Use this class to get access to database
    
class DAO:
    # use this to erase all data for your machine
    def erase_all_titles(self):
        connection = get_db()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("DELETE FROM Title")
                connection.commit()
                print("All titles erased...")
                return True
            except Error as e:
                print(f"ERROR: {e}")
                return False
            finally:
                cursor.close()
                connection.close()
        return False
        
    # example function to show how we can use this to return queries
    def get_all_titles(self):
        connection = get_db()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                cursor.execute("SELECT * FROM Title")
                titles = cursor.fetchall()
                return titles
            except Error as e:
                print(f"ERROR: {e}")
            finally:
                cursor.close()
                connection.close()
        return []
    
    #example function to add titles
    def add_titles(self, title_id, title_name=None, content_type=None, release_year=None, total_runtime=None, plot_summary=None, tmdb_avg_rating=None):
        connection = get_db()
        if connection:
            try:
                cursor = connection.cursor()
                query = """
                INSERT INTO Title(
                    title_id,
                    title_name,
                    content_type,
                    release_year,
                    total_runtime,
                    plot_summary,
                    tmdb_avg_rating
                )
                VALUES(%s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    title_name = COALESCE(VALUES(title_name)),
                    content_type = COALESCE(VALUES(content_type)),
                    release_year = COALESCE(VALUES(release_year)),
                    total_runtime = COALESCE(VALUES(total_runtime)),
                    plot_summary = COALESCE(VALUES(plot_summary)),
                    tmdb_avg_rating = COALESCE(VALUES(tmdb_avg_rating))
                """
                
                values = (title_id, title_name, content_type, release_year, total_runtime, plot_summary, tmdb_avg_rating)
                
                cursor.execute(query, values)
                connection.commit()
                return cursor.lastrowid
            except Error as e:
                print(f"ERROR: {e}")
                return None
            finally:
                cursor.close()
                connection.close()
            return None
        
    # episode
    def add_episodes(self, seasonepisode_id, title_id, episode_name=None, 
                   airdate=None, synopsis=None, runtime=None):
        """Add or update an episode"""
        connection = get_db()
        if connection:
            try:
                cursor = connection.cursor()
                query = """
                    INSERT INTO Episodes_Seasons (
                        seasonepisode_id, 
                        title_id, 
                        episode_name, 
                        airdate, 
                        synopsis, 
                        runtime
                    )
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                        episode_name = COALESCE(VALUES(episode_name)),
                        airdate = COALESCE(VALUES(airdate)),
                        synopsis = COALESCE(VALUES(synopsis)),
                        runtime = COALESCE(VALUES(runtime))
                """

                value = (seasonepisode_id, title_id, episode_name, 
                        airdate, synopsis, runtime)
                cursor.execute(query, value)
                
                connection.commit()
                return cursor.lastrowid
            except Error as e:
                print(f"ERROR: {e}")
                return None
            finally:
                cursor.close()
                connection.close()
            return None
    
    # rating
    def add_rating(self, rating, review_text, title_id):
        connection = get_db()
        if connection:
            try:
                date_posted = datetime.datetime.now()
                cursor = connection.cursor()
                query = """
                INSERT INTO Rating(
                    rating,
                    date_posted,
                    review_text,
                    title_id
                )
                VALUES(%s, %s, %s, %s)
                """
                values = (rating, date_posted, review_text, title_id)
                cursor.execute(query, values)
                connection.commit()
                print(f"Rating: {rating} successfully added for title ID: {title_id}")
                
                return cursor.lastrowid
            except Error as e:
                print(f"ERROR: {e}")
            
            finally:
                cursor.close()
                connection.close()
    
    def delete_rating(self, rating_id = None, title_id = None):
        connection = get_db()
        if connection:
            try:
                cursor = connection.cursor()
                
                # prioritize deleting by rating_id, fallback to title_id if not possible
                if rating_id:
                    print(f"***** Deleting Rating by Rating ID: {rating_id}")
                    
                    cursor.execute(f"DELETE FROM Rating WHERE rating_id = {rating_id}")
                
                elif title_id:
                    print(f"***** Deleting Rating by Title ID: {title_id}")
                    
                    cursor.execute(f"DELETE FROM Rating WHERE title_id = {title_id}")
                
                else:
                    print("****** Error: No ID provided by deletion")
                    return False
                
                connection.commit()
                
                # check if any row was actually deleted
                if cursor.rowcount > 0:
                    print("****** Rating deleted successfully")
                    return True
                else:
                    print("****** No rating found to delete")
                    return False
                
            except Error as e:
                print(f"ERROR: {e}")
                return False
            finally:
                cursor.close()
                connection.close()
            return False
    # genre
    def add_genre(self, genre_id, genre_name=None):
        connection = get_db()
        if connection:
            try:
                cursor = connection.cursor()
                query = """
                INSERT INTO Genre(
                    genre_id,
                    genre_name
                )
                VALUES(%s, %s)
                ON DUPLICATE KEY UPDATE
                    genre_name = COALESCE(VALUES(genre_name))
                """
                
                values = (genre_id, genre_name)
                
                cursor.execute(query, values)
                connection.commit()
                return cursor.lastrowid
            except Error as e:
                print(f"ERROR: {e}")
                return None
            finally:
                cursor.close()
            return None
             
    def link_title_genre(self, title_id, genre_id):
        connection = get_db()
        if connection:
            try:
                cursor = connection.cursor()
                query = """
                INSERT INTO Title_Genre(
                    title_id,
                    genre_id
                )
                VALUES(%s, %s)
                """
                
                values = (title_id, genre_id)
                
                cursor.execute(query, values)
                connection.commit()
                return cursor.lastrowid
            except Error as e:
                print(f"ERROR: {e}")
                return None
            finally:
                cursor.close()
            return None
    
    # function to return all logs -> meant to be used eventually for frontend
    def get_all_logs(self):
        connection = get_db()
        if connection:
            try:
                print("*****Attempting to connect cursor...")
                cursor = connection.cursor(dictionary=True)
                print("*****Cursor connected successfully.")
                query = '''
                SELECT
                t.title_id, 
                t.title_name, 
                t.release_year, 
                t.content_type, 
                t.total_runtime as display_duration,
                t.tmdb_avg_rating,
                r.rating as user_rating,
                r.review_text, 
                r.date_posted,
                
                -- aggregate multiple genres into one string
                GROUP_CONCAT(g.genre_name SEPARATOR ', ') as genre_string
                
                FROM Title t
                
                -- JOINS
                LEFT JOIN Title_Genre tg ON t.title_id = tg.title_id
                LEFT JOIN Genre g ON tg.genre_id = g.genre_id
                LEFT JOIN Rating r ON t.title_id = r.title_id
                GROUP BY t.title_id, t.title_name, t.release_year, t.content_type, t.total_runtime, t.tmdb_avg_rating, r.rating, r.review_text, r.date_posted
                '''
                
                print("*****executing query...")
                cursor.execute(query)
                print("*****query executed successfully.")
                logs = cursor.fetchall()
                
                # convert comara seperated string into a python list
                for log in logs:
                    if log['genre_string']:
                        log['genres'] = log['genre_string'].split(', ')
                    else:
                        log['genres'] = []
                    
                    # remove temp string field to keep JSON clean
                    del log['genre_string']
                
                return logs
            except Error as e:
                print(f"ERROR: SQL or Connection failed: {Error}")
                return []
            finally:
                print("*****closing cursor and connection...")
                cursor.close()
                if connection:
                    connection.close()
                
                print("*****connection and cursor closed...")



    def get_sorted_logs(self, sort, order):
        connection = get_db()

        translate_sort = {
            "title": "t.title_name",
            "release": "t.release_year",
            "rating": "r.rating",
            "duration": "t.total_runtime",
        }

        sort = translate_sort.get(sort, "t.title_name") # defaults to sorting by title
        
        if order == "desc" or order =="DESC":
            order = "DESC"
        else:
            order = "ASC"

        if connection:
            try:
                cursor = connection.cursor(dictionary=True)

                query = f'''
                SELECT
                t.title_id, 
                t.title_name, 
                t.release_year, 
                t.content_type, 
                t.total_runtime as display_duration,
                t.tmdb_avg_rating,
                r.rating as user_rating,
                r.review_text,
                r.date_posted,
                
                -- aggregate multiple genres into one string
                GROUP_CONCAT(g.genre_name SEPARATOR ', ') as genre_string
                
                FROM Title t
                
                -- JOINS
                LEFT JOIN Title_Genre tg ON t.title_id = tg.title_id
                LEFT JOIN Genre g ON tg.genre_id = g.genre_id
                LEFT JOIN Rating r ON t.title_id = r.title_id
                GROUP BY t.title_id, t.title_name, t.release_year, t.content_type, t.total_runtime, t.tmdb_avg_rating, r.rating, r.review_text, r.date_posted
                ORDER BY {sort} {order}
                '''

                cursor.execute(query)
                logs = cursor.fetchall()

                # convert comara seperated string into a python list
                for log in logs:
                    if log['genre_string']:
                        log['genres'] = log['genre_string'].split(', ')
                    else:
                        log['genres'] = []
                    
                    # remove temp string field to keep JSON clean
                    del log['genre_string']
                
                return logs
            except Error as e:
                print(f"ERROR: SQL or Connection failed: {Error}")
                return []
            finally:
                print("*****closing cursor and connection...")
                cursor.close()
                if connection:
                    connection.close()
                
                print("*****connection and cursor closed...")



    # function to delete all tables in schema based on linkage
    def delete_title_data(self,title_id):
        connection = get_db()
        if connection:
            try:
                cursor = connection.cursor()

                # Delete dependent data first (Rating)
                
                cursor.execute("DELETE FROM Rating WHERE title_id = %s", (title_id,))
                cursor.execute("DELETE FROM Title_Genre WHERE title_id = %s",(title_id,))
                cursor.execute("DELETE FROM Episodes_Seasons WHERE title_id = %s",(title_id,))
                cursor.execute("DELETE FROM Title WHERE title_id = %s",(title_id,))
                
                connection.commit()
                print(f"Title ID {title_id} and all related data successfully deleted.")
                return True
            
            except Error as e:
                connection.rollback()
                print(f"ERROR deleting title data: {e}")
                return False
            finally:
                cursor.close()
                if connection:
                    connection.close()
        return False
    
    # Clears all data from tables to keep them empty
    def delete_all_data(self):
        connection = get_db()
        if connection:
            try:
                cursor = connection.cursor()
                # Disable foreign key checks to allow truncation regardless of linkage
                cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
                
                # list tables to truncate
                tables = [
                    'Title_Genre',
                    'Episodes_Seasons',
                    'Rating',
                    'Genre',
                    'Title'
                ]
                
                print("***** Starting database cleanup...")
                
                for table in tables:
                    cursor.execute(f"TRUNCATE TABLE {table}")
                    print(f"LOG: Table {table} executed")
                    
                # re-enable key checks
            except Error as e:
                print(f"******ERROR: Failed to delete all data: {e}")
                try:
                    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
                except:
                    pass
                return False

            finally:
                cursor.close()
                connection.close()
                
    """
    Create a summarized statistics based on what is in the database
    Average rating
    Most watched genre
    Percentage of how much tv/show has been watched
    Total watchtime of movie/shows
    """
    
    def get_statistics(self):
        connection = get_db()
        if connection:
            try:
                cursor = connection.cursor(dictionary = True)
                stats = {
                    "total_titles" : 0,
                    "total_watchtime_minutes" : 0,
                    "total_watchtime_hours" : 0,
                    "average_rating" : 0.0,
                    "most_watched_genre" : "N/A",
                    "movie_percentage" : 0,
                    "tv_percentage" : 0
                }
                
                # General stats (counts and runtimes)
                
                query_general = """
                SELECT
                    COUNT(*) as total_count,
                    COALESCE(SUM(total_runtime), 0) as total_minutes,
                    SUM(CASE WHEN content_type ='movie' THEN 1 ELSE 0 END) as movie_count,
                    SUM(CASE WHEN content_type = 'tv' THEN 1 ELSE 0 END) as tv_count
                FROM Title
                """
                cursor.execute(query_general)
                general_data = cursor.fetchone()
                
                if general_data and general_data['total_count'] > 0:
                    stats['total_titles'] = general_data['total_count']
                    stats['total_watchtime_minutes'] = general_data['total_minutes']
                    stats['total_watchtime_hours'] = general_data['total_minutes']/60
                    
                    # Calculate Percentages
                    stats["movie_percentage"] = round((general_data['movie_count'] / general_data['total_count']) * 100, 1)
                    stats["tv_percentage"] = round((general_data['tv_count'] / general_data['total_count']) * 100, 1)
                
                # Average Rating
                cursor.execute("SELECT AVG(rating) as avg_rating FROM Rating")
                rating_data = cursor.fetchone()
                if rating_data and rating_data['avg_rating']:
                    stats["average_rating"] = round(float(rating_data['avg_rating']), 1)
                
                # Most Watched Genre
                # title -> title_genre -> genre
                
                query_genre = """"
                SELECT g.genre_name, COUNT(tg.title_id) as count
                FROM Title_Genre tg
                JOIN Genre g ON tg.genre_id = g.genre_id
                GROUP BY g.genre_name
                ORDER BY count DESC
                LIMIT 1
                """
                
                cursor.execute(query_genre)
                genre_data = cursor.fetchone()
                if genre_data:
                    stats["most_watched_genre"] = genre_data['genre_name']
                    
                return stats
            
            except Error as e:
                print(f"ERROR : {e}")
            finally:
                cursor.close()
                connection.close()
        return None

# import mysql.connector
# from mysql.connector import Error
# import os
# from dotenv import load_dotenv
# from pathlib import Path
# import json
# import datetime
# from decimal import Decimal

# # load dotenv for loading environment variables

# env_path = Path(__file__).parent / '.env'
# load_dotenv(env_path)

# print(f"*****Loading file from : {env_path}")
# print(f"***** .env file exists: {env_path.exists()}")
# print(f"*****DB_PASSWORD loaded:", "YES" if os.getenv('DB_PASSWORD') else "NO")

# # Helper function for JSON Serialization
# def json_serial(obj):
#     # Serialize datetime and Decimal objects for Json
    
#     if isinstance(obj,datetime.datetime):
#         return obj.isoformat()
#     if isinstance(obj, datetime.date):
#         return obj.isoformat()
    
#     if isinstance(obj, Decimal):
#         return float(obj)
#     raise TypeError(f"Object of type {object.__class__.__name__} is not JSON serialization")

# # this is used to get database from mysql connection
# def get_db():
#     # created tow ork with environment files, heres what is going to occur.
#     # everything will default to the second parameter, so if you do not have a DB_HOST in your environment file.
#     # then the default will become 'localhost'. The only thing that does not default is the password.
    
#     try:
        
#         return mysql.connector.connect(
#         host=os.getenv('DB_HOST', 'localhost'),
#         user=os.getenv('DB_USER', 'root'),
#         password=os.getenv('DB_PASSWORD'),
#         database=os.getenv('DB_NAME', 'tvmate')
#         )
    
#     except Error as e:
#         if "Unknown database" in str(e):
#             # try the same connection but without specifying the database.
#             print("Database not found, running schema setup...")
#             conn = mysql.connector.connect(
#             host=os.getenv('DB_HOST', 'localhost'),
#             user=os.getenv('DB_USER', 'root'),
#             password=os.getenv('DB_PASSWORD')
#             )
            
            
#             create_database_and_tables(conn)
            
#             # Try to connect again
            
#             conn.close()
            
#             return mysql.connector.connect(
#                 host=os.getenv('DB_HOST', 'localhost'),
#                 user=os.getenv('DB_USER', 'root'),
#                 password=os.getenv('DB_PASSWORD'),
#                 database=os.getenv('DB_NAME', 'tvmate')
#             )
#         else:
#             print(f"Database connection error: {e}")
#             return None


# # automatically create database and tables for first time setup
# def create_database_and_tables(connection):
#     try:
#         if connection:
            
#             cursor = connection.cursor()
            
#             # read schema file
#             schema_path = Path(__file__).parent.parent / 'database' / '01_schema.sql'
            
#             print(f"LOG: Reading Schema file at {schema_path}...")
            
#             with open(schema_path, 'r') as file:
#                 schema_sql = file.read()
            
#             print("LOG: Schema successfully read.")
            
#             for statement in schema_sql.split(';'):
#                 if statement.strip():
#                     cursor.execute(statement)
                
            
#             connection.commit()
            
#             print("LOG : Schema executed successfully.")
#     except Error as e:
#         print("ERROR: {e}")
    
#     finally:
#         cursor.close()
            
# # Use this class to get access to database
    
# class DAO:
#     # use this to erase all data for your machine
#     def erase_all_titles(self):
#         connection = get_db()
#         if connection:
#             try:
#                 cursor = connection.cursor()
#                 cursor.execute("DELETE FROM Title")
#                 connection.commit()
#                 print("All titles erased...")
#                 return True
#             except Error as e:
#                 print(f"ERROR: {e}")
#                 return False
#             finally:
#                 cursor.close()
#                 connection.close()
#         return False
        
#     # example function to show how we can use this to return queries
#     def get_all_titles(self):
#         connection = get_db()
#         if connection:
#             try:
#                 cursor = connection.cursor(dictionary=True)
#                 cursor.execute("SELECT * FROM Title")
#                 titles = cursor.fetchall()
#                 return titles
#             except Error as e:
#                 print(f"ERROR: {e}")
#             finally:
#                 cursor.close()
#                 connection.close()
#         return []
    
#     #example function to add titles
#     def add_titles(self, title_id, title_name=None, content_type=None, release_year=None, total_runtime=None, plot_summary=None, tmdb_avg_rating=None):
#         connection = get_db()
#         if connection:
#             try:
#                 cursor = connection.cursor()
#                 query = """
#                 INSERT INTO Title(
#                     title_id,
#                     title_name,
#                     content_type,
#                     release_year,
#                     total_runtime,
#                     plot_summary,
#                     tmdb_avg_rating
#                 )
#                 VALUES(%s, %s, %s, %s, %s, %s, %s)
#                 ON DUPLICATE KEY UPDATE
#                     title_name = COALESCE(VALUES(title_name)),
#                     content_type = COALESCE(VALUES(content_type)),
#                     release_year = COALESCE(VALUES(release_year)),
#                     total_runtime = COALESCE(VALUES(total_runtime)),
#                     plot_summary = COALESCE(VALUES(plot_summary)),
#                     tmdb_avg_rating = COALESCE(VALUES(tmdb_avg_rating))
#                 """
                
#                 values = (title_id, title_name, content_type, release_year, total_runtime, plot_summary, tmdb_avg_rating)
                
#                 cursor.execute(query, values)
#                 connection.commit()
#                 return cursor.lastrowid
#             except Error as e:
#                 print(f"ERROR: {e}")
#                 return None
#             finally:
#                 cursor.close()
#                 connection.close()
#             return None
        
#     # episode
#     def add_episodes(self, seasonepisode_id, title_id, episode_name=None, 
#                    airdate=None, synopsis=None, runtime=None):
#         """Add or update an episode"""
#         connection = get_db()
#         if connection:
#             try:
#                 cursor = connection.cursor()
#                 query = """
#                     INSERT INTO Episodes_Seasons (
#                         seasonepisode_id, 
#                         title_id, 
#                         episode_name, 
#                         airdate, 
#                         synopsis, 
#                         runtime
#                     )
#                     VALUES (%s, %s, %s, %s, %s, %s)
#                     ON DUPLICATE KEY UPDATE
#                         episode_name = COALESCE(VALUES(episode_name)),
#                         airdate = COALESCE(VALUES(airdate)),
#                         synopsis = COALESCE(VALUES(synopsis)),
#                         runtime = COALESCE(VALUES(runtime))
#                 """

#                 value = (seasonepisode_id, title_id, episode_name, 
#                         airdate, synopsis, runtime)
#                 cursor.execute(query, value)
                
#                 connection.commit()
#                 return cursor.lastrowid
#             except Error as e:
#                 print(f"ERROR: {e}")
#                 return None
#             finally:
#                 cursor.close()
#                 connection.close()
#             return None
    
#     # rating
#     def add_rating(self, rating, review_text, title_id):
#         connection = get_db()
#         if connection:
#             try:
#                 date_posted = datetime.datetime.now()
#                 cursor = connection.cursor()
#                 query = """
#                 INSERT INTO Rating(
#                     rating,
#                     date_posted,
#                     review_text,
#                     title_id
#                 )
#                 VALUES(%s, %s, %s, %s)
#                 """
#                 values = (rating, date_posted, review_text, title_id)
#                 cursor.execute(query, values)
#                 connection.commit()
#                 print(f"Rating: {rating} successfully added for title ID: {title_id}")
                
#                 return cursor.lastrowid
#             except Error as e:
#                 print(f"ERROR: {e}")
            
#             finally:
#                 cursor.close()
#                 connection.close()
    
#     def delete_rating(self, rating_id = None, title_id = None):
#         connection = get_db()
#         if connection:
#             try:
#                 cursor = connection.cursor()
                
#                 # prioritize deleting by rating_id, fallback to title_id if not possible
#                 if rating_id:
#                     print(f"***** Deleting Rating by Rating ID: {rating_id}")
                    
#                     cursor.execute(f"DELETE FROM Rating WHERE rating_id = {rating_id}")
                
#                 elif title_id:
#                     print(f"***** Deleting Rating by Title ID: {title_id}")
                    
#                     cursor.execute(f"DELETE FROM Rating WHERE title_id = {title_id}")
                
#                 else:
#                     print("****** Error: No ID provided by deletion")
#                     return False
                
#                 connection.commit()
                
#                 # check if any row was actually deleted
#                 if cursor.rowcount > 0:
#                     print("****** Rating deleted successfully")
#                     return True
#                 else:
#                     print("****** No rating found to delete")
#                     return False
                
#             except Error as e:
#                 print(f"ERROR: {e}")
#                 return False
#             finally:
#                 cursor.close()
#                 connection.close()
#             return False
#     # genre
#     def add_genre(self, genre_id, genre_name=None):
#         connection = get_db()
#         if connection:
#             try:
#                 cursor = connection.cursor()
#                 query = """
#                 INSERT INTO Genre(
#                     genre_id,
#                     genre_name
#                 )
#                 VALUES(%s, %s)
#                 ON DUPLICATE KEY UPDATE
#                     genre_name = COALESCE(VALUES(genre_name))
#                 """
                
#                 values = (genre_id, genre_name)
                
#                 cursor.execute(query, values)
#                 connection.commit()
#                 return cursor.lastrowid
#             except Error as e:
#                 print(f"ERROR: {e}")
#                 return None
#             finally:
#                 cursor.close()
#             return None
             
#     def link_title_genre(self, title_id, genre_id):
#         connection = get_db()
#         if connection:
#             try:
#                 cursor = connection.cursor()
#                 query = """
#                 INSERT INTO Title_Genre(
#                     title_id,
#                     genre_id
#                 )
#                 VALUES(%s, %s)
#                 """
                
#                 values = (title_id, genre_id)
                
#                 cursor.execute(query, values)
#                 connection.commit()
#                 return cursor.lastrowid
#             except Error as e:
#                 print(f"ERROR: {e}")
#                 return None
#             finally:
#                 cursor.close()
#             return None
    
#     # function to return all logs -> meant to be used eventually for frontend
#     def get_all_logs(self):
#         connection = get_db()
#         if connection:
#             try:
#                 print("*****Attempting to connect cursor...")
#                 cursor = connection.cursor(dictionary=True)
#                 print("*****Cursor connected successfully.")
#                 query = '''
#                 SELECT
#                 t.title_id, 
#                 t.title_name, 
#                 t.release_year, 
#                 t.content_type, 
#                 t.total_runtime as display_duration,
#                 r.rating, 
#                 r.date_posted,
                
#                 -- aggregate multiple genres into one string
#                 GROUP_CONCAT(g.genre_name SEPARATOR ', ') as genre_string
                
#                 FROM Title t
                
#                 -- JOINS
#                 LEFT JOIN Title_Genre tg ON t.title_id = tg.title_id
#                 LEFT JOIN Genre g ON tg.genre_id = g.genre_id
#                 LEFT JOIN Rating r ON t.title_id = r.title_id
#                 GROUP BY t.title_id, t.title_name, t.release_year, t.content_type, t.total_runtime, r.rating, r.date_posted
#                 '''
                
#                 print("*****executing query...")
#                 cursor.execute(query)
#                 print("*****query executed successfully.")
#                 logs = cursor.fetchall()
                
#                 # convert comara seperated string into a python list
#                 for log in logs:
#                     if log['genre_string']:
#                         log['genres'] = log['genre_string'].split(', ')
#                     else:
#                         log['genres'] = []
                    
#                     # remove temp string field to keep JSON clean
#                     del log['genre_string']
                
#                 return logs
#             except Error as e:
#                 print(f"ERROR: SQL or Connection failed: {Error}")
#                 return []
#             finally:
#                 print("*****closing cursor and connection...")
#                 cursor.close()
#                 if connection:
#                     connection.close()
                
#                 print("*****connection and cursor closed...")


#     # function to delete all tables in schema based on linkage
#     def delete_title_data(self,title_id):
#         connection = get_db()
#         if connection:
#             try:
#                 cursor = connection.cursor()

#                 # Delete dependent data first (Rating)
                
#                 cursor.execute("DELETE FROM Rating WHERE title_id = %s", (title_id,))
#                 cursor.execute("DELETE FROM Title_Genre WHERE title_id = %s",(title_id,))
#                 cursor.execute("DELETE FROM Episodes_Seasons WHERE title_id = %s",(title_id,))
#                 cursor.execute("DELETE FROM Title WHERE title_id = %s",(title_id,))
                
#                 connection.commit()
#                 print(f"Title ID {title_id} and all related data successfully deleted.")
#                 return True
            
#             except Error as e:
#                 connection.rollback()
#                 print(f"ERROR deleting title data: {e}")
#                 return False
#             finally:
#                 cursor.close()
#                 if connection:
#                     connection.close()
#         return False
    
#     # Clears all data from tables to keep them empty
#     def delete_all_data(self):
#         connection = get_db()
#         if connection:
#             try:
#                 cursor = connection.cursor()
#                 # Disable foreign key checks to allow truncation regardless of linkage
#                 cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
                
#                 # list tables to truncate
#                 tables = [
#                     'Title_Genre',
#                     'Episodes_Seasons',
#                     'Rating',
#                     'Genre',
#                     'Title'
#                 ]
                
#                 print("***** Starting database cleanup...")
                
#                 for table in tables:
#                     cursor.execute(f"TRUNCATE TABLE {table}")
#                     print(f"LOG: Table {table} executed")
                    
#                 # re-enable key checks
#             except Error as e:
#                 print(f"******ERROR: Failed to delete all data: {e}")
#                 try:
#                     cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
#                 except:
#                     pass
#                 return False

#             finally:
#                 cursor.close()
#                 connection.close()
                
#     """
#     Create a summarized statistics based on what is in the database
#     Average rating
#     Most watched genre
#     Percentage of how much tv/show has been watched
#     Total watchtime of movie/shows
#     """
    
#     def get_statistics(self):
#         connection = get_db()
#         if connection:
#             try:
#                 cursor = connection.cursor(dictionary = True)
#                 stats = {
#                     "total_titles" : 0,
#                     "total_watchtime_minutes" : 0,
#                     "total_watchtime_hours" : 0,
#                     "average_rating" : 0.0,
#                     "most_watched_genre" : "N/A",
#                     "movie_percentage" : 0,
#                     "tv_percentage" : 0
#                 }
                
#                 # General stats (counts and runtimes)
                
#                 query_general = """
#                 SELECT
#                     COUNT(*) as total_count,
#                     COALESCE(SUM(total_runtime), 0) as total_minutes,
#                     SUM(CASE WHEN content_type ='movie' THEN 1 ELSE 0 END) as movie_count,
#                     SUM(CASE WHEN content_type = 'tv' THEN 1 ELSE 0 END) as tv_count
#                 FROM Title
#                 """
#                 cursor.execute(query_general)
#                 general_data = cursor.fetchone()
                
#                 if general_data and general_data['total_count'] > 0:
#                     stats['total_titles'] = general_data['total_count']
#                     stats['total_watchtime_minutes'] = general_data['total_minutes']
#                     stats['total_watchtime_hours'] = general_data['total_minutes']/60
                    
#                     # Calculate Percentages
#                     stats["movie_percentage"] = round((general_data['movie_count'] / general_data['total_count']) * 100, 1)
#                     stats["tv_percentage"] = round((general_data['tv_count'] / general_data['total_count']) * 100, 1)
                
#                 # Average Rating
#                 cursor.execute("SELECT AVG(rating) as avg_rating FROM Rating")
#                 rating_data = cursor.fetchone()
#                 if rating_data and rating_data['avg_rating']:
#                     stats["average_rating"] = round(float(rating_data['avg_rating']), 1)
                
#                 # Most Watched Genre
#                 # title -> title_genre -> genre
                
#                 query_genre = """"
#                 SELECT g.genre_name, COUNT(tg.title_id) as count
#                 FROM Title_Genre tg
#                 JOIN Genre g ON tg.genre_id = g.genre_id
#                 GROUP BY g.genre_name
#                 ORDER BY count DESC
#                 LIMIT 1
#                 """
                
#                 cursor.execute(query_genre)
#                 genre_data = cursor.fetchone()
#                 if genre_data:
#                     stats["most_watched_genre"] = genre_data['genre_name']
                    
#                 return stats
            
#             except Error as e:
#                 print(f"ERROR : {e}")
#             finally:
#                 cursor.close()
#                 connection.close()
#         return None