.mode box
.nullvalue NULL

-- Requirement 1: Filtering and Sorting
-- Shows all reviews where visibility is public and sort by rating in descending order
.print "\nAll Public Reviews\n------------------"
SELECT * FROM reviews
WHERE visibility="public"
ORDER BY rating DESC;


-- Requirement 1: Filtering and Sorting
-- Shows all reviews of a specific book where visibility is public
.print "\nAll Public Reviews of Books by Sarah J. Maas\n-------------------------------------"
SELECT u.username, b.title, b.author, r.review_text, r.rating FROM reviews AS r
JOIN users as u
    ON u.user_id = r.user_id
JOIN books AS b
    ON b.book_id = r.book_id
WHERE b.author = "Sarah J. Maas" AND visibility="public";


-- Requirement 1: Filtering and Sorting
-- Shows all reviews from a specific user
.print "\nReviews From Priya Patel\n-----------------------"
SELECT u.username, b.title, b.author, r.review_text, r.rating FROM reviews AS r
JOIN users AS u
    ON u.user_id = r.user_id
JOIN books AS b
    ON r.book_id = b.book_id
WHERE u.user_id = 8;


-- Requirement 2: INNER JOIN
-- Shows the username and reward info of users who have obtained rewards
.print "\nInner Join of User Rewards\n--------------------------"
SELECT u.username, r.species, r.rarity
FROM users AS u
INNER JOIN user_rewards AS ur
    ON u.user_id = ur.user_id
INNER JOIN rewards AS r
    ON ur.reward_id = r.reward_id;


-- Requirement 3: LEFT JOIN
-- Shows the username and reward info of all users, regardless of if they've obtained rewards
-- If no rewards were obtained, they will just have NULL values
.print "\nLeft Join of User Rewards\n-------------------------"
SELECT u.username, r.species, r.rarity
FROM users AS u
LEFT JOIN user_rewards AS ur
    ON u.user_id = ur.user_id
LEFT JOIN rewards AS r
    ON ur.reward_id = r.reward_id;


-- Requirement 3: LEFT JOIN
-- Useful for seeing a user's genre preferences. Can further be filtered by inividual user or genre.
.print "\nUser Preferences and Tag Names (Left Join)\n------------------------------------------"
SELECT u.username, t.tag_name,
    CASE
        WHEN up.does_like = 0 THEN "Dislikes"
        WHEN up.does_like = 1 THEN "Likes"
    END AS preference
FROM users AS u
LEFT JOIN user_preferences AS up
    ON u.user_id = up.user_id
LEFT JOIN tags AS t
    ON up.tag_id = t.tag_id;


-- Requirement 4: Three-Table Join
-- Shows all of the associated tags for a specific book by joining multiple tables (user_library, books, book_tags, and tags)
.print "\nDisplaying Tags for a Specific Book in User's Library\n-----------------------------------------------------"
SELECT b.title, t.tag_name, ul.category, ul.status
FROM user_library AS ul
JOIN books AS b
    ON ul.book_id = b.book_id
JOIN book_tags AS bt
    ON b.book_id = bt.book_id
JOIN tags AS t
    ON bt.tag_id = t.tag_id
WHERE ul.user_id = 5 AND b.title = "A Court of Thorns and Roses";


-- Requirement 5: Aggregate Query
-- Shows the total rewards collected by each user
.print "\nTotal Rewards Collected by Each User\n-------------------------------------------"
SELECT u.username, COUNT(*) AS "Rewards Collected"
FROM user_rewards as ur
JOIN users AS u
    ON u.user_id = ur.user_id
GROUP BY ur.user_id;


-- Requirement 6: GROUP BY and HAVING
-- Implements a leaderboard of sorts where the minimum requirement is to read at least 2 books within the current year
-- Shows all public users who have completed at least 2 books in the current year
.print "\nReading Leaderboard\n-------------------"
SELECT u.username, bc.books_completed AS "Books Completed in 2026"
FROM users as u
JOIN (
        SELECT user_id, COUNT(*) AS books_completed
        FROM user_library
        WHERE status = "read"
            AND finished_date IS NOT NULL
            AND (finished_date >= "2026-01-01" AND finished_date <= "2026-12-31")
        GROUP BY user_id
        HAVING books_completed >= 2
    ) AS bc
    ON u.user_id = bc.user_id
WHERE u.profile_visibility = "public"
ORDER BY bc.books_completed DESC;


-- Requirement 7: Subquery
-- Displays all books written by a certain author in a specific user's library
-- Useful for filtering user's library when you only want to look at books you've read, are reading, or want to read by a specific author.
.print "\nDisplaying All Books by a Certain Author in a Specific User's Library (itzzzYUNA and Emily Henry in this example)\n----------------------------------------"
SELECT b.title, ul.status, b.publication_year, b.page_count
FROM books AS b
JOIN user_library AS ul
    ON b.book_id = ul.book_id
JOIN users AS u
    ON ul.user_id = u.user_id
WHERE (
    b.book_id IN (
        SELECT book_id FROM books
        WHERE author = "Emily Henry"
    )

    AND

    u.user_id = (
        SELECT user_id FROM users
        WHERE username = "itzzzYUNA"
    )
);


-- Requirement 8: Set Operation
-- Shows the intersection between book tags and all tags
-- Helpful during the setup process so when the user picks their preferences,
-- they can pick tags that are available in the current curation of books in the DB.
.print "\nAvailable Tags\n---------------------------"
WITH tags_intersection AS (
    SELECT tag_id FROM tags
    INTERSECT
    SELECT tag_id FROM book_tags
)

SELECT t.tag_name FROM tags AS t
JOIN tags_intersection AS ti
    ON ti.tag_id = t.tag_id;


-- Requirement 9: View
-- Using the user_books views made in schema to display books that users with a public profile are currently reading.
-- This is useful for the social aspect of the application where users can be inspired by what others are reading and get indirect recommendations.
.print "\nWhat Public Users are Currently Reading\n---------------------------------------"
SELECT * FROM user_books
WHERE (status = "currently reading") AND (profile_visibility = "public");