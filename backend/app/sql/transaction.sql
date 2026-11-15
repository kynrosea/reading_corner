.mode box
.nullvalue NULL
PRAGMA foreign_keys=ON;

BEGIN TRANSACTION;

-- I chose to demonstrate multiple operations that one specific user may do when using the application
-- Each operation is directly relevant to using the database in a web or mobile application
-- I have chosen one specific user for all operations to demonstrate the rollback as well
-- The account deletion should NOT be permanent here

-- DELETE Operation
-- user wants to delete their account and all associated information
.print "\nBefore Account Deletion"
SELECT * FROM users
WHERE username = "itzzzYUNA";

SELECT * FROM user_books
WHERE username = "itzzzYUNA";


SELECT * FROM all_user_rewards
WHERE username = "itzzzYUNA";

SAVEPOINT before_account_deletion;

DELETE FROM users
WHERE username = "itzzzYUNA";

.print "\nAfter Account Deletion\nNothing should be outputted.\nAccount deletion now being rolled back...\n"
SELECT * FROM users
WHERE username = "itzzzYUNA";

SELECT * FROM user_books
WHERE username = "itzzzYUNA";

SELECT * FROM all_user_rewards
WHERE username = "itzzzYUNA";

SELECT * FROM user_library
WHERE user_id=5;

SELECT * FROM user_rewards
WHERE user_id=5;

SELECT * FROM reviews
WHERE user_id=5;


ROLLBACK TO before_account_deletion;

-- UPDATE Operation
-- user wants to change their profile visibility to public
.print "\nBefore updating profile visibility"
SELECT username, profile_visibility
FROM users
WHERE username="itzzzYUNA";

UPDATE users
SET profile_visibility="private"
WHERE username="itzzzYUNA";

.print "\nAfter updating profile visibility"
SELECT username, profile_visibility
FROM users
WHERE username="itzzzYUNA";

-- UPDATE Operation
-- update the reading status of a book in a user's personal collection (or user_library)
.print "\nBefore updating book status"
SELECT * FROM user_books
WHERE username = "itzzzYUNA" AND title="Beach Read";

UPDATE user_library
SET status = "read"
WHERE (user_id, book_id) = (
    SELECT user_id, book_id
    FROM user_books
    WHERE username = "itzzzYUNA" AND title = "Beach Read"
);

.print "\nAfter updating book status"
SELECT * FROM user_books
WHERE username = "itzzzYUNA" AND title="Beach Read";

-- INSERT Operation
-- directly connects to the previous operation
-- adding a review about the newly completed book
.print "\nBefore Inserting Review"
SELECT * FROM reviews
WHERE user_id=5;

INSERT INTO reviews
    (user_id, book_id, creation_date, review_text, rating)
VALUES
    (5, 8, "2026-11-03", "Such a cozy and introspective romance. Emily Henry is amazing!!", 5);

.print "\nAfter Inserting Review"
SELECT * FROM reviews
WHERE user_id=5;

-- UPSERT Operation
-- add a new reward to user account and update duplicate count if they've already obtained it
.print "\nBefore Reward update"
SELECT user_id, username, reward_id, duplicate_count
FROM all_user_rewards
WHERE user_id=5 AND reward_id=4;

INSERT INTO user_rewards
    (user_id, reward_id)
VALUES
    (5,4)
ON CONFLICT(user_id, reward_id)
DO UPDATE SET
    duplicate_count = duplicate_count + 1;

.print "\nAfter reward update"
SELECT user_id, username, reward_id, duplicate_count
FROM all_user_rewards
WHERE user_id=5 AND reward_id=4;


COMMIT;
