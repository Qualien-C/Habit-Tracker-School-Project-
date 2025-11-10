# Habit-Tracker-School-Project 📝
The Personal Task and Habit Tracker is a simple Python and MySQL project that helps users record, manage, and track their daily habits. It allows users to sign up, log in, add, edit, or delete habits, and mark them as completed, storing all data in a MySQL database.

Follow the instructions

1) Run the following code in MySQL command line

CREATE DATABASE habit_tracker;
USE habit_tracker;

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(50) NOT NULL
);

CREATE TABLE habits (
    habit_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    habit_name VARCHAR(100),
    category VARCHAR(50),
    frequency VARCHAR(20),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE habit_log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    habit_id INT,
    date DATE,
    status BOOLEAN,
    FOREIGN KEY (habit_id) REFERENCES habits(habit_id) ON DELETE CASCADE
);

2) Change the password in `main.py` to the user's MySQL password.
