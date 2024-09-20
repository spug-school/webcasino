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
  `username` VARCHAR(50),
  `password` VARCHAR(255),
  `total_winnings` INTEGER,
  `games_played` INTEGER,
  `games_won` INTEGER,
  `games_lost` INTEGER,
  `is_banned` BOOLEAN
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `balance` (
  `balance` INTEGER,
  `user_id` INTEGER
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

ALTER TABLE `balance` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `game_history` ADD FOREIGN KEY (`user`) REFERENCES `users` (`id`);

ALTER TABLE `game_history` ADD FOREIGN KEY (`game`) REFERENCES `games` (`id`);


-- Test data 
-- TODO: remove this
INSERT INTO `users`
    (`username`, `password`, `total_winnings`, `games_played`, `games_won`, `games_lost`, `is_banned`)
VALUES
    ('pekkapelaaja', '$2y$10$3Z6', 12, 29, 2, 27, 0),
    ('ismolaitela69', 'salasana', 0, 200, 0, 200, 1);