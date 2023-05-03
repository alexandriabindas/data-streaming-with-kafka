-- Use chess.com database
use chess.com;


-- Add DBMS
CREATE TABLE ChessGameType (
    id SERIAL PRIMARY KEY,
    gameType VARCHAR(50) NOT NULL
		displayName VARCHAR(50) NOT NULL
);

INSERT INTO ChessGameType (gameType, displayName) VALUES ('live_rapid', 'Rapid');
INSERT INTO ChessGameType (gameType, displayName) VALUES ('live_blitz', 'Blitz');
INSERT INTO ChessGameType (gameType, displayName) VALUES ('daily', 'Daily');
ALTER TABLE ChessGameType ADD CONSTRAINT ChessGameType_gameType_unique UNIQUE (gameType);


SELECT * FROM ChessGameType;
-- Before Normalization

-- CREATE TABLE Leaderboard(
--   playerId INTEGER PRIMARY KEY,
--   playerName VARCHAR(30),
-- 	playerUsername VARCHAR(50) NOT NULL,
--   playerRank INTEGER NOT NULL,
-- 	winCount INTEGER NOT NULL,
-- 	lossCount INTEGER NOT NULL,
-- 	drawCount INTEGER NOT NULL,
-- 	score INTEGER NOT NULL,
-- 	country VARCHAR(250),
-- 	gameType VARCHAR(200)
-- );


-- Leaderboard Table
CREATE TABLE Leaderboard(
  leaderboardId SERIAL PRIMARY KEY,
	player_id INTEGER NOT NULL,
	gametype VARCHAR(50) NOT NULL,
  	playerRank INTEGER NOT NULL,
	winCount INTEGER NOT NULL,
	lossCount INTEGER NOT NULL,
	drawCount INTEGER NOT NULL,
	score INTEGER NOT NULL,
	CONSTRAINT Leaderboard_PlayerId_FK FOREIGN KEY (player_id) REFERENCES Player(player_id),
	CONSTRAINT Leaderboard_GameType_FK FOREIGN KEY (gametype) REFERENCES ChessGameType(gametype)
);

SELECT * FROM Leaderboard;

-- Chess Player Table
CREATE TABLE Player (
	player_id 					INTEGER PRIMARY KEY,
	player_name 				VARCHAR(255),
	username 						VARCHAR(255) NOT NULL,
	player_title 				VARCHAR(255),
	player_status 			VARCHAR(255) NOT NULL,
	player_location 		VARCHAR(255),
	player_country 			VARCHAR(255) NOT NULL,
	joined_on 					TIMESTAMP NOT NULL,
	last_online 				TIMESTAMP NOT NULL,
	followers 					INTEGER NOT NULL,
	is_streamer 				BOOLEAN
);
SELECT * FROM Player;
SELECT * FROM Player WHERE is_streamer = False;

-- Complex query to retrieve player and ranking info by gametype
CREATE VIEW TopPlayersByGameType AS
SELECT
  Player.player_id,
  Player.player_name,
  Player.username,
  Player.player_title,
  TopPlayers.gametype,
  TopPlayers.score,
  TopPlayers.rank
FROM Player
JOIN (
  SELECT
    leaderboardId,
    player_id,
    gametype,
    score,
    ROW_NUMBER() OVER (PARTITION BY gametype ORDER BY score DESC) AS rank
  FROM Leaderboard
) AS TopPlayers
ON Player.player_id = TopPlayers.player_id
WHERE TopPlayers.rank <= 10
ORDER BY TopPlayers.gametype, TopPlayers.rank;

-- Drop playerRank column from Leaderboard table
ALTER TABLE Leaderboard DROP COLUMN playerRank;


