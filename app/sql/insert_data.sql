PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;

-- Inserting data into users table
INSERT INTO users 
    (user_id, username, first_name, last_name, email, birth_date, creation_date, leaf_balance, profile_visibility)
VALUES
    (1,'tvd_elena','Elena','Gilbert','e_gilbert@gmail.com','1992-06-22','2026-10-20',50,'private'),
    (2,'missjday','Jessica','Day','jess_loves_apples@yahoo.com','1982-02-13','2026-10-22',0,'private'),
    (3,'brainiac3000','Spencer','Reid','dr_reid_bau@gmail.com','1981-10-12','2026-09-17',0,'private'),
    (4,'not_the_flash','Barry','Allen','not_the_flash@gmail.com','1989-03-14','2026-02-11',162,'private'),
    (5,'itzzzYUNA','Yuna','Shin','itzy_yuna@yahoo.com','2003-12-09','2026-07-22',546,'public'),
    (6,'mchen','Maya','Chen','maya.chen@testmail.com','1998-04-16','2026-10-25',85,'private'),
    (7,'itznoah','Noah','Bennett','noah.bennett@testmail.com','1995-11-02','2026-10-25',24,'public'),
    (8,'pripri45','Priya','Patel','priya.patel@testmail.com','2001-07-28','2026-10-26',310,'private'),
    (9,'martinezzzz','Lucas','Martinez','lucas.martinez@testmail.com','1999-01-09','2026-10-27',12,'public'),
    (10,'avelovesbooks','Avery','Brooks','avery.brooks@testmail.com','2002-05-31','2026-10-27',190,'private'),
    (11,'missninapark','Nina','Park','nina.park@testmail.com','1997-09-14','2026-10-28',73,'private'),
    (12,'ellgreen17','Elliot','Green','elliot.green@testmail.com','1993-12-03','2026-10-28',441,'private'),
    (13,'lil_miss_soso','Sofia','Rivera','sofia.rivera@testmail.com','2000-03-22','2026-10-29',58,'public'),
    (14,'theo_the_great','Theo','Morgan','theo.morgan@testmail.com','1996-08-11','2026-10-30',0,'public'),
    (15,'queen_amara','Amara','Lewis','amara.lewis@testmail.com','2003-02-19','2026-10-31',127,'private');

-- Inserting data into books table
INSERT INTO books 
    (book_id, author, title, publication_year, synopsis, isbn, page_count, cover)
