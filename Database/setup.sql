DROP DATABASE IF EXISTS `cli_casino`;
CREATE DATABASE `cli_casino` CHARACTER SET `utf8mb4` COLLATE `utf8mb4_unicode_ci`;
USE `cli_casino`;

-- Tables
CREATE TABLE `users` (
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `username` VARCHAR(25) NOT NULL UNIQUE,
  `password` VARCHAR(255) NOT NULL,
  `hidden` BOOLEAN DEFAULT 0, -- we want some users to be hidden (like admin)
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE `user_statistics` (
  `user_id` INTEGER PRIMARY KEY,
  `balance` INTEGER DEFAULT 1000,
  `total_winnings` INTEGER DEFAULT 0,
  `games_played` INTEGER DEFAULT 0,
  `games_won` INTEGER DEFAULT 0,
  `games_lost` INTEGER DEFAULT 0,
  `is_banned` BOOLEAN DEFAULT 0,
  FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
);

CREATE TABLE `game_types` (
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `name` VARCHAR(50) NOT NULL UNIQUE,
  `name_en` VARCHAR(50) NOT NULL UNIQUE,
  `rules` TEXT
);

CREATE TABLE `game_history` (
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `bet` INTEGER,
  `win_amount` INTEGER,
  `played_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `user_id` INTEGER NOT NULL,
  `game_type_id` INTEGER NOT NULL,
  FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  FOREIGN KEY (`game_type_id`) REFERENCES `game_types` (`id`)
);

-- Indexes
-- CREATE INDEX idx_user_id_history ON `game_history` (`user_id`);
-- CREATE INDEX idx_game_id_history ON `game_history` (`game_type_id`);

-- Game types
INSERT INTO `game_types` 
  (`name`, `name_en`, `rules`)
VALUES
  ('nopanheitto', 'dice', 'Pelissä heitetään pelaajan valitsemaa määrää noppia. Pelaaja arvaa, mikä nopanheiton summa on.\n\n- Voittokerroin = noppien määrä'),
  ('ruletti', 'roulette', 'Pelaaja arvaa värin sekä halutessaan kahta numeroa. Pelaaja asettaa jokaiselle arvaukselle (väri sekä numerot) oman erillisen panoksensa.\n\n- Numeroarvauksen voittokerroin = 36x\n- Väriarvauksen = 2x'),
  ('ventti', 'twentyone', 'Pelaaja ja jakaja saavat alussa kaksi korttia. Pelaaja aloittaa. Pelaaja voi joko jäädä tai ottaa lisää kortteja. Tavoitteena on saada korttien summa mahdollisimman lähelle 21:ä, mutta ei yli. Pelaaja voittaa, jos hänen korttiensa summa on suurempi kuin jakajan korttien summa, mutta ei yli 21:ä. Jos pelaajan ja jakajan kädet ovat yhtä suuret, jakaja voittaa.\n\n- Voittokerroin = 2x'),
  ('hedelmäpeli', 'slots', 'Pelaaja asettaa panoksen ja painaa pelinappia. Pelissä on 4 rullaa, joissa on erilaisia symboleja. Jos rullat pysähtyvät samoihin symboleihin, pelaaja voittaa.\n\nPyöräytyksen hinta: 100 pistettä\n\nVoittokertoimet:\n- 2 samaa symbolia = 1.25x\n- 3 samaa symbolia = 5x\n- 4 samaa symbolia = 25x'),
  ('kolikonheitto', 'coinflip', 'Pelaaja valitsee joko kruunan tai klaavan. Jos pelaaja arvaa oikein, hän voittaa.\n\n- Voittokerroin = 2x');

-- Insert admin on setup
INSERT INTO `users` (`username`, `password`, `hidden`)
VALUES
-- password is 'password' in sha256
('admin', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 1);
INSERT INTO `user_statistics` (`user_id`, `balance`)
VALUES
(1, 99999999);
