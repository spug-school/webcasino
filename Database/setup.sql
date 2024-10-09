DROP DATABASE IF EXISTS `cli_casino`;
CREATE DATABASE `cli_casino` CHARACTER SET `utf8mb4` COLLATE `utf8mb4_unicode_ci`;
USE `cli_casino`;

-- Tables
CREATE TABLE `users` (
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `username` VARCHAR(25) NOT NULL UNIQUE,
  `password` VARCHAR(255) NOT NULL,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARACTER SET `utf8mb4` COLLATE `utf8mb4_unicode_ci`;

CREATE TABLE `user_statistics` (
  `user_id` INTEGER PRIMARY KEY,
  `balance` INTEGER DEFAULT 1000,
  `total_winnings` INTEGER DEFAULT 0,
  `games_played` INTEGER DEFAULT 0,
  `games_won` INTEGER DEFAULT 0,
  `games_lost` INTEGER DEFAULT 0,
  `is_banned` BOOLEAN DEFAULT 0,
  FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARACTER SET `utf8mb4` COLLATE `utf8mb4_unicode_ci`;

CREATE TABLE `game_types` (
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `name` VARCHAR(50) NOT NULL UNIQUE,
  `name_en` VARCHAR(50) NOT NULL UNIQUE,
  `rules` TEXT
) ENGINE=InnoDB DEFAULT CHARACTER SET `utf8mb4` COLLATE `utf8mb4_unicode_ci`;

CREATE TABLE `game_history` (
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `bet` INTEGER,
  `win_amount` INTEGER,
  `played_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `user_id` INTEGER NOT NULL,
  `game_type_id` INTEGER NOT NULL,
  FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  FOREIGN KEY (`game_type_id`) REFERENCES `game_types` (`id`)
) ENGINE=InnoDB DEFAULT CHARACTER SET `utf8mb4` COLLATE `utf8mb4_unicode_ci`;

-- Indexes
CREATE INDEX idx_user_id_history ON `game_history` (`user_id`);
CREATE INDEX idx_game_id_history ON `game_history` (`game_type_id`);

-- Game types
INSERT INTO `game_types` 
  (`name`, `name_en`, `rules`)
VALUES
  ('nopanheitto', 'dice', 'Pelaaja valitsee itse, kuinka suurta noppaa heittää. Pelaajan tulee sitten arvata nopan oikea silmäluku.\n\n- Voittokerroin on silmälukujen lukumäärä'),
  ('ruletti', 'roulette', 'Pelaaja arvaa värin sekä halutessaan kahta numeroa. Pelaaja asettaa jokaiselle arvaukselle (väri sekä numerot) oman erillisen panoksensa.\n\n- Numeroarvauksen voittokerroin = 36x\n- Väriarvauksen = 2x'),
  ('ventti', 'twentyone', 'Pelaaja saa kaksi korttia, joista toinen on piilotettu. Pelaaja voi joko jäädä tai ottaa lisää kortteja. Tavoitteena on saada korttien summa mahdollisimman lähelle 21:ä, mutta ei yli. Pelaaja voittaa, jos hänen korttiensa summa on suurempi kuin jakajan korttien summa, mutta ei yli 21:ä.\n\n- Voittokerroin = 2x'),
  ('hedelmäpeli', 'slots', 'Pelaaja asettaa panoksen ja painaa pelinappia. Pelissä on 4 rullaa, joissa on erilaisia symboleja. Jos rullat pysähtyvät samoihin symboleihin, pelaaja voittaa.\n\nPyöräytyksen hinta: 10 pistettä\n\nVoittokertoimet:\n- 3 samaa symbolia = 5x\n- 4 samaa symbolia = 25x'),
  ('kolikonheitto', 'coinflip', 'Pelaaja valitsee joko kruunan tai klaavan. Jos pelaaja arvaa oikein, hän voittaa.\n\n- Voittokerroin = 2x');

-- Insert admin on setup
INSERT INTO `users` (`id`, `username`, `password`)
VALUES
-- password is 'password' in sha256
(1, 'admin', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8');

INSERT INTO `user_statistics` (`user_id`, `balance`)
VALUES
(1, 99999999);
