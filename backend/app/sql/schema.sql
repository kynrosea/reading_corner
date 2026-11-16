PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;

DROP TABLE IF EXISTS user_library;
DROP TABLE IF EXISTS user_rewards;
DROP TABLE IF EXISTS reading_logs;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS book_tags;
DROP TABLE IF EXISTS user_preferences;
DROP TABLE IF EXISTS tags;
DROP TABLE IF EXISTS rewards;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS users;
DROP VIEW IF EXISTS user_books;
DROP VIEW IF EXISTS all_user_rewards;

-- need to include a view and index

CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT,
    email TEXT UNIQUE NOT NULL,
    birth_date TEXT NOT NULL,
    creation_date TEXT NOT NULL,
    leaf_balance INTEGER DEFAULT 0,
    profile_visibility TEXT DEFAULT "private"
);

CREATE TABLE books (
    book_id INTEGER PRIMARY KEY,
    author TEXT NOT NULL,
    title TEXT NOT NULL,
    publication_year INTEGER,
    synopsis TEXT,
    isbn TEXT,
    page_count INTEGER CHECK (page_count > 0),
    cover BLOB
);

CREATE TABLE rewards (
    reward_id INTEGER PRIMARY KEY,
    species TEXT NOT NULL,
    rarity TEXT NOT NULL,
    image BLOB,
    description TEXT
);

CREATE TABLE tags (
    tag_id INTEGER PRIMARY KEY,
    tag_name TEXT NOT NULL
);

CREATE TABLE book_tags (
    book_id INTEGER,
    tag_id INTEGER,

    PRIMARY KEY (book_id, tag_id),

    FOREIGN KEY (book_id)
        REFERENCES books(book_id),
    
    FOREIGN KEY (tag_id)
        REFERENCES tags(tag_id)
);

CREATE TABLE user_preferences (
    preference_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    tag_id INTEGER,
    does_like INTEGER, -- bool value represented by 1/0 ==> true/false

    FOREIGN KEY (user_id)
        REFERENCES users(user_id) ON DELETE CASCADE,

    FOREIGN KEY (tag_id)
        REFERENCES tags(tag_id)
);

CREATE TABLE reading_logs (
    log_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    book_id INTEGER,
    log_date TEXT NOT NULL,
    progress REAL DEFAULT 0 CHECK (progress >= 0 AND progress <= 100),
    notes TEXT,
    session_time REAL,

    FOREIGN KEY (user_id)
        REFERENCES users(user_id) ON DELETE CASCADE,

    FOREIGN KEY (book_id)
        REFERENCES books(book_id)
);

CREATE TABLE reviews (
    review_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    book_id INTEGER,
    creation_date TEXT NOT NULL,
    review_text TEXT,
    visibility TEXT NOT NULL DEFAULT "private",
    rating INTEGER NOT NULL CHECK (rating > 0 AND rating <= 5),

    FOREIGN KEY (user_id)
        REFERENCES users(user_id) ON DELETE CASCADE,

    FOREIGN KEY (book_id)
        REFERENCES books(book_id)
);

CREATE TABLE user_library (
    user_id INTEGER,
    book_id INTEGER,
    category TEXT,
    status TEXT NOT NULL,
    start_date TEXT,
    finished_date TEXT,

    PRIMARY KEY (user_id, book_id),

    FOREIGN KEY (user_id)
        REFERENCES users(user_id) ON DELETE CASCADE,
    
    FOREIGN KEY (book_id)
        REFERENCES books(book_id)

);

CREATE TABLE user_rewards (
    user_id INTEGER,
    reward_id INTEGER,
    duplicate_count INTEGER DEFAULT 0,

    PRIMARY KEY (user_id, reward_id),

    FOREIGN KEY (user_id)
        REFERENCES users(user_id) ON DELETE CASCADE,

    FOREIGN KEY (reward_id)
        REFERENCES rewards(reward_id)
);

-- view to see all books that user has in library with ids, names, and statuses
CREATE VIEW user_books AS
SELECT u.user_id,
        u.username,
        u.first_name,
        u.profile_visibility,
        b.book_id,
        b.author,
        b.title,
        ul.status
FROM users AS u
JOIN user_library AS ul
    ON u.user_id = ul.user_id
JOIN books AS b
    ON ul.book_id = b.book_id;

-- view to see all rewards user has with ides, names, and rarities
CREATE VIEW all_user_rewards AS
SELECT u.user_id,
        u.username,
        r.reward_id,
        r.species,
        r.rarity,
		r.image,
		r.description,
        ur.duplicate_count
FROM users AS u
JOIN user_rewards AS ur
    ON u.user_id = ur.user_id
JOIN rewards AS r
    ON ur.reward_id = r.reward_id;

-- creating index for user_id and book_id in reviews
CREATE INDEX idx_user_book_review
ON reviews (user_id, book_id);

-- creating index for user_id and book_id in reading_logs
CREATE INDEX idx_user_book_logs
ON reading_logs (user_id, book_id);

COMMIT;
