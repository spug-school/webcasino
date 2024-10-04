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


INSERT INTO `users` 
  (`username`, `password`, `balance`, `total_winnings`, `games_played`, `games_won`, `games_lost`, `is_banned`) 
VALUES
  ('admin', 'admin123', 10000, 0, 0, 0, 0, 0),
  ('alice', 'alice123', 1200, 500, 10, 5, 5, 0),
  ('bob', 'bob123', 800, 200, 8, 3, 5, 0),
  ('charlie', 'charlie123', 1500, 700, 15, 10, 5, 0),
  ('david', 'david123', 500, 100, 5, 2, 3, 0),
  ('eve', 'eve123', 1000, 300, 12, 6, 6, 0),
  ('frank', 'frank123', 2000, 1000, 20, 15, 5, 0),
  ('grace', 'grace123', 300, 50, 3, 1, 2, 0),
  ('hannah', 'hannah123', 2500, 1200, 25, 20, 5, 0),
  ('ivan', 'ivan123', 700, 150, 7, 3, 4, 0),
  ('judy', 'judy123', 1800, 900, 18, 12, 6, 0),
  ('karen', 'karen123', 900, 250, 9, 4, 5, 0),
  ('leo', 'leo123', 1600, 800, 16, 11, 5, 0),
  ('mike', 'mike123', 400, 75, 4, 2, 2, 0),
  ('nina', 'nina123', 2200, 1100, 22, 17, 5, 0),
  ('oliver', 'oliver123', 600, 125, 6, 3, 3, 0),
  ('paula', 'paula123', 1400, 700, 14, 9, 5, 0),
  ('quinn', 'quinn123', 100, 25, 1, 0, 1, 0),
  ('rachel', 'rachel123', 2400, 1150, 24, 19, 5, 0),
  ('steve', 'steve123', 500, 100, 5, 2, 3, 0),
  ('tina', 'tina123', 2000, 950, 20, 14, 6, 0),
  ('ursula', 'ursula123', 800, 200, 8, 4, 4, 0),
  ('victor', 'victor123', 1800, 850, 18, 13, 5, 0),
  ('wendy', 'wendy123', 300, 50, 3, 1, 2, 0),
  ('xander', 'xander123', 2600, 1250, 26, 21, 5, 0),
  ('yvonne', 'yvonne123', 700, 150, 7, 3, 4, 0);