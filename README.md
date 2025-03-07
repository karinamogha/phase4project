Budget Tracker

Description

Budget Tracker is a full-stack web application designed to help users manage their personal finances efficiently. The application enables users to track their income, expenses, and savings through an intuitive interface. It features authentication, category-based spending analysis, and real-time updates, allowing users to stay on top of their financial goals.

Technologies Used

Frontend: React, React Router, React Hooks, CSS

Backend: Flask, Flask-RESTful, Flask-SQLAlchemy, Flask-Migrate

Database: SQLite

Other: Flask-CORS, SQLAlchemy-Serializer, Faker (for seeding data)

Installation and Setup

Prerequisites

Ensure you have the following installed on your system:

Python 3.x

Node.js & npm

Pipenv (for backend dependency management)

Cloning the Repository

git clone <repository-url>
cd budget-tracker

Backend Setup

Navigate to the server directory:

cd server

Install dependencies:

pipenv install

Activate virtual environment:

pipenv shell

Initialize and migrate the database:

flask db init
flask db upgrade head

(Optional) Seed the database with test data:

python seed.py

Start the Flask server:

python app.py

Frontend Setup

Navigate to the client directory:

cd client

Install dependencies:

npm install

Start the React application:

npm start

The frontend should now be running on http://localhost:3000 and the backend API on http://localhost:5555.

Directory Structure

.
├── client          # React frontend
│   ├── src        # React components & logic
│   ├── public     # Static assets
│   └── package.json  # Frontend dependencies
├── server         # Flask backend
│   ├── app.py     # Main Flask application
│   ├── config.py  # App configuration
│   ├── models.py  # Database models
│   ├── seed.py    # Script to seed test data
│   ├── migrations # Database migrations
│   └── instance   # SQLite database file
└── README.md      # Project documentation

API Routes

The backend provides RESTful API endpoints for managing transactions and user accounts.

Authentication

POST /register - Register a new user

POST /login - Authenticate user and return a token

Transactions

GET /transactions - Retrieve all transactions

POST /transactions - Add a new transaction

PUT /transactions/:id - Update an existing transaction

DELETE /transactions/:id - Remove a transaction

Budget Categories

GET /categories - Retrieve spending categories

POST /categories - Create a new category

Models

User: Stores user credentials and authentication data

Transaction: Stores transaction details (amount, category, date, description)

Category: Stores different spending categories

Features

✅ User authentication (sign-up & login)
✅ Add, update, and delete transactions
✅ Categorize expenses and incomes
✅ View total income, expenses, and savings
✅ Responsive UI for easy mobile and desktop access

Future Enhancements

Integration with external financial APIs for automatic transaction tracking

Graphical data visualization for spending trends

Export transactions as CSV or PDF

Multi-user support for shared budget management

License

This project is licensed under the MIT License.

Contributors

Karina Mogha - Developer

Contact

For questions or collaboration, reach out at moghakarina@gmail.com.

Happy Budgeting! 🚀
