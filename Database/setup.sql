DROP DATABASE IF EXISTS `cli_casino`;
CREATE DATABASE `cli_casino`;
USE `cli_casino`;

ALTER DATABASE `cli_casino` CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

-- Tables
CREATE TABLE `games` (
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `name` VARCHAR(20),
  `rules` text,
  `player` INTEGER
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `users` (
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `username` VARCHAR(25),
  `password` VARCHAR(255),
  `balance` INTEGER DEFAULT 1000,
  `total_winnings` INTEGER DEFAULT 0,
  `games_played` INTEGER DEFAULT 0,
  `games_won` INTEGER DEFAULT 0,
  `games_lost` INTEGER DEFAULT 0,
  `is_banned` BOOLEAN DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `game_history` (
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `user` INTEGER,
  `game` INTEGER,
  `bet` INTEGER,
  `win_amount` INTEGER,
  `played_at` DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Foreign keys
ALTER TABLE `games` ADD FOREIGN KEY (`player`) REFERENCES `users` (`id`);

ALTER TABLE `game_history` ADD FOREIGN KEY (`user`) REFERENCES `users` (`id`);

ALTER TABLE `game_history` ADD FOREIGN KEY (`game`) REFERENCES `games` (`id`);


-- Test data 
-- TODO: remove this
INSERT INTO `users`
    (`username`, `balance`, `total_winnings`, `games_played`, `games_won`, `games_lost`, `is_banned`)
VALUES
    ('pekkapelaaja', 5122, 12, 29, 2, 27, 0),
    ('ismolaitela69', 1000, 0, 200, 0, 200, 1);