VALUES
    (1,'Sarah J. Maas','A Court of Thorns and Roses',2015,'When nineteen-year-old huntress Feyre kills a wolf in the woods, a terrifying beast arrives to demand retribution. Dragged to a treacherous, magical land she only knows from legends, Feyre learns her captor isn''t a monster, but Tamlin,”a lethal, immortal faerie lord. As an ancient, wicked shadow grows over his kingdom, Feyre''s feelings for Tamlin turn from icy hatred to fire, and she must fight to break a curse that threatens to destroy his world,”and hers.','9781635575569',448,''),
    (2,'Sarah J. Maas','A Court of Mist and Fury',2016,'Feyre survived Under the Mountain, but the nightmare left her soul in shattered pieces. Trapped in a gilded cage at the Spring Court, she is forced to pay the price of her freedom: one week every month with Rhysand, the mysterious and feared High Lord of the Night Court. Navigating a web of dark politics and intoxicating temptation, Feyre must harness her terrifying new powers and decide where her true allegiance,”and heart,”belongs.','9781635575576',640,''),
    (3,'Sarah J. Maas','A Court of Wings and Ruin',2017,'War is coming, and the fate of Prythian hangs in the balance. Stepping into the heart of deceit, Feyre plays a deadly game of espionage within the Spring Court to tear down the King of Hybern from the inside. But time is running out. To save her home, her friends, and her mate, Feyre must forge impossible alliances and prepare to pay the ultimate price on a blood-soaked battlefield.','9781635575606',736,''),
    (4,'Sarah J. Maas','A Court of Frost and Starlight',2018,'The war is over, but the wounds are far from healed. As the Winter Solstice approaches, Feyre, Rhysand, and their Inner Circle gather to celebrate, rebuild, and attempt to move forward. But lingering ghosts, unsettled hearts, and the scars of war threaten to throw their hard-won peace back into chaos.','9781635575620',272,''),
    (5,'Sarah J. Maas','A Court of Silver Flames',2021,'Nesta Archeron is angry at the world, her fate, and most of all, herself. Forced into the deadly, intoxicating world of the Fae, she wants nothing to do with her new life,”or with Cassian, the battle-scarred warrior whose presence infuriates her as much as it ignites her desire. But when a treacherous threat arises, Nesta and Cassian must train together to conquer their own inner demons before a terrible new evil claims them all.','9781635575637',768,''),
    (6,'George Orwell','1984',1949,'In a nightmare vision of total surveillance, Oceania rules every action, every breath, and every thought. Winston Smith is a low-level propaganda clerk who commits the ultimate sin: he remembers the truth. When he begins a forbidden love affair in secret, Winston embarks on a dangerous path of resistance against a terrifying regime that will stop at nothing to erase his humanity.','9780451524935',328,''),
    (7,'Emily Henry','Happy Place',2023,'Harriet and Wyn were the perfect couple,”until they broke up five months ago and never told their best friends. Now, back at their favorite Maine cottage for their group''s annual reunion, they find out the house is being sold. Desperate not to ruin the last magical week together, Harriet and Wyn agree to pretend they''re still madly in love. How hard can it be to fake it for seven days in front of the people who know them best?','9780593441275',400,''),
    (8,'Emily Henry','Beach Read',2020,'Augustus is a literary snob who only writes dark tragedy. January is a hopeless romantic who writes glowing bestsellers. Both are broke, hopelessly stuck with writer''s block, and living in neighboring beach houses for the summer. To break their slumps, they strike a bet: January will write the Next Great American Novel, Augustus will write a rom-com, and whoever publishes first wins. But as their summer field trips turn into something deeper, they realize their story might not go according to plan.','9781984806734',384,''),
    (9,'Alex Michaelides','The Silent Patient',2019,'Alicia Berenson''s life seems perfect. A famous painter married to an in-demand fashion photographer, she lives in a grand house overlooking a park. Then one evening, she shoots her husband five times in the face and never speaks another word. Theo Faber, a criminal psychotherapist, has waited years for the chance to treat her. His search for the truth leads him down a dark, twisting path that threatens to consume him entirely.','9781250301697',336,''),
    (10,'Jessica Goodman','They Wish They Were Us',2020,'At Gold Coast''s elite Prep, the Players rule everything. Three years ago, high school senior Jill Newman''s best friend was murdered, and the case was closed with a swift confession. Now, in her senior year, secret texts emerge hinting that the wrong person might be taking the fall. As Jill digs deeper into the dark underbelly of her school''s secret society, she uncovers secrets that could destroy everything she''s built.','9780593114292',336,''),
    (11,'Lena Hart','The Glass Orchard',2024,'A young botanist inherits an abandoned greenhouse and uncovers a family mystery hidden among its rare plants.','9900000000011',352,''),
    (12,'Marcus Vale','Signal at Dusk',2022,'A communications engineer begins receiving impossible radio messages that seem to predict events one day ahead.','9900000000012',416,''),
    (13,'Iris Monroe','A Map of Small Goodbyes',2021,'Three estranged siblings return home and piece together their mother''s unfinished travel journal.','9900000000013',304,''),
    (14,'Daniel Cho','The Last Archive',2025,'An archivist discovers that records from an entire decade are quietly disappearing from a city''s public database.','9900000000014',388,''),
    (15,'Mina Reyes','Summer on Bellweather Lane',2023,'Two former childhood friends reunite while renovating neighboring houses during one unusually eventful summer.','9900000000015',336,''),
    (16,'Owen Price','Under a Paper Moon',2020,'A stage magician and a skeptical journalist investigate a string of impossible disappearances.','9900000000016',372,''),
    (17,'Camille Foster','The Quiet Between Stars',2024,'A deep-space research crew loses contact with Earth and must decide whether a mysterious signal is a warning or an invitation.','9900000000017',448,''),
    (18,'Rowan Blake','Ashes in the Wallpaper',2019,'A graduate student renting an old house finds handwritten messages appearing beneath layers of wallpaper.','9900000000018',320,''),
    (19,'June Holloway','Second Draft Hearts',2025,'Two rival editors are assigned to rescue the same troubled romance manuscript before publication.','9900000000019',344,''),
    (20,'Elias Grant','The Memory Garden',2022,'A caretaker at a secluded estate discovers flowers that seem connected to memories their visitors have forgotten.','9900000000020',400,''),
    (21,'Tessa Nguyen','The Borrowed Year',2021,'A woman agrees to live by a late friend''s unfinished list of goals for one year.','9900000000021',288,''),
    (22,'Jonah Wells','Northbound',2018,'A stranded traveler joins a winter train journey where every passenger appears to be hiding something.','9900000000022',360,''),
    (23,'Ada Mercer','Notes from Room 314',2023,'A resident assistant starts cataloging strange notes left behind in an empty dorm room.','9900000000023',296,''),
    (24,'Harper Sloan','How to Begin Again',2024,'A practical guide to rebuilding routines after a major life transition using small, repeatable habits.','9900000000024',240,''),
    (25,'Felix Arden','The City Beneath the Lake',2025,'During a drought, the ruins of a flooded town emerge and reveal a decades-old disappearance.','9900000000025',432,'');

-- Inserting data into rewards table
INSERT INTO rewards 
    (reward_id, species, rarity, image, description)
VALUES
    (1,'monarch','common','',''),
    (2,'queen','common','',''),
    (3,'black swallowtail','common','',''),
    (4,'painted lady','uncommon','',''),
    (5,'peacock','uncommon','',''),
    (6,'blue morpho','rare','',''),
    (7,'kaiser-i-hind','rare','',''),
    (8,'glasswing','common','','A translucent-wing butterfly collectible.'),
    (9,'red admiral','common','','A bold red-and-black butterfly collectible.'),
    (10,'ulysses','uncommon','','A vivid blue butterfly collectible.'),
    (11,'apollo','uncommon','','A pale mountain butterfly collectible.'),
    (12,'madagascan sunset moth','rare','','A jewel-toned rare collectible.');
    
-- Inserting data into tags table
INSERT INTO tags
    (tag_id, tag_name)
VALUES
    (1,'fantasy'),
    (2,'romance'),
    (3,'fiction'),
    (4,'nonfiction'),
    (5,'self-help'),
    (6,'classic'),
    (7,'romantasy'),
    (8,'mystery'),
    (9,'thriller'),
    (10,'literary fiction'),
    (11,'contemporary fiction'),
    (12,'dystopian'),
    (13,'science fiction'),
    (14,'horror'),
    (15,'historical fiction'),
    (16,'young adult');

-- Inserting data into book_tags table
INSERT INTO book_tags
    (book_id, tag_id)
VALUES
    (1,1),
    (1,2),
    (1,7),
    (2,1),
    (2,2),
    (2,7),
    (3,1),
    (3,2),
    (3,7),
    (4,1),
    (4,2),
    (4,7),
    (5,1),
    (5,2),
    (5,7),
    (6,6),
    (6,12),
    (7,2),
    (7,3),
    (8,2),
    (8,3),
    (9,8),
    (10,8),
    (11,3),
    (11,8),
    (12,3),
    (12,9),
    (12,13),
    (13,3),
    (13,10),
    (14,3),
    (14,8),
    (14,9),
    (15,2),
    (15,11),
    (16,3),
    (16,8),
    (16,9),
    (17,3),
    (17,13),
    (18,3),
    (18,14),
    (19,2),
    (19,11),
    (20,1),
    (20,3),
    (20,10),
    (21,3),
    (21,11),
    (22,3),
    (22,8),
    (22,9),
    (23,3),
    (23,8),
    (23,16),
    (24,4),
    (24,5),
    (25,1),
    (25,8),
    (25,9);

