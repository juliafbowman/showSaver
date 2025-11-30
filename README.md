```
Welcome to...
 ____    __                              ____    __                                           
/\  _`\ /\ \                            /\  _`\ /\ \__                                        
\ \,\L\_\ \ \___     ___   __  __  __   \ \,\L\_\ \ ,_\   ___   _____   _____      __   _ __  
 \/_\__ \\ \  _ `\  / __`\/\ \/\ \/\ \   \/_\__ \\ \ \/  / __`\/\ '__`\/\ '__`\  /'__`\/\`'__\
   /\ \L\ \ \ \ \ \/\ \L\ \ \ \_/ \_/ \    /\ \L\ \ \ \_/\ \L\ \ \ \L\ \ \ \L\ \/\  __/\ \ \/ 
   \ `\____\ \_\ \_\ \____/\ \___x___/'    \ `\____\ \__\ \____/\ \ ,__/\ \ ,__/\ \____\\ \_\ 
    \/_____/\/_/\/_/\/___/  \/__//__/       \/_____/\/__/\/___/  \ \ \/  \ \ \/  \/____/ \/_/ 
                                                                  \ \_\   \ \_\               
                                                                   \/_/    \/_/
                                                                   
```

# What is Show Stopper?
Show Stopper is a Flask-based backend application designed to help users track and manager their TV show and movie watch history. It integrates The Movie Database (TMDB) API to fetch metadata and uses a local MySQL Database to store user logs, ratings, and statistics.

<img width="1424" height="788" alt="480MainPage" src="https://github.com/user-attachments/assets/038012bc-5ce2-4d7c-9109-89014ef21456" />

## Features
- **TMDB Integration** : Search for movies and TV shows, fetch details directly from TMDB.
- **Watch Logging** : Import titles into a local database to track what you've watched
- **Rating System** : Rate movies and TV shows with reviews.
- **Statistics** : View summarized stats lilke total watch time, average rating and most watched genres. 
- **RESTful API** : Provides endpoints for searching, logging, rating, and retrieving data.

## Development Team

### Frontend Team
#### **Julia Bowman** - [[LinkedIn](https://www.linkedin.com/in/juliafbowman/)]

#### **Basil Tiongson** - [[LinkedIn](https://www.linkedin.com/in/basiltiongson/)]

### Backend Team
#### **Jason Carmona** - [[LinkedIn](https://www.linkedin.com/in/cs-jason-carmona/)]

#### **Tam Le** - [[LinkedIn](https://www.linkedin.com/in/tamthanhle/)]

#### **Brian Li** - [[LinkedIn](https://www.linkedin.com/in/weitaoli1/)]


## Prerequisites

before running the application, ensure you have the following installed:
- **Python 3.8+**
- **MySQL Server** (ensure that it is running locally)
- **Node.js & npm**


## Setup & Installation

### 1. Clone the repository
```bash
git clone <https://github.com/jcarm6/Project-TVDB>
cd tvmate
```

### 2. Set up Virtual Environment
```bash
# Windows
python -m venv venv
venv/Scripts/activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Configuration
**1. Start MySQL Server:** Make sure your MySQL server is running

**2. Configure Environment Variables:** The project uses a ```.env``` file to manage database credentials. A template is provided in the uploaded files. Create a ```.env``` file titled ```.env``` in the **backend folder** with the following content:

```bash
# Database configuration
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=password <-- CHANGE THIS
DB_NAME=tvmate
```
*Note: Application automatically creates the tvmate database and required tables using the file ```01_schema.sql``` file.*

## Running The Application
Start the flask environment
```bash
python app.py
```

The server will start at ```http://127.0.0.1:5000/```

## Frontend
Create another terminal inside of our ```frontend``` folder. Then in the terminal:
```bash
npm install
# wait until finished
npm start
```

After this, you will have set up our web application correctly!

---

## API Endpoints
### TMDB Integration
```
Method,Endpoint,Description,Params
GET,/api/search,Search for movies/TV shows,query (string)
GET,/api/movie,Get movie details,id (TMDB ID)
GET,/api/show/seasons,Get season count for a show,id (TMDB ID)
GET,/api/show/episodes,Get episodes for a season,"id, season"
GET,/api/trending_movies,Get trending movies,None
GET,/api/trending_shows,Get trending TV shows,None
```

### Database Operations
```
Method,Endpoint,Description,Params/Body
GET,/api/db/import,Import title from TMDB to DB,"id, type ('movie'/'tv'), episode_id (optional for TV)"
GET,/api/logs,Get all watched logs,None
GET,/api/logs/sorted,Get sorted logs,"sort (title, release, rating, duration), order (asc, desc)"
DELETE,/api/logs/<id>,Delete a specific title log,title_id in URL
DELETE,/api/db/delete_all,Clear entire database,None
```

### Ratings & Stats
```
Method,Endpoint,Description,Params/Body
POST,/api/rating,Add a rating,"JSON: { ""rating"": 8.5, ""title_id"": 123, ""review_text"": ""Good!"" }"
DELETE,/api/rating,Delete a rating,rating_id OR title_id
GET,/api/stats,Get user watch statistics,None
```

## Project Structure
- ```app.py```: This is the main flask application entry point. This file defines our routes and API logic.
- ```dao.py```: Data Access Object. Handles all database connections and SQL Queries
- ```01_schema.sql```: SQL script for creating the database schema (tables for Title, Genre, Rating, etc.)
- ```requirements.txt```: List of Python dependencies
- ```.env```: Configuration file for database credentials

## User Interface
### Search a Title
![frankSearch](https://github.com/user-attachments/assets/064a17aa-a394-4ef9-9353-9f300990f161)

### Rate a Title
![frankRating](https://github.com/user-attachments/assets/87fbf89c-1170-4845-a364-7f02e6966052)

## Notes
- **TMDB API Key**: The ```app.py``` file currently contains a hardcoded TMBD API Key. For production we would move this key to .env file. But for this project we have decided to just hardcode it.
- **CORS**: Cross-Origin Resource Sharing is enabled, this allows a frontend application running on a different port to communicate with backend

## Future Improvments
- Implement user authentication.
- Refine error handling for TMDB IDs.
- Migrate TMDB API key to environment variables

