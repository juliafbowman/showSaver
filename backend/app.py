import requests
from flask import Flask, jsonify, request
from flask_cors import CORS
from dao import DAO

app = Flask(__name__)
CORS(app)  # Allow Next.js frontend to access backend API
dao = DAO()

TMDB_API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJhYjhhZTg0NGQ0ZWIxM2ZmNzBmYjBhZTllMGE5NzIyNiIsIm5iZiI6MTc2MjY0NzA2OS4zLCJzdWIiOiI2OTBmZGMxZDI4NTlkZDk3NTU0YzdiMTQiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.9kKW08BtDzsVFyq7kpQn9iEBwGmlezpgIpRVwQHIWCA"

HEADER = {
    "accept": "application/json",
    "Authorization": f"Bearer {TMDB_API_KEY}"
}

TMDB_BASE = "https://api.themoviedb.org/3"

def tmdb_get(path, params=None):
    params = params or {}
    response = requests.get(f"{TMDB_BASE}{path}", headers=HEADER, params=params, timeout=10)
    return response.json()

# test on browser by entering http://127.0.0.1:5000/ ( or whatever your terminals says)
@app.route("/")
def home():
    return "backend (flask) working"

# testing on browser by entering http://127.0.0.1:5000/api/hello ( or whatever your terminal says + /api/hello)
@app.route("/api/hello")
def hello():
    return jsonify({"message": "Hello from Flask Backend!"}) # converts python data into json responses

# search?query=toy
# http://127.0.0.1:5000/api/search?query=toy
@app.route("/api/search", methods=["GET"])
def getMulti():
    user_input = request.args.get("query")

    data = tmdb_get(f"/search/multi", {"language": "en-US", "page": "1", "include_adult": "false", "query": {user_input}})

    data = data["results"]

    # parse and simplify response
    parsed_data = {}

    for i, film in enumerate(data):
        curr_dict = {}

        curr_dict["id"] = film.get("id")
        curr_dict["title"] = film.get("title") or film.get("name")
        curr_dict["overview"] = film.get("overview")
        curr_dict["poster_path"] = film.get("poster_path")
        curr_dict["media_type"] = film.get("media_type")
        curr_dict["release_date"] = film.get("release_date")
        curr_dict['vote_average'] = film.get("vote_average")

        parsed_data[i] = curr_dict
    
    return jsonify(parsed_data)

# get movie details
# http://127.0.0.1:5000/api/movie?id=355772
@app.route("/api/movie", methods=["GET"])
def getMovie():
    movie_id = request.args.get("id")
    
    data = tmdb_get(f"/movie/{movie_id}", {"language": "en-US"})

    parsed_movie = {
        "title": data.get("title"),
        "overview": data.get("overview"),
        "poster_path": data.get("poster_path"),
        "release_date": data.get("release_date"),
        "runtime": data.get("runtime"),
        "vote_average": data.get("vote_average"),
        "genres": data.get("genres")
    }

    return jsonify(parsed_movie)

# get total number of seasons for a TV show
# http://127.0.0.1:5000/api/show/seasons?id=105556
@app.route("/api/show/seasons", methods=["GET"])
def getSeasons():
    show_id = request.args.get("id")
    
    data = tmdb_get(f"/tv/{show_id}", {"language": "en-US"})

    parsed_seasons = {
        "number_of_seasons": data.get("number_of_seasons"),
        "seasons": data.get("seasons")
    }
    
    return jsonify(parsed_seasons)

# get episode details for a TV show
# http://127.0.0.1:5000/api/show/episodes?id=105556&season=1
@app.route("/api/show/episodes", methods=["GET"])
def getEpisodes():
    show_id = request.args.get("id")
    season = request.args.get("season")
    
    data = tmdb_get(f"/tv/{show_id}/season/{season}", {"language": "en-US"})
    
    # parse episode data
    parsed_episodes = {}
    
    if "episodes" in data:
        for i, episode in enumerate(data["episodes"]):
            episode_data = {
                "id": episode.get("id"),
                "episode_number": episode.get("episode_number"),
                "name": episode.get("name"),
                "overview": episode.get("overview"),
                "air_date": episode.get("air_date"),
                "still_path": episode.get("still_path"),
                "vote_average": episode.get("vote_average"),
                "runtime": episode.get("runtime")
            }

            parsed_episodes[i] = episode_data
    
    return jsonify(parsed_episodes)