-- Inserting data into user_preferences table
INSERT INTO user_preferences 
    (preference_id, user_id, tag_id, does_like)
VALUES
    (1,1,2,1),
    (2,1,1,1),
    (3,5,1,1),
    (4,5,2,1),
    (5,5,4,0),
    (6,6,8,1),
    (7,6,10,1),
    (8,6,14,0),
    (9,7,13,1),
    (10,7,9,1),
    (11,7,2,0),
    (12,8,2,1),
    (13,8,11,1),
    (14,8,14,0),
    (15,9,14,1),
    (16,9,9,1),
    (17,9,5,0),
    (18,10,10,1),
    (19,10,11,1),
    (20,10,9,0),
    (21,11,8,1),
    (22,11,14,1),
    (23,12,13,1),
    (24,12,1,1),
    (25,13,10,1),
    (26,13,2,1),
    (27,14,8,1),
    (28,14,3,1),
    (29,15,2,1),
    (30,15,16,1);

-- Inserting data into reading_logs table
INSERT INTO reading_logs
    (log_id, user_id, book_id, log_date, progress, notes, session_time)
VALUES
    (1,5,4,'2026-08-20',50.0,'',''),
    (2,5,4,'2026-08-28',92.0,'',''),
    (3,4,6,'2026-05-15',17.0,'',''),
    (4,4,6,'2026-05-20',73.0,'',''),
    (5,6,14,'2026-10-28',8.0,'Started after dinner.',24.0),
    (6,6,14,'2026-10-30',31.0,'The mystery is picking up.',47.0),
    (7,6,14,'2026-11-01',54.0,'',38.0),
    (8,7,17,'2026-10-30',12.0,'Interesting opening.',30.0),
    (9,7,17,'2026-11-01',37.0,'',55.0),
    (10,8,20,'2026-10-24',15.0,'',35.0),
    (11,8,20,'2026-10-27',42.0,'Love the atmosphere.',52.0),
    (12,8,20,'2026-11-01',68.0,'',61.0),
    (13,9,22,'2026-10-29',10.0,'',20.0),
    (14,9,22,'2026-10-31',44.0,'Suspicious of everyone.',49.0),
    (15,10,24,'2026-10-27',20.0,'Trying the first exercise.',28.0),
    (16,10,24,'2026-10-30',58.0,'',41.0),
    (17,11,23,'2026-10-31',16.0,'Very eerie.',26.0),
    (18,12,25,'2026-10-20',9.0,'',22.0),
    (19,12,25,'2026-10-24',35.0,'',44.0),
    (20,12,25,'2026-10-29',71.0,'Big reveal.',63.0),
    (21,14,14,'2026-10-30',14.0,'',25.0),
    (22,14,14,'2026-11-01',39.0,'Good pacing.',46.0),
    (23,15,23,'2026-10-25',11.0,'',19.0),
    (24,15,23,'2026-10-29',48.0,'The notes are getting stranger.',51.0),
    (25,15,23,'2026-11-01',76.0,'',58.0);

-- Inserting data into reviews table
INSERT INTO reviews 
    (review_id, user_id, book_id, creation_date, review_text, visibility, rating)
