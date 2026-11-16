# Reading Corner

## Project Overview
This web application simulates a reading tracker where a user can add books to their personal collection, browse books in the database, receive rewards, and more to encourage building better reading habits. For this current submission, There are only a few key operations implemented, which will we be touched on later.

## Technologies
- Frontend: React, TypeScripts, Vite
- Backend: Python, Flask
- Database: SQLite

## Requirements
- Python: 3.12.7
- Node.js: 24.11.9
- Required Python packages: [requirements.txt](requirements.txt)
- Required JavaScript packages: [package.json](frontend/package.json)

## Installation and Setup
### Database Setup
- In the root project directory, run the bash script to build the database: `bash backend/build_db.sh`
- This does not perform any queries. This ensures that we are working with the same schema and data to replicate environment and results.
### Backend Setup
- Create or activate virtual environment: `source .venv/bin/activate`
- Install dependencies: `pip -r install requirements.txt`
- Run Flask in a separate terminal window from the frontend: `flask run`
### Frontend Setup
- Install JavaScript dependencies: `npm install`
- In separate terminal window from the backend, start the Vite dev server: `npm run dev`
### Access the App
- You can access the application through this link: http://localhost:5173
## Required Database Operations
| Operation | Application Feature |
|---|---|
| Search or browse | Browse and search available books |
| Display related data | View a personal library using related book and user data |
| Add data | Add a book to database |
| Update or delete | Change a book's reading status |
| Summary or report | View the leaderboard |
| Additional operation | Spend leaves to receive a butterfly reward |

## Notes

- Reading Corner uses SQLite as its primary persistent data store.
- Database operations are performed through the Flask backend using SQL.
- [Document any relevant assumptions or known limitations.]