# http://127.0.0.1:5000/api/trending_movies
# Todo: Needs proper parsing
@app.route("/api/trending_movies")
def getTrendingMovies():
    url = "https://api.themoviedb.org/3/trending/movie/week?language=en-US"

    response = requests.get(url, headers=HEADER)

    data = response.json()

    data = data["results"]

    parsed_data = {}

    for i, movie in enumerate(data):
        curr_dict = {}

        curr_dict["id"] = movie.get("id")
        curr_dict["title"] = movie.get("title") or movie.get("name")
        curr_dict["poster_path"] = movie.get("poster_path")
        curr_dict["rating"] = movie.get("vote_average")

        #curr_dict["genre_ids"] = movie.get("genre_ids") # this removed for now, but need to ask frontend if they want to show genre in trending
        # thinking of making this a lot more lightweight...showing trending page doesnt need a lot of details
        # curr_dict["media_type"] = movie.get("media_type")
        # curr_dict["release_date"] = movie.get("release_date")
        # curr_dict["overview"] = movie.get("overview")

        parsed_data[i] = curr_dict

    return jsonify(list((parsed_data.values())))

# http://127.0.0.1:5000/api/trending_shows
# Todo: Needs proper parsing
@app.route("/api/trending_shows")
def getTrendingShows():
    url = "https://api.themoviedb.org/3/trending/tv/week?language=en-US"

    response = requests.get(url, headers=HEADER)

    data = response.json()

    data = data["results"]

    parsed_data = {}
    for i, show in enumerate(data):
        curr_dict = {}

        curr_dict["id"] = show.get("id")
        curr_dict["title"] = show.get("title") or show.get("name")
        curr_dict["poster_path"] = show.get("poster_path")
        curr_dict["rating"] = show.get("vote_average")

        # should make it thin by removing below fields
        # curr_dict["overview"] = show.get("overview")
        # curr_dict["media_type"] = show.get("media_type")
        # curr_dict["release_date"] = show.get("first_air_date")
        # curr_dict["genre_ids"] = show.get("genre_ids") # still need to ask frontend if they want this

        parsed_data[i] = curr_dict

    return jsonify(list((parsed_data.values())))

# api for DB
# http://127.0.0.1:5000/api/db/import?id=355772&type=movie
# http://127.0.0.1:5000/api/db/import?id=105556&type=tv&episode_id=4202979
# http://127.0.0.1:5000/api/db/import?id=105556&type=tv
@app.route("/api/db/import", methods=["GET", "POST"])
def tmdb_import():
    tmdb_id = request.args.get("id")
    media_type = request.args.get("type")

    if media_type == 'movie':
        details = tmdb_get(f"/movie/{tmdb_id}", {"language": "en-US"})
        title_id = details["id"]
        title_name = details.get("title")
        content_type = "movie"
        release_year = (details.get("release_date") or "")[:4] or None
        total_runtime = details.get("runtime")
        plot_summary = details.get("overview")
        tmdb_avg_rating = details.get("vote_average")

        # get movie info
        dao.add_titles(
            title_id, 
            title_name, 
            content_type, 
            release_year, 
            total_runtime, 
            plot_summary, 
            tmdb_avg_rating
        )

        for genre in details.get("genres", []):
            dao.add_genre(genre["id"], genre["name"])
            dao.link_title_genre(title_id, genre["id"])

        return jsonify({"status": "imported", "tmdb_id": title_id, "type": "movie"}), 201

    elif media_type == 'tv':
        episode_id = request.args.get("episode_id", default=1, type=int)
        details = tmdb_get(f"/tv/{tmdb_id}", {"language": "en-US"})
        title_id = details["id"]
        title_name = details.get("name")
        content_type = "tv"
        release_year = (details.get("first_air_date") or "")[:4] or None
        total_runtime = 0
        plot_summary = details.get("overview")
        tmdb_avg_rating = details.get("vote_average")

        # get tv info
        dao.add_titles(
            title_id, 
            title_name, 
            content_type, 
            release_year, 
            None, 
            plot_summary, 
            tmdb_avg_rating
        )

        for genre in details.get("genres", []):
            dao.add_genre(genre["id"], genre["name"])
            dao.link_title_genre(title_id, genre["id"])

        for season in details.get("seasons", []):
            season_number = season.get("season_number")
            if season_number is None:
                continue
            
            try:
                season_data = tmdb_get(f"/tv/{tmdb_id}/season/{season_number}", {"language": "en-US"})
                for episode in season_data.get("episodes", []):
                    seasonepisode_id = episode.get("id")
                    episode_name = episode.get("name")
                    airdate = episode.get("air_date")
                    synopsis = episode.get("overview")
                    runtime = episode.get("runtime")
                    total_runtime += runtime  # calculate total runtime
                    
                    # match the episode user picked
                    if seasonepisode_id == episode_id:
                        dao.add_episodes(
                            seasonepisode_id, 
                            title_id, 
                            episode_name, 
                            airdate, 
                            synopsis, 
                            runtime
                        )
                    else:
                        dao.add_episodes(
                            seasonepisode_id, 
                            title_id, 
                            episode_name, 
                            airdate, 
                            synopsis, 
                            runtime
                        )
            except Exception as e:
                print(f"ERROR fetching season {season_number}: {e}")
                continue

        # update total runtime
        dao.add_titles(
            title_id,
            title_name,
            content_type,
            release_year,
            total_runtime,
            plot_summary,
            tmdb_avg_rating
        )

        return jsonify({"status": "imported", "tmdb_id": title_id, "type": "tv", "episode_id": seasonepisode_id}), 201

    else:
        return jsonify({"error": "type must be 'movie' or 'tv'"}), 400