VALUES
    (1,1,2,'2026-10-21','','public',5),
    (2,5,4,'2026-08-29','','private',4),
    (3,5,5,'2026-09-18','','private',4),
    (4,5,7,'2026-10-02','','private',5),
    (5,4,6,'2026-05-23','','public',5),
    (6,6,11,'2026-09-18','A gentle mystery with a cozy setting and a satisfying ending.','public',4),
    (7,7,12,'2026-10-17','Fast-paced and clever. I liked the central idea more than the ending.','public',4),
    (8,8,15,'2026-08-20','Sweet, easy to read, and exactly what I wanted from a summer romance.','public',5),
    (9,8,19,'2026-09-17','The banter worked for me and the publishing setting was fun.','private',4),
    (10,9,18,'2026-10-10','Creepy without being too graphic. The house was the best part.','public',4),
    (11,10,13,'2026-07-15','Quiet and reflective, with strong family dynamics.','public',5),
    (12,10,21,'2026-09-09','A thoughtful premise, though the middle dragged a little.','private',3),
    (13,11,16,'2026-09-03','A fun mystery with an old-fashioned theatrical feel.','public',4),
    (14,12,17,'2026-06-14','The isolation and uncertainty made this one hard to put down.','public',5),
    (15,13,11,'2026-09-21','Atmospheric and surprisingly emotional.','private',4),
    (16,13,15,'2026-10-11','Warm, funny, and easy to finish in a weekend.','public',4),
    (17,15,19,'2026-09-22','A very cute workplace romance with great dialogue.','public',5);

-- Inserting data into user_library table
INSERT INTO user_library 
    (user_id, book_id, category, status, start_date, finished_date)
VALUES
    (5,1,'personal','read','2026-02-27','2026-03-10'),
    (5,2,'personal','read','2026-03-26','2026-04-19'),
    (5,3,'personal','read','2026-05-01','2026-05-23'),
    (5,4,'personal','read','','2026-06-12'),
    (5,5,'personal','read','','2026-06-30'),
    (5,7,'personal','read','','2025-09-21'),
    (5,8,'','currently reading','',''),
    (1,2,'personal','read','',''),
    (1,3,'','currently reading','',''),
    (4,6,'','read','',''),
    (6,11,'personal','read','2026-09-05','2026-09-17'),
    (6,14,'personal','currently reading','2026-10-28',''),
    (6,19,'wishlist','want to read','',''),
    (7,12,'personal','read','2026-10-01','2026-10-16'),
    (7,17,'personal','currently reading','2026-10-30',''),
    (7,24,'wishlist','want to read','',''),
    (8,15,'personal','read','2026-08-11','2026-08-19'),
    (8,19,'personal','read','2026-09-10','2026-09-16'),
    (8,20,'personal','currently reading','2026-10-24',''),
    (9,18,'personal','read','2026-10-02','2026-10-09'),
    (9,22,'personal','currently reading','2026-10-29',''),
    (10,13,'personal','read','2026-07-06','2026-07-14'),
    (10,21,'personal','read','2026-09-03','2026-09-08'),
    (10,24,'personal','currently reading','2026-10-27',''),
    (11,16,'personal','read','2026-08-25','2026-09-02'),
    (11,23,'personal','currently reading','2026-10-31',''),
    (12,17,'personal','read','2026-06-01','2026-06-13'),
    (12,25,'personal','currently reading','2026-10-20',''),
    (13,11,'personal','read','2026-09-12','2026-09-20'),
    (13,15,'personal','read','2026-10-03','2026-10-10'),
    (14,14,'personal','currently reading','2026-10-30',''),
    (14,18,'wishlist','want to read','',''),
    (15,19,'personal','read','2026-09-15','2026-09-21'),
    (15,23,'personal','currently reading','2026-10-25','');

-- Inserting data into user_rewards table
INSERT INTO user_rewards 
    (user_id, reward_id, duplicate_count)
VALUES
    (1,1,0),
    (5,1,0),
    (5,4,0),
    (4,3,0),
    (4,1,0),
    (3,2,0),
    (6,8,0),
    (6,1,1),
    (7,9,0),
    (8,10,2),
    (8,4,0),
    (10,11,0),
    (10,2,1),
    (11,3,0),
    (12,12,0),
    (12,6,1),
    (13,9,0),
    (14,8,2),
    (15,10,0),
    (15,5,0);
    
COMMIT;
