# Flask Blog App

## Introduction

This is a simple Flask web application for managing users, posts, likes, and comments. Users can register, log in, create posts, like/unlike posts, and add comments.

## Features

- User Registration: Users can register with a unique username, email, and password.
- User Authentication: Secure user authentication using Flask-Login.
- Post Management: Users can create, read, update, and delete their posts.
- Likes: Users can like/unlike posts, and the number of likes is tracked for each post.
- Comments: Users can add comments to posts, and each comment has the user who posted it, the comment text, and a timestamp.

## Technologies Used

- Flask: Micro web framework for Python.
- SQLAlchemy: SQL toolkit and Object-Relational Mapping (ORM) for Python.
- Flask-Login: User session management.
- etc.

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/nitin1994C/Flask_Blog_app.git

2.pip install -r requirements.txt
3.flask db init
flask db migrate -m "Initial migration"
flask db upgrade

4.flask run
The app will be accessible at http://127.0.0.1:5000/ in your web browser.

