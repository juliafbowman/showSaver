# API Documentation

## GET /api/search?query=<search_text>

### Purpose

Search for movies, TV shows, or people.

### Query Parameters

| Name  | Type   | Required | Description        |
| ----- | ------ | -------- | ------------------ |
| query | string | Yes      | Text to search for |

### Return Fields

| Field        | Type   | Description                                 |
| ------------ | ------ | ------------------------------------------- |
| id           | int    | TMDB id                                     |
| media_tpye   | string | Type of result (movie, tv, or person)       |
| title        | string | Movie title (if media_type is movie)        |
| name         | string | TV show or person name (if applicable)      |
| overview     | string | Description or overview                     |
| poster_path  | string | Poster image path                           |
| release_date | string | Movie release date (if media_type is movie) |
| vote_average | string | Movie rating from TMDB                      |

### Example Response

```json
{
  "0": {
    "id": 355772,
    "media_type": "movie",
    "overview": "ToY is a drama about two lost souls from disparate backgrounds who find each other amid the desperation and glamour of Los Angeles, forging an unlikely relationship that spirals into tragic chaos.",
    "poster_path": "/38hm7meoMAGlRK0H8CrbzNCz4J9.jpg",
    "release_date": "2015-08-22",
    "title": "ToY",
    "vote_average": "8.0"
  }
}
```

---

## GET /api/show/seasons?id=<show_id>

### Purpose

Get the number of seasons and metadata for a TV show.

### Query Parameters

| Name | Type | Required | Description |
| ---- | ---- | -------- | ----------- |
| id   | int  | Yes      | TV show ID  |

### Return Fields

| Field             | Type   | Description                                              |
| ----------------- | ------ | -------------------------------------------------------- |
| number_of_seasons | int    | Total number of seasons in the TV show                   |
| seasons           | array  | List of season objects                                   |
| id                | int    | TMDB ID for the season                                   |
| air_date          | string | First air date of the season (format: YYYY-MM-DD)        |
| episode_count     | int    | Number of episodes in this season                        |
| name              | string | Name of the season (e.g., "Season 1", "Specials")        |
| overview          | string | Summary/description of the season                        |
| poster_path       | string | Path to the poster image for the season                  |
| season_number     | int    | Season number (0 for specials, 1 for first season, etc.) |
| vote_average      | float  | Average rating for the season                            |

### Example Response

```json
{
  "number_of_seasons": 2,
  "seasons": [
    {
      "air_date": "2023-01-08",
      "episode_count": 12,
      "id": 326816,
      "name": "Specials",
      "overview": "Nagatoro decides to train Senpai to become more popular, with the promise of a reward.",
      "poster_path": "/4Z11PQHlVI4QvxYTUKByLuf7MP6.jpg",
      "season_number": 0,
      "vote_average": 0.0
    },
    {
      "air_date": "2021-04-10",
      "episode_count": 12,
      "id": 155270,
      "name": "Season 1",
      "overview": "Every day, Naoto Hachiouji is teased relentlessly by Hayase Nagatoro, a first year student he meets one day in the library while working on his manga. After reading his story and seeing his awkward demeanor, she decides from that moment on to toy with him, even calling him \"Senpai\" in lieu of using his real name.\n\nAt first, Nagatoro's relentless antics are more bothersome than anything and leave him feeling embarrassed, as he is forced to cater to her whims. However, as they spend more time together, a strange sort of friendship develops between them, and Naoto finds that life with Nagatoro can even be fun. But one thing's for sure: his days will never be dull again.",
      "poster_path": "/ocznQZAqhG7EYTbAQgyIKAyXQRi.jpg",
      "season_number": 1,
      "vote_average": 7.1
    },
    {
      "air_date": "2023-01-06",
      "episode_count": 12,
      "id": 317660,
      "name": "2nd Attack",
      "overview": "Hayase Nagatoro and Naoto Hachiouji have grown closer: the girl spends more time than ever in the art club room with her senpai. Although he is always on edge, Naoto no longer seems to mind Nagatoro's presence. Time and again, Naoto demonstrates his hidden, cool demeanor, and Nagatoro displays her possessive tendencies. However, they still can not seem to completely close the distance between them. It is clear to everyone else that the pair have feelings for each other.\n\nFor Nagatoro, there is nothing more entertaining than toying with Naoto. But as the girl shows no plans to stop teasing her senpai, it is only a matter of time before they realize how they truly feel.",
      "poster_path": "/180GLeujRw5VrWLpjSX6GcUUimE.jpg",
      "season_number": 2,
      "vote_average": 7.2
    }
  ]
}
```

---

## GET /api/show/episodes?id=<show_id>&season=<season_number>

### Purpose

Get all episodes from a specific season of a TV show.

### Query Parameters

| Name   | Type | Required | Description   |
| ------ | ---- | -------- | ------------- |
| id     | int  | Yes      | TV show ID    |
| season | int  | Yes      | Season number |

### Return Fields

| Field          | Type   | Description                                  |
| -------------- | ------ | -------------------------------------------- |
| id             | int    | TMDB ID for the episode                      |
| air_date       | string | Air date of the episode (format: YYYY-MM-DD) |
| episode_number | int    | Episode number within the season             |
| name           | string | Episode title                                |
| overview       | string | Description of the episode                   |
| runtime        | int    | Duration of the episode in minutes           |
| still_path     | string | Path to the still image of the episode       |
| vote_average   | float  | Average rating for the episode               |

### Example Response

