# Week 7: Secure Authentication System
Student Name: [Lakshana Dunessur] 
Student ID: [M01093418]
Course: CST1510 -CW2 - Multi-Domain Intelligence Platform
## Project Description
A command-line authentication system implementing secure password hashing
This system allows users to register accounts and log in with proper pass
## Features
- Secure password hashing using bcrypt with automatic salt generation
- User registration with duplicate username prevention
- - User login with password verification
- Input validation for usernames and passwords
- File-based user data persistence
## Technical Implementation
- Hashing Algorithm: bcrypt with automatic salting
- Data Storage: Plain text file (`users.txt`) with comma-separated values
- Password Security: One-way hashing, no plaintext storage
- Validation: Username (3-20 alphanumeric characters), Password (6-50 characters)


# WEEK 8: Data Pipeline & CRUD (SQL)

## Project Description
In Week 8, the project was extended to include a relational database-backed data pipeline using SQLite.
The focus was on database schema design, secure SQL operations, and full CRUD functionality across multiple domains while preventing SQL injection.

## Features 
- Relational Databases and SQL
- SQLite database management
- Schema design and normalisation
- Secure database access using parameterised queries
- Full CRUD lifecycle (Create, Read, Update, Delete)

## Technical Implementation
- Schema Design (users, cyber_incidents, datasets_metadata, it_tickets)
- Data migration : Read user credentials from 'users.txt'
- Insert data into SQLite users table
- Preserved hashed passwords without exposing plaintext

## WEEK 9: 
In Week 9, the project was transformed into a web-based application using Streamlit.
The focus was on application architecture, session state management, multi-page navigation, and interactive data visualisation.

## Features
- Streamlit fundamentals
- Web application architecture
- Session state management
- Multi-page application design

## Technical Implementation
- Framework: Streamlit
- Visualisation libraries: Plotly
- Data source: SQLite database
- Integration: Connection between authentication, CRUD operations and analytics.