# route function that returns all logs
@app.route('/api/logs', methods = ['GET'])
def get_logs_route():
    try:
        logs = dao.get_all_logs()
        
        if logs is None:
            return jsonify({'error' : 'Database error occured'}), 500
        
        return jsonify(logs),200
    except Exception as e:
        return jsonify({'error' : 'str(e)'}), 500

# return sorted logs 
@app.route('/api/logs/sorted', methods=['GET'])
def get_sorted_logs_route():
    sort = request.args.get('sort', 'title') 
    order = request.args.get('order', 'asc')  

    logs = dao.get_sorted_logs(sort, order)
    return jsonify(logs), 200


# function deletes data for specific title_id
@app.route('/api/logs/<int:title_id>', methods = ['DELETE'])
def delete_title_data(title_id):
    try:
        print(f"*****ATTEMPTING TO DELETE TITLE_ID : {title_id}")
        dao.delete_title_data(title_id)
        print("***** TITLE_ID SUCCESSFULLY DELETED")
        return jsonify({'message' : 'Title deleted successfully'}), 200
    except Exception as e:
        print(f"*****ERROR: {e}")
        return jsonify({'error' : str(e)}), 500


# function to delete rating by rating_id or title_id
@app.route('/api/rating', methods = ['DELETE'])
def delete_rating_route():
    # Get parameters from URL (ex: ?rating_id=5 or ?title_id=101)
    rating_id = request.args.get('rating_id')
    title_id = request.args.get('title_id')
    
    # Ensure one id was sent
    if not rating_id and not title_id:
        return jsonify({'error' : 'you must provide either a rating_id or a title_id'})
    
    try:
        # Call DAO method
        success = dao.delete_rating(rating_id = rating_id, title_id = title_id)
        
        # Handle response
        
        if success:
            return jsonify({'message' : 'Rating deleted successfully'}) , 200
        else:
            return jsonify({'error' : 'Rating not found or already deleted'}), 404
        
    except Exception as e:
        print(f"******ERROR: {e}")
        return jsonify({'error' : str(e)}),500


# This function deletes all data in databse, used for debugging and before plugging into main
@app.route('/api/db/delete_all', methods = ['DELETE'])
def delete_all_data():
    try:
        print("*****ATTEMPTING TO DELETE ALLLLL DATA...")
        success = dao.delete_all_data()
        if success:
            print("****** ALL DATA IN DATABASE DELETED")
            return jsonify({'message' : 'All data deleted successfully'}),200
        else:
            print("****** FAILED TO DELETE DATA")
            return jsonify({'error' : 'Database operation failed interally'}),500
    
    except Exception as e:
        print(f"*****ERROR : {e}")
        return jsonify({'error' : str(e)}), 500
    
