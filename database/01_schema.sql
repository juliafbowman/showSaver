CREATE DATABASE IF NOT EXISTS tvmate;
USE tvmate;

-- Create tables for Title, Genre, Person, Rating, Episode

CREATE TABLE IF NOT EXISTS Title(
    -- given from TMDB
    title_id INT PRIMARY KEY,
    title_name VARCHAR(255) NOT NULL,

    content_type ENUM('movie', 'tv') NOT NULL,

    -- metadata from TMDB
    release_year INT CHECK (release_year > 1880),
    total_runtime INT CHECK (total_runtime > 0),
    tmdb_avg_rating FLOAT,
    plot_summary TEXT
);

CREATE TABLE IF NOT EXISTS Episodes_Seasons(
    seasonepisode_id INT PRIMARY KEY,
    title_id INT,
    episode_name VARCHAR(255),
    airdate DATE,
    synopsis TEXT,
    runtime INT CHECK (runtime > 0),

    FOREIGN KEY (title_id) REFERENCES Title(title_id)
);



CREATE TABLE IF NOT EXISTS Person(
    person_id INT PRIMARY KEY,
    name VARCHAR(255)

);


CREATE TABLE IF NOT EXISTS Episode_Person(
    episode_id INT NOT NULL,
    person_id INT NOT NULL,

    role VARCHAR(100) NOT NULL,

    PRIMARY KEY(episode_id, person_id),
    FOREIGN KEY (episode_id) REFERENCES Episodes_Seasons(seasonepisode_id),
    FOREIGN KEY (person_id) REFERENCES Person(person_id)
);

CREATE TABLE IF NOT EXISTS Genre(
    genre_id INT PRIMARY KEY,
    genre_name VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS Title_Genre(
    genre_id INT NOT NULL,
    title_id INT NOT NULL,

    PRIMARY KEY(genre_id, title_id),
    FOREIGN KEY (genre_id) REFERENCES Genre(genre_id),
    FOREIGN KEY (title_id) REFERENCES Title(title_id)
);

CREATE TABLE IF NOT EXISTS Rating(
    rating_id INT PRIMARY KEY AUTO_INCREMENT,
    rating INT CHECK (rating BETWEEN 1 AND 10),
    date_posted DATE,
    review_text TEXT,
    title_id INT NOT NULL,

    FOREIGN KEY(title_id) REFERENCES Title(title_id)
 );

 