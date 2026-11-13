# Assignment 3 -3005

Python application that connects to a PostgreSQL students table
and performs create, read, update, and delete operations.

## Video Demo
[PASTE YOUR YOUTUBE/VIMEO LINK HERE]


## Project Structure
```
Assignment 3 -3005/
├── database/
│   └── init.sql          # Schema and initial data
├── app/
│   ├── db.py             # Database connection
│   ├── main.py           # CRUD functions and menu for demo
│   └── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## Setup

### 1. Create the database
Open pgAdmin and create a database called `3005`:    
```sql
CREATE DATABASE 3005;
```

### 2. Load the schema and initial data
```bash
psql -U postgres -d student_db -f database/init.sql
```

### 3. Set up Python environment
```bash
cd app
python -m venv venv

# Windows (Git Bash):
source venv/Scripts/activate
# Windows (PowerShell):
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 4. Configure credentials
Create a file named .env in the project root with the following contents, replacing your_password with your real PostgreSQL password:

DB_HOST=localhost
DB_PORT=5432
DB_NAME=student_db
DB_USER=postgres
DB_PASSWORD=your_password

### 5. Run
```bash
python main.py
```

## Functions


`getAllStudents()` uses SELECT in SQL and prints all students 
`addStudent(fn, ln, email, date)` uses INSERT in SQL and adds a new student 
`updateStudentEmail(id, email)` uses UPDATE in SQL and changes a student's email 
`deleteStudent(id)` uses DELETE in SQL and removes a student 

## Verifying changes in pgAdmin
After any write operation:
1. Right-click the `students` table
2. Click **Refresh**
3. Confirm the change appears

