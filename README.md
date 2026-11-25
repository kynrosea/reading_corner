# Reading Corner

## Project Overview
This web application simulates a reading tracker where a user can add books to their personal collection, browse books in the database, receive rewards, and more to encourage building better reading habits. For this current submission, There are only a few key operations implemented, which will we be touched on later.
## Testing Note
The signup feature is fully functioning, but if you want to see an account with pre-filled data to view all reports and functionalities, then please use the following log in details.
- Email: itzy_yuna@yahoo.com
- Username: itzzzYUNA
## Languages and Frameworks Used
- Frontend: React, TypeScript, Vite
- Backend: Python, Flask
- Database: SQLite

## Requirements
- Python: 3.12.7
- Node.js: 24.11.9
- Required Python packages: [requirements.txt](requirements.txt)
- Required TypeScript packages: [package-lock.json](frontend/package-lock.json)

## Installation and Setup
### Environment Setup
- Clone this repository: `git clone https://github.com/kynrosea/reading_corner.git`
- Make sure you move into project root directory: `cd reading_corner`
- Create virtual environment (if not using one already): `python3 -m venv .venv`
- Activate virtual environment: `source .venv/bin/activate`
- Install backend dependencies: `pip install -r requirements.txt`
- Install root dependencies: `npm install`
- Install frontend dependencies: `npm --prefix frontend install`
### Database Setup
- In the root project directory, run the bash script to build the database: `bash backend/build_db.sh`
- This does not perform any queries. This ensures that we are working with the same schema and data to replicate environment and results.

## Run Instructions
### With run.sh script
- I created a script that performs the setup, installation, and running of the application for you. You still to activate virtual environment though.
    - `python3 -m venv .venv`
    - `source .venv/bin/activate`
    - `bash run.sh`
### Manually
- If you'd prefer to do the steps of installation and setup yourself, just follow those instructions in that [section](#installation-and-setup). Then, once the setup is complete, do this command to run the application: `npm run dev`
- Note: I am using Concurrently to run the backend and frontend at the same time without having to type in separate commands. `npm run dev` handles running both without any additional commands.
### Access the App
- You can access the application through this link: [Reading Corner App](http://localhost:5173)
- The full frontend URL is http://localhost:5173
- The full backend URL is http://localhost:5000
## Required Database Operations
### Search or Browse Data
User is able to browse books and search for books based on the title and/or author. Any and all matching results will appear on the page. If no results match, then a message relaying that information will appear on the page.
### Display Related Data
When viewing a user's personal library, the application is displaying the status of that book from user_library, the title and author from books, and persistent data across pages from logged in user to access primary key that returns personal information.
### Add Data
A user can add a book to the book table if the one they're searching for is not already in the database. I am running into errors rendering the signup function for a user, but the backend operation does work. You can view it at the backend endpoints.
### Update or Delete Data
A user can delete a book from the database if they accidentally added the wrong book. This was meant to be in the form of an undo button, but for time's sake, it is an open delete button. This is obviously not the most secure operation for a web application, but for the purposes of this project, it demonstrates the idea. \
Additionally, a user can update their reading status when viewing books in their personal library.
### Summary or Report
A user can view a leaderboard that displays all users with a public profile who have read at least 2 books in 2026. This utilizes an aggregate function, join, subquery, and group by to display these results.
### Additional Meaningful Operation
When viewing all of the rewards a user has, they can make a wish if they have enough leaves (the currency of the app). If they don't have enough leaves, then that option will not be available. However, if they do, then, through multiple SQL statements, a random reward will be obtained and displayed. If this reward was a duplicate, then the duplicate count of that reward will increase upon each insertion attempt. This is treated as a complete transaction.

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