```json
{
  "0": {
    "air_date": "2021-04-11",
    "episode_number": 1,
    "id": 2334595,
    "name": "Senpai is a bit... / Senpai, don't you ever get angry?",
    "overview": "Senpai is a nerdy high schooler whose manga work is discovered by some loud girls in the library. They all tease him, but one among them, Nagatoro, takes it further than the others.",
    "runtime": 24,
    "still_path": "/gPHmaJaPjum8p0EQJUEAODCocSU.jpg",
    "vote_average": 6.545
  }
}
```

---

## GET /api/trending_movies

### Purpose

Get the list of trending movies for the week.

### Notes

Lightweight trending movie list for the homepage.
Only includes fields needed for the trending UI.

### Frontend Example

```js
useEffect(() => {
  const loadTrendingMovies = async () => {
    const res = await fetch("http://127.0.0.1:5000/api/trending_movies");
    const movies = await res.json();
    setTrendingMovies(movies); // or whatever you have set up
  };

  loadTrendingMovies();
}, []);
```

### Example Response

```json
[
  {
    "id": 673,
    "poster_path": "/aWxwnYoe8p2d2fcxOqtvAtJ72Rw.jpg",
    "rating": 8.0,
    "title": "Harry Potter and the Prisoner of Azkaban"
  },
  {
    "id": 967941,
    "poster_path": "/si9tolnefLSUKaqQEGz1bWArOaL.jpg",
    "rating": 5.5,
    "title": "Wicked: For Good"
  },
  {
    "id": 1323475,
    "poster_path": "/a66w2eVNFHMgevJlw0d6f4TTrrD.jpg",
    "rating": 5.8,
    "title": "Champagne Problems"
  }
]
```

---

## GET /api/trending_shows

### Purpose

Get the list of trending TV shows for the week.

### Example Frontend

```js
useEffect(() => {
  const loadTrendingShows = async () => {
    const res = await fetch("http://127.0.0.1:5000/api/trending_shows");
    const shows = await res.json();
    setTrendingShows(shows); //// or whatever you have set up
  };

  loadTrendingShows();
}, []);
```

### Example Response (simplified)

```json
[
  {
    "id": 225171,
    "poster_path": "/nrM2xFUfKJJEmZzd5d7kohT2G0C.jpg",
    "rating": 8.3,
    "title": "Pluribus"
  },
  {
    "id": 252193,
    "poster_path": "/wKNEFlrs68rzweVzfwkjWmkJqu7.jpg",
    "rating": 8.1,
    "title": "Last Samurai Standing"
  },
  {
    "id": 66732,
    "poster_path": "/cVxVGwHce6xnW8UaVUggaPXbmoE.jpg",
    "rating": 8.6,
    "title": "Stranger Things"
  },
  {
    "id": 200875,
    "poster_path": "/nyy3BITeIjviv6PFIXtqvc8i6xi.jpg",
    "rating": 8.001,
    "title": "IT: Welcome to Derry"
  }
]
```

---

## GET /api/movie?id=<movie_id>

### Purpose

Get detailed movie information by movie ID.

### Query Parameters

| Name | Type | Required | Description     |
| ---- | ---- | -------- | --------------- |
| id   | int  | Yes      | Movie ID (TMDB) |

### Returned Fields

| Field        | Description              |
| ------------ | ------------------------ |
| title        | Movie title              |
| overview     | Description of the movie |
| poster_path  | Poster image path        |
| release_date | Release date             |
| runtime      | Duration in minutes      |
| vote_average | Average rating           |
| genres       | List of genre objects    |

### Example Response

```json
{
  "genres": [
    {
      "id": 10749,
      "name": "Romance"
    },
    {
      "id": 53,
      "name": "Thriller"
    }
  ],
  "overview": "ToY is a drama about two lost souls from disparate backgrounds who find each other amid the desperation and glamour of Los Angeles, forging an unlikely relationship that spirals into tragic chaos.",
  "poster_path": "/38hm7meoMAGlRK0H8CrbzNCz4J9.jpg",
  "release_date": "2015-08-22",
  "runtime": 94,
  "title": "ToY",
  "vote_average": 5.382
}
```

---

## GET/POST /api/db/import?id=<tmdb_id>&type=<media_type>&episode_id=<episode_id>(optional)

### Purpose

Import a movie or TV show from TMDB into the database.

### Query Parameters

| Name       | Type   | Required | Description                            |
| ---------- | ------ | -------- | -------------------------------------- |
| id         | int    | Yes      | TMDB ID of the movie or TV show        |
| type       | string | Yes      | Media type: `movie` or `tv`            |
| episode_id | int    | No       | If provided, imports only that episode |

### Behavior

**Movies:**

- Fetches movie details from TMDB
- Inserts title and genres into database

**TV Shows:**

- Fetches TV show details from TMDB
- Inserts title and genres into database
- Imports all seasons and episodes (or specific episode if `episode_id` provided)
- Calculates total runtime from all episodes
- Updates title with computed total runtime

### Example Request

```
http://127.0.0.1:5000/api/db/import?id=355772&type=movie
http://127.0.0.1:5000/api/db/import?id=105556&type=tv
http://127.0.0.1:5000/api/db/import?id=105556&type=tv&episode_id=4202979
```

### Example Response

**Movie:**

```json
{
  "status": "imported",
  "tmdb_id": 355772,
  "type": "movie"
}
```

**TV:**

```json
{
  "status": "imported",
  "tmdb_id": 105556,
  "type": "tv",
  "total_runtime": 1440
}
```

### Error Response

```json
{
  "error": "type must be 'movie' or 'tv'"
}
```

---
