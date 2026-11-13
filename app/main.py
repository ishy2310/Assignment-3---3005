
from datetime import datetime
from psycopg2 import errors
from db import get_connection


def getAllStudents():
    """SELECT every student and print them in a readable table."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT student_id, first_name, last_name, email, enrollment_date
                    FROM students
                    ORDER BY student_id;
                """)
                rows = cur.fetchall()

                if not rows:
                    print("\n(No students in database.)\n")
                    return

                print("\n" + "-" * 92)
                print(f"{'ID':<5}{'First':<14}{'Last':<14}{'Email':<34}{'Enrolled'}")
                print("-" * 92)
                for r in rows:
                    print(f"{r[0]:<5}{r[1]:<14}{r[2]:<14}{r[3]:<34}{r[4]}")
                print("-" * 92 + "\n")
    except Exception as e:
        print(f"[ERROR] getAllStudents: {e}")


def addStudent(first_name, last_name, email, enrollment_date):
    """INSERT a new student. enrollment_date must be YYYY-MM-DD."""
    try:
    
        datetime.strptime(enrollment_date, "%Y-%m-%d")

        with get_connection() as conn:
            with conn.cursor() as cur:
              
                cur.execute("""
                    INSERT INTO students (first_name, last_name, email, enrollment_date)
                    VALUES (%s, %s, %s, %s)
                    RETURNING student_id;
                """, (first_name, last_name, email, enrollment_date))
                new_id = cur.fetchone()[0]
                conn.commit()
                print(f"[OK] Added student #{new_id}: {first_name} {last_name}")
    except errors.UniqueViolation:
        print(f"[ERROR] Email '{email}' already exists.")
    except ValueError:
        print("[ERROR] Date must be YYYY-MM-DD (e.g. 2023-09-15).")
    except Exception as e:
        print(f"[ERROR] addStudent: {e}")



def updateStudentEmail(student_id, new_email):
    """Change a student's email."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE students SET email = %s WHERE student_id = %s;",
                    (new_email, student_id),
                )
                if cur.rowcount == 0:
                    print(f"[ERROR] No student with ID {student_id}.")
                else:
                    conn.commit()
                    print(f"[OK] Updated email for student #{student_id} -> {new_email}")
    except errors.UniqueViolation:
        print(f"[ERROR] Email '{new_email}' is already in use.")
    except Exception as e:
        print(f"[ERROR] updateStudentEmail: {e}")



def deleteStudent(student_id):
    """Remove the student with the given ID."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM students WHERE student_id = %s;",
                    (student_id,),
                )
                if cur.rowcount == 0:
                    print(f"[ERROR] No student with ID {student_id}.")
                else:
                    conn.commit()
                    print(f"[OK] Deleted student #{student_id}.")
    except Exception as e:
        print(f"[ERROR] deleteStudent: {e}")



# Interactive menu to use during demo
def main():
    menu = """
====== Student CRUD ======
 1. List all students
 2. Add a student
 3. Update a student's email
 4. Delete a student
 5. Exit
==========================
"""
    while True:
        print(menu)
        choice = input("Choice (1-5): ").strip()

        if choice == "1":
            getAllStudents()
        elif choice == "2":
            fn = input("First name: ").strip()
            ln = input("Last name: ").strip()
            em = input("Email: ").strip()
            dt = input("Enrollment date (YYYY-MM-DD): ").strip()
            addStudent(fn, ln, em, dt)
        elif choice == "3":
            try:
                sid = int(input("Student ID: ").strip())
                em = input("New email: ").strip()
                updateStudentEmail(sid, em)
            except ValueError:
                print("[ERROR] Student ID must be a number.")
        elif choice == "4":
            try:
                sid = int(input("Student ID: ").strip())
                if input(f"Delete #{sid}? (y/n): ").strip().lower() == "y":
                    deleteStudent(sid)
                else:
                    print("Cancelled.")
            except ValueError:
                print("[ERROR] Student ID must be a number.")
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()