📝 Blog Management System

A simple yet powerful Blog Management System built with Flask that allows users to create, read, update, and delete (CRUD) blog posts. The system includes user authentication using sessions, and a comment section where readers can share their thoughts on posts.

🚀 Features

✅ User Authentication

Login and Logout using Flask sessions

Only logged-in users can create, edit, or delete blogs

✅ CRUD Operations

Create, Read, Update, and Delete blog posts

Display all blogs on the homepage with author details

✅ Comment System

Readers can post comments under each blog

Comments are stored in the database and linked to specific posts

✅ Session Management

Secure session handling to manage user states

Prevents unauthorized access to protected routes

✅ Responsive Design (Optional)

Clean, minimal UI for an intuitive user experience

🧱 Tech Stack
Component	Technology
Backend	Flask (Python)
Database	SQLite
ORM	SQLAlchemy
Frontend	HTML, CSS, Jinja2 Templates
Authentication	Flask Sessions
📁 Project Structure
Blog-Management-System/
│
├── static/                 # CSS, JS, and static assets
├── templates/              # HTML templates (home, login, post, etc.)
├── app.py                  # Main Flask application file
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation

⚙️ Installation & Setup

Follow these steps to run the project locally 👇

1️⃣ Clone the Repository
git clone https://github.com/<your-username>/Blog-Management-System.git
cd Blog-Management-System

2️⃣ Create a Virtual Environment
python -m venv venv
source venv/bin/activate      # For Mac/Linux
venv\Scripts\activate         # For Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

Run the Application
python app.py

🧠 How It Works

Users can sign up or log in.

Authenticated users can add new blog posts.

Anyone can read blogs and post comments.

Logged-in users can edit or delete their own posts.

The system uses sessions to keep users logged in.

🗃️ Database Design

Tables:

users → stores user credentials and profile info

blogs → stores blog title, content, author, and timestamps

comments → stores comments linked to blog posts

🧩 Future Improvements

🔹 Add image upload for blogs
🔹 Add profile pictures for users
🔹 Integrate like/dislike feature for posts
🔹 Implement pagination for blogs and comments

3️⃣ Install Dependencies
pip install -r requirements.txt
