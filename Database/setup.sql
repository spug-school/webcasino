DROP DATABASE IF EXISTS `cli_casino`;
CREATE DATABASE `cli_casino`;
USE `cli_casino`;

ALTER DATABASE `cli_casino` CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

-- Tables
CREATE TABLE `users` (
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `username` VARCHAR(25) NOT NULL UNIQUE,
  `password` VARCHAR(255) NOT NULL,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `user_statistics` (
  `user_id` INTEGER PRIMARY KEY,
  `balance` INTEGER DEFAULT 1000,
  `total_winnings` INTEGER DEFAULT 0,
  `games_played` INTEGER DEFAULT 0,
  `games_won` INTEGER DEFAULT 0,
  `games_lost` INTEGER DEFAULT 0,
  `is_banned` BOOLEAN DEFAULT 0,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `game_types` (
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `name` VARCHAR(50) NOT NULL UNIQUE,
  `rules` TEXT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `game_history` (
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `bet` INTEGER,
  `win_amount` INTEGER,
  `played_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `user_id` INTEGER NOT NULL,
  `game_type_id` INTEGER NOT NULL,
  FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  FOREIGN KEY (`game_type_id`) REFERENCES `game_types` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Indexes
CREATE INDEX idx_user_id_history ON `game_history` (`user_id`);
CREATE INDEX idx_game_id_history ON `game_history` (`game_type_id`);

-- Table population
INSERT INTO `game_types` 
  (`name`, `rules`)
VALUES
  (`Ventti`, 'TODO'),
  (`Nopanheitto`, 'Pelaaja valitsee itse, kuinka suurta noppaa heittää. Pelaajan tulee sitten arvata nopan oikea silmäluku.'),
  (`Slots`, 'TODO'),
  (`Ruletti`, 'TODO');


-- Test data TODO remove
-- Insert test data into `users` table
INSERT INTO `users` (`username`, `password`)
VALUES
('admin', 'password'),
('john_doe', 'P@ssw0rd123'),
('jane_smith', 'S3cur3P@ss'),
('alice_jones', 'Al1c3J0n3s!'),
('bob_brown', 'B0bBr0wn#'),
('charlie_davis', 'Ch@rl13D@v!s'),
('david_clark', 'D@v1dCl@rk$'),
('emily_miller', 'Em1lyM!ll3r'),
('frank_wilson', 'Fr@nkW1ls0n'),
('grace_lee', 'Gr@c3L33!'),
('henry_moore', 'H3nryM00r3'),
('isabella_taylor', 'Is@b3ll@T@yl0r'),
('jack_anderson', 'J@ckAnd3rs0n'),
('karen_thomas', 'K@r3nTh0m@s'),
('larry_martin', 'L@rryM@rt1n'),
('maria_white', 'M@r1@Wh1t3'),
('nancy_harris', 'N@nc7H@rr1s'),
('oliver_clark', '0l1v3rCl@rk'),
('paula_roberts', 'P@ul@R0b3rts'),
('quentin_walker', 'Qu3nt1nW@lk3r'),
('rachel_hall', 'R@ch3lH@ll!');

-- Insert test data into `user_statistics` table
INSERT INTO `user_statistics` (`user_id`, `balance`, `total_winnings`, `games_played`, `games_won`, `games_lost`, `is_banned`)
VALUES
(1, 1000, 500, 10, 5, 5, 0),
(2, 2000, 1500, 20, 15, 5, 0),
(3, 3000, 2500, 30, 25, 5, 0),
(4, 4000, 3500, 40, 35, 5, 0),
(5, 5000, 4500, 50, 45, 5, 0),
(6, 6000, 5500, 60, 55, 5, 0),
(7, 7000, 6500, 70, 65, 5, 0),
(8, 8000, 7500, 80, 75, 5, 0),
(9, 9000, 8500, 90, 85, 5, 0),
(10, 10000, 9500, 100, 95, 5, 0),
(11, 11000, 10500, 110, 105, 5, 0),
(12, 12000, 11500, 120, 115, 5, 0),
(13, 13000, 12500, 130, 125, 5, 0),
(14, 14000, 13500, 140, 135, 5, 0),
(15, 15000, 14500, 150, 145, 5, 0),
(16, 16000, 15500, 160, 155, 5, 0),
(17, 17000, 16500, 170, 165, 5, 0),
(18, 18000, 17500, 180, 175, 5, 0),
(19, 19000, 18500, 190, 185, 5, 0),
(20, 20000, 19500, 200, 195, 5, 0);

-- Insert test data into `game_types` table
INSERT INTO `game_types` (`name`, `description`)
VALUES
('Dice', 'A simple dice game'),
('Blackjack', 'A classic card game'),
('Roulette', 'A popular casino game'),
('Poker', 'A strategic card game'),
('Slots', 'A slot machine game'),
('Baccarat', 'A comparing card game'),
('Craps', 'A dice game'),
('Keno', 'A lottery-like game'),
('Bingo', 'A number matching game'),
('Sic Bo', 'A Chinese dice game');

-- Insert test data into `active_games` table
INSERT INTO `active_games` (`game_type_id`, `user_id`)
VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6),
(7, 7),
(8, 8),
(9, 9),
(10, 10),
(1, 11),
(2, 12),
(3, 13),
(4, 14),
(5, 15),
(6, 16),
(7, 17),
(8, 18),
(9, 19),
(10, 20);

-- Insert test data into `game_history` table
INSERT INTO `game_history` (`bet`, `win_amount`, `user_id`, `game_id`)
VALUES
(100, 200, 1, 1),
(200, 400, 2, 2),
(300, 600, 3, 3),
(400, 800, 4, 4),
(500, 1000, 5, 5),
(600, 1200, 6, 6),
(700, 1400, 7, 7),
(800, 1600, 8, 8),
(900, 1800, 9, 9),
(1000, 2000, 10, 10),
(1100, 2200, 11, 11),
(1200, 2400, 12, 12),
(1300, 2600, 13, 13),
(1400, 2800, 14, 14),
(1500, 3000, 15, 15),
(1600, 3200, 16, 16),
(1700, 3400, 17, 17),
(1800, 3600, 18, 18),
(1900, 3800, 19, 19),
(2000, 4000, 20, 20);