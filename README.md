# Reading Corner

## Project Overview
This web application simulates a reading tracker where a user can add books to their personal collection, browse books in the database, receive rewards, and more to encourage building better reading habits. For the final submission, I tried to implement at least one logical function for each table in my database to simulate a real reading tracking application. I want to demonstrate a truly functionable application.
## Testing Note
The signup feature is fully functioning, but if you want to see an account with pre-filled data to view all reports and functionalities, then please use the following log in details.
- Email: itzy_yuna@yahoo.com
- Username: itzzzYUNA
## Languages and Frameworks Used
- Frontend: React, TypeScript, Vite
- Backend: Python, Flask
- Database: SQLite

## Requirements
- Python: 3.12.3
- Node.js: 24.11.9
- Required Python packages: [requirements.txt](requirements.txt)
- Required TypeScript packages: [package-lock.json](frontend/package-lock.json)

## Installation and Setup
### Environment Setup
- Clone this repository: `git clone https://github.com/kynrosea/reading_corner.git`
- Make sure you move into project root directory: `cd reading_corner`
- Create virtual environment (if not using one already): `python3 -m venv .venv`
- Activate virtual environment: `source .venv/bin/activate`
### Install Dependencies
- Install backend dependencies: `pip install -r requirements.txt`
- Install root dependencies: `npm install`
- Install frontend dependencies: `npm --prefix frontend install`
### Database Setup
- In the root project directory, run the bash script to build the database: `bash backend/build_db.sh`
- This does not perform any queries. This ensures that we are working with the same schema and data to replicate environment and results.

## Run Instructions
### With run.sh script
- I created a script that performs the setup, installation, and running of the application for you. You would only need to follow the instructions in the [Environment Setup Section](#environment-setup). Then, run the following command: `bash run.sh`
### Manually
- If you'd prefer to do the steps of installation and setup yourself, just follow all instructions in the [Installation and Setup section](#installation-and-setup). Then, once the setup is complete, do this command to run the application: `npm run dev`
- Note: I am using Concurrently to run the backend and frontend at the same time without having to type in separate commands. `npm run dev` handles running both without any additional commands.
### Access the App
- You can access the application through this link: [Reading Corner App](http://localhost:5173)
- The full frontend URL is http://localhost:5173
- The full backend URL is http://localhost:5000
## Required Database Operations
### Search or Browse Data
- User can browse books and search for books based on the title and/or author. Any and all matching results will appear on the page. If no results match, then a message relaying that information will appear on the page.
- User can log in to an existing account based on their username and email. I thought about changing the database to add a password function, but due to time constraints, I opted to keep it simple even though it's not very secure.
### Display Related Data
- When viewing a user's personal library, the application displays the status of that book from user_library, the title and author from books, and reading logs associated with each book, if any. If you are in the test user account provided, then view reading logs for 'A Court of Frost and Starlight' by Sarah J. Maas to see real data.
- You can filter books based on genres that the user prefers using the tags in user_preferences and tags in all available book tags.
- A user can view all reviews that they've made in their personal library.
### Add Data
- A user can add a book to the book table, if needed.
- A user can add an existing book to their library.
- A user can signup, which adds a user to the users table in the database.
- A user can add new preferences to user_preferences upon signup or through profile settings.
- A user can add a new review about a book in their personal library.
### Update or Delete Data
- A user can update their first name, last name, or profile visibility through profile settings.
- A user can update their genre preferences. As mentioned before, a user can add a preference, but they can also delete preferences from user_preferences. By deselecting a tag on the page, that tag associated with the user will be removed from user_preferences.
- A user can update the status of a book from user_library. This can be manipulated to receive more leaves for reward wishing, but that is a limitation that was not worth implementing for this submission. If you mark the status of a book as finished, it will automatically set the finished_date as the current day's date. Due to not wanting to spend too much additional time on styling and rendering, I chose to not add a separate feature to manually input the finished date.
### Summary or Report
- A user can view a leaderboard that displays all users with a public profile who have read at least 2 books in 2026. This utilizes an aggregate function, join, subquery, and group by to display these results.
- This is not as intricate, but when viewing one's personal library, a user can see how many books in their library (user_library), how many books they're currently reading, and how many books they've finished. This updates in real time as you change statuses on the page.
### Additional Meaningful Operations
- When viewing all of the rewards a user has, they can make a wish if they have enough leaves (the currency of the app). If they don't have enough leaves, then that option will not be available. However, if they do, then, through multiple SQL statements, a random reward will be obtained and displayed. If this reward was a duplicate, then the duplicate count of that reward will increase upon each insertion attempt. This is treated as a complete transaction. 

## Database Configuration
- There is no separate database configuration.
- The database file is stored in the backend directory, but the database initialization is taken care of in the build_db.sh script.
- Other than the previously mentioned setup requirements, there are no additional configurations.

## Notes
- Reading Corner uses SQLite as its primary persistent data storage.
- Database operations are performed through the Flask backend using SQL.
- There is a couple of assumptions and limitations in this application
    - Assumption: There are not many, if any, books with duplicate titles and authors.
    - Limitation: User can manipulate the reward system by switching between statuses.
    - Limitation: When updating status, the finished_date is automatically assumed as the current date.