# add rating
@app.route('/api/rating', methods=['POST'])
def add_rating_route():
    data = request.get_json(silent=True) or {}
    # accept JSON or query params 
    # (ex: ?rating=5&title_id=105556&review_text=good)
    # (ex: .\backend\test.js)
    rating = data.get('rating') or request.args.get('rating')
    title_id = data.get('title_id') or request.args.get('title_id')
    review_text = data.get('review_text') or request.args.get('review_text', '')

    if rating is None or title_id is None:
        return jsonify({'error': 'rating and title_id are required'}), 400

    try:
        rating_val = float(rating)
    except Exception:
        return jsonify({'error': 'rating must be a number'}), 400

    try:
        title_id_val = int(title_id)
    except Exception:
        return jsonify({'error': 'title_id must be an integer'}), 400

    try:
        new_id = dao.add_rating(rating_val, review_text, title_id_val)
        if new_id:
            return jsonify({'message': 'Rating added', 'rating_id': new_id}), 201
        else:
            return jsonify({'error': 'Failed to add rating'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route for get_statistics in dao.py -> returns statistics as JSON
@app.route('/api/stats', methods = ['GET'])
def get_stats_route():
    dao = DAO()
    try:
        stats = dao.get_statistics()
        if stats:
            return jsonify(stats), 200
        else:
            return jsonify({'error' : 'Could not calculate statistics'}), 500
        
    except Exception as e:
        print(f"ERROR: {e}")
        return jsonify({'error' : str(e)}), 500
    
if __name__ == "__main__":
    app.run(debug=True, port=5000)

# import requests
# from flask import Flask, jsonify, request
# from flask_cors import CORS
# from dao import DAO

# app = Flask(__name__)
# CORS(app)  # Allow Next.js frontend to access backend API
# dao = DAO()

# TMDB_API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJhYjhhZTg0NGQ0ZWIxM2ZmNzBmYjBhZTllMGE5NzIyNiIsIm5iZiI6MTc2MjY0NzA2OS4zLCJzdWIiOiI2OTBmZGMxZDI4NTlkZDk3NTU0YzdiMTQiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.9kKW08BtDzsVFyq7kpQn9iEBwGmlezpgIpRVwQHIWCA"

# HEADER = {
#     "accept": "application/json",
#     "Authorization": f"Bearer {TMDB_API_KEY}"
# }

# TMDB_BASE = "https://api.themoviedb.org/3"

# def tmdb_get(path, params=None):
#     params = params or {}
#     response = requests.get(f"{TMDB_BASE}{path}", headers=HEADER, params=params, timeout=10)
#     return response.json()

# # test on browser by entering http://127.0.0.1:5000/ ( or whatever your terminals says)
# @app.route("/")
# def home():
#     return "backend (flask) working"

# # testing on browser by entering http://127.0.0.1:5000/api/hello ( or whatever your terminal says + /api/hello)
# @app.route("/api/hello")
# def hello():
#     return jsonify({"message": "Hello from Flask Backend!"}) # converts python data into json responses

# # search?query=toy
# # http://127.0.0.1:5000/api/search?query=toy
# @app.route("/api/search", methods=["GET"])
# def getMulti():
#     user_input = request.args.get("query")

#     data = tmdb_get(f"/search/multi", {"language": "en-US", "page": "1", "include_adult": "false", "query": {user_input}})

#     data = data["results"]

#     # parse and simplify response
#     parsed_data = {}

#     for i, film in enumerate(data):
#         curr_dict = {}

#         curr_dict["id"] = film.get("id")
#         curr_dict["title"] = film.get("title") or film.get("name")
#         curr_dict["overview"] = film.get("overview")
#         curr_dict["poster_path"] = film.get("poster_path")
#         curr_dict["media_type"] = film.get("media_type")
#         curr_dict["release_date"] = film.get("release_date")
#         curr_dict['vote_average'] = film.get("vote_average")

#         parsed_data[i] = curr_dict
    
#     return jsonify(parsed_data)

# # get movie details
# # http://127.0.0.1:5000/api/movie?id=355772
# @app.route("/api/movie", methods=["GET"])
# def getMovie():
#     movie_id = request.args.get("id")
    
#     data = tmdb_get(f"/movie/{movie_id}", {"language": "en-US"})

#     parsed_movie = {
#         "title": data.get("title"),
#         "overview": data.get("overview"),
#         "poster_path": data.get("poster_path"),
#         "release_date": data.get("release_date"),
#         "runtime": data.get("runtime"),
#         "vote_average": data.get("vote_average"),
#         "genres": data.get("genres")
#     }

#     return jsonify(parsed_movie)

# # get total number of seasons for a TV show
# # http://127.0.0.1:5000/api/show/seasons?id=105556
# @app.route("/api/show/seasons", methods=["GET"])
# def getSeasons():
#     show_id = request.args.get("id")
    
#     data = tmdb_get(f"/tv/{show_id}", {"language": "en-US"})

#     parsed_seasons = {
#         "number_of_seasons": data.get("number_of_seasons"),
#         "seasons": data.get("seasons")
#     }
    
#     return jsonify(parsed_seasons)

# # get episode details for a TV show
# # http://127.0.0.1:5000/api/show/episodes?id=105556&season=1
# @app.route("/api/show/episodes", methods=["GET"])
# def getEpisodes():
#     show_id = request.args.get("id")
#     season = request.args.get("season")
    
#     data = tmdb_get(f"/tv/{show_id}/season/{season}", {"language": "en-US"})
    
#     # parse episode data
#     parsed_episodes = {}
    
#     if "episodes" in data:
#         for i, episode in enumerate(data["episodes"]):
#             episode_data = {
#                 "id": episode.get("id"),
#                 "episode_number": episode.get("episode_number"),
#                 "name": episode.get("name"),
#                 "overview": episode.get("overview"),
#                 "air_date": episode.get("air_date"),
#                 "still_path": episode.get("still_path"),
#                 "vote_average": episode.get("vote_average"),
#                 "runtime": episode.get("runtime")
#             }

#             parsed_episodes[i] = episode_data
    
#     return jsonify(parsed_episodes)


# # http://127.0.0.1:5000/api/trending_movies
# # Todo: Needs proper parsing
# @app.route("/api/trending_movies")
# def getTrendingMovies():
#     url = "https://api.themoviedb.org/3/trending/movie/week?language=en-US"

#     response = requests.get(url, headers=HEADER)

#     data = response.json()

#     data = data["results"]

#     parsed_data = {}

#     for i, movie in enumerate(data):
#         curr_dict = {}

#         curr_dict["id"] = movie.get("id")
#         curr_dict["title"] = movie.get("title") or movie.get("name")
#         curr_dict["poster_path"] = movie.get("poster_path")
#         curr_dict["rating"] = movie.get("vote_average")

#         #curr_dict["genre_ids"] = movie.get("genre_ids") # this removed for now, but need to ask frontend if they want to show genre in trending
#         # thinking of making this a lot more lightweight...showing trending page doesnt need a lot of details
#         # curr_dict["media_type"] = movie.get("media_type")
#         # curr_dict["release_date"] = movie.get("release_date")
#         # curr_dict["overview"] = movie.get("overview")

#         parsed_data[i] = curr_dict

#     return jsonify(list((parsed_data.values())))

# # http://127.0.0.1:5000/api/trending_shows
# # Todo: Needs proper parsing
# @app.route("/api/trending_shows")
# def getTrendingShows():
#     url = "https://api.themoviedb.org/3/trending/tv/week?language=en-US"

#     response = requests.get(url, headers=HEADER)

#     data = response.json()

#     data = data["results"]

#     parsed_data = {}
#     for i, show in enumerate(data):
#         curr_dict = {}

#         curr_dict["id"] = show.get("id")
#         curr_dict["title"] = show.get("title") or show.get("name")
#         curr_dict["poster_path"] = show.get("poster_path")
#         curr_dict["rating"] = show.get("vote_average")

#         # should make it thin by removing below fields
#         # curr_dict["overview"] = show.get("overview")
#         # curr_dict["media_type"] = show.get("media_type")
#         # curr_dict["release_date"] = show.get("first_air_date")
#         # curr_dict["genre_ids"] = show.get("genre_ids") # still need to ask frontend if they want this

#         parsed_data[i] = curr_dict

#     return jsonify(list((parsed_data.values())))

# # api for DB
# # http://127.0.0.1:5000/api/db/import?id=355772&type=movie
# # http://127.0.0.1:5000/api/db/import?id=105556&type=tv&episode_id=4202979
# # http://127.0.0.1:5000/api/db/import?id=105556&type=tv
# @app.route("/api/db/import", methods=["GET", "POST"])
# def tmdb_import():
#     tmdb_id = request.args.get("id")
#     media_type = request.args.get("type")

#     if media_type == 'movie':
#         details = tmdb_get(f"/movie/{tmdb_id}", {"language": "en-US"})
#         title_id = details["id"]
#         title_name = details.get("title")
#         content_type = "movie"
#         release_year = (details.get("release_date") or "")[:4] or None
#         total_runtime = details.get("runtime")
#         plot_summary = details.get("overview")
#         tmdb_avg_rating = details.get("vote_average")

#         # get movie info
#         dao.add_titles(
#             title_id, 
#             title_name, 
#             content_type, 
#             release_year, 
#             total_runtime, 
#             plot_summary, 
#             tmdb_avg_rating
#         )

#         for genre in details.get("genres", []):
#             dao.add_genre(genre["id"], genre["name"])
#             dao.link_title_genre(title_id, genre["id"])

#         return jsonify({"status": "imported", "tmdb_id": title_id, "type": "movie"}), 201

#     elif media_type == 'tv':
#         episode_id = request.args.get("episode_id", default=1, type=int)
#         details = tmdb_get(f"/tv/{tmdb_id}", {"language": "en-US"})
#         title_id = details["id"]
#         title_name = details.get("name")
#         content_type = "tv"
#         release_year = (details.get("first_air_date") or "")[:4] or None
#         total_runtime = 0
#         plot_summary = details.get("overview")
#         tmdb_avg_rating = details.get("vote_average")

#         # get tv info
#         dao.add_titles(
#             title_id, 
#             title_name, 
#             content_type, 
#             release_year, 
#             None, 
#             plot_summary, 
#             tmdb_avg_rating
#         )

#         for genre in details.get("genres", []):
#             dao.add_genre(genre["id"], genre["name"])
#             dao.link_title_genre(title_id, genre["id"])

#         for season in details.get("seasons", []):
#             season_number = season.get("season_number")
#             if season_number is None:
#                 continue
            
#             try:
#                 season_data = tmdb_get(f"/tv/{tmdb_id}/season/{season_number}", {"language": "en-US"})
#                 for episode in season_data.get("episodes", []):
#                     seasonepisode_id = episode.get("id")
#                     episode_name = episode.get("name")
#                     airdate = episode.get("air_date")
#                     synopsis = episode.get("overview")
#                     runtime = episode.get("runtime")
#                     total_runtime += runtime  # calculate total runtime
                    
#                     # match the episode user picked
#                     if seasonepisode_id == episode_id:
#                         dao.add_episodes(
#                             seasonepisode_id, 
#                             title_id, 
#                             episode_name, 
#                             airdate, 
#                             synopsis, 
#                             runtime
#                         )
#                     else:
#                         dao.add_episodes(
#                             seasonepisode_id, 
#                             title_id, 
#                             episode_name, 
#                             airdate, 
#                             synopsis, 
#                             runtime
#                         )
#             except Exception as e:
#                 print(f"ERROR fetching season {season_number}: {e}")
#                 continue

#         # update total runtime
#         dao.add_titles(
#             title_id,
#             title_name,
#             content_type,
#             release_year,
#             total_runtime,
#             plot_summary,
#             tmdb_avg_rating
#         )

#         return jsonify({"status": "imported", "tmdb_id": title_id, "type": "tv", "episode_id": seasonepisode_id}), 201

#     else:
#         return jsonify({"error": "type must be 'movie' or 'tv'"}), 400

# # route function that returns all logs
# @app.route('/api/logs', methods = ['GET'])
# def get_logs_route():
#     try:
#         logs = dao.get_all_logs()
        
#         if logs is None:
#             return jsonify({'error' : 'Database error occured'}), 500
        
#         return jsonify(logs),200
#     except Exception as e:
#         return jsonify({'error' : 'str(e)'}), 500

# # function deletes data for specific title_id
# @app.route('/api/logs', methods = ['DELETE'])
# def delete_title_data(title_id):
#     # Get parameters from URL (ex: ?title_id=101)
#     title_id = request.args.get('title_id')
#     try:
#         print(f"*****ATTEMPTING TO DELETE TITLE_ID : {title_id}")
#         dao.delete_title_data(title_id)
#         print("***** TITLE_ID SUCCESSFULLY DELETED")
#         return jsonify({'message' : 'Title deleted successfully'}), 200
#     except Exception as e:
#         print(f"*****ERROR: {e}")
#         return jsonify({'error' : str(e)}), 500


# # function to delete rating by rating_id or title_id
# @app.route('/api/rating', methods = ['DELETE'])
# def delete_rating_route():
#     # Get parameters from URL (ex: ?rating_id=5 or ?title_id=101)
#     rating_id = request.args.get('rating_id')
#     title_id = request.args.get('title_id')
    
#     # Ensure one id was sent
#     if not rating_id and not title_id:
#         return jsonify({'error' : 'you must provide either a rating_id or a title_id'})
    
#     try:
#         # Call DAO method
#         success = dao.delete_rating(rating_id = rating_id, title_id = title_id)
        
#         # Handle response
        
#         if success:
#             return jsonify({'message' : 'Rating deleted successfully'}) , 200
#         else:
#             return jsonify({'error' : 'Rating not found or already deleted'}), 404
        
#     except Exception as e:
#         print(f"******ERROR: {e}")
#         return jsonify({'error' : str(e)}),500


# # This function deletes all data in databse, used for debugging and before plugging into main
# @app.route('/api/db/delete_all', methods = ['DELETE'])
# def delete_all_data():
#     try:
#         print("*****ATTEMPTING TO DELETE ALLLLL DATA...")
#         success = dao.delete_all_data()
#         if success:
#             print("****** ALL DATA IN DATABASE DELETED")
#             return jsonify({'message' : 'All data deleted successfully'}),200
#         else:
#             print("****** FAILED TO DELETE DATA")
#             return jsonify({'error' : 'Database operation failed interally'}),500
    
#     except Exception as e:
#         print(f"*****ERROR : {e}")
#         return jsonify({'error' : str(e)}), 500
    
# # add rating
# @app.route('/api/rating', methods=['POST'])
# def add_rating_route():
#     data = request.get_json(silent=True) or {}
#     # accept JSON or query params 
#     # (ex: ?rating=5&title_id=105556&review_text=good)
#     # (ex: .\backend\test.js)
#     rating = data.get('rating') or request.args.get('rating')
#     title_id = data.get('title_id') or request.args.get('title_id')
#     review_text = data.get('review_text') or request.args.get('review_text', '')

#     if rating is None or title_id is None:
#         return jsonify({'error': 'rating and title_id are required'}), 400

#     try:
#         rating_val = float(rating)
#     except Exception:
#         return jsonify({'error': 'rating must be a number'}), 400

#     try:
#         title_id_val = int(title_id)
#     except Exception:
#         return jsonify({'error': 'title_id must be an integer'}), 400

#     try:
#         new_id = dao.add_rating(rating_val, review_text, title_id_val)
#         if new_id:
#             return jsonify({'message': 'Rating added', 'rating_id': new_id}), 201
#         else:
#             return jsonify({'error': 'Failed to add rating'}), 500
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# # Route for get_statistics in dao.py -> returns statistics as JSON
# @app.route('/api/stats', methods = ['GET'])
# def get_stats_route():
#     dao = DAO()
#     try:
#         stats = dao.get_statistics()
#         if stats:
#             return jsonify(stats), 200
#         else:
#             return jsonify({'error' : 'Could not calculate statistics'}), 500
        
#     except Exception as e:
#         print(f"ERROR: {e}")
#         return jsonify({'error' : str(e)}), 500
    
# if __name__ == "__main__":
#     app.run(debug=True, port=5000)