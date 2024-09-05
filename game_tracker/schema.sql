DROP TABLE IF EXISTS player;
DROP TABLE IF EXISTS game;
DROP TABLE IF EXISTS game_played;
DROP TABLE IF EXISTS games_players_played;

CREATE TABLE player (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_name TEXT UNIQUE NOT NULL,
    player_bio TEXT,
    player_image TEXT,
    password TEXT
);
CREATE TABLE game (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_name TEXT NOT NULL,
    game_info TEXT
);
-- The date_played field is using the text format which stores date as YYYY-MM-DD
-- this makes it compatible with PostgreSQL's DATE format.
-- To insert a date do:
--      INSERT INTO game_played(date_played, game_id, player_id) VALUES (date('now'), 2, 3);
-- To select the date do:
--      SELECT date_played FROM game_played;
-- The foreign key 'player_id' is the winner of the game played
CREATE TABLE game_played (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date_played INTEGER NOT NULL DEFAULT CURRENT_DATE, 
    game_id INTEGER NOT NULL,
    player_id INTEGER NOT NULL,
    FOREIGN KEY (game_id) REFERENCES game (id),
    FOREIGN KEY (player_id) REFERENCES player (id)
);
CREATE TABLE games_players_played (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_played_id INTEGER NOT NULL,
    player_id INTEGER NOT NULL,
    FOREIGN KEY (game_played_id) REFERENCES game (id),
    FOREIGN KEY (player_id) REFERENCES player (id)
);