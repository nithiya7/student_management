import mysql.connector
from mysql.connector import IntegrityError

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',       # Replace with your MySQL username
    'password': 'nithiya',   # Replace with your MySQL password
    'database': 'student_db'
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def add_student():
    name = input("Enter student name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return
    age_input = input("Enter age: ").strip()
    try:
        age = int(age_input)
    except ValueError:
        print("Invalid age.")
        return
    grade = input("Enter grade (e.g. A, B): ").strip().upper()
    email = input("Enter email: ").strip()

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'INSERT INTO students (name, age, grade, email) VALUES (%s, %s, %s, %s)',
            (name, age, grade, email)
        )
        conn.commit()
        print("Student added successfully.")
    except IntegrityError:
        print("Error: Email must be unique.")
    finally:
        cursor.close()
        conn.close()

def view_students():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, age, grade, email FROM students ORDER BY name')
    rows = cursor.fetchall()
    if rows:
        print("\nStudents List:")
        print(f"{'ID':<3} {'Name':<20} {'Age':<4} {'Grade':<6} {'Email'}")
        print("-"*50)
        for r in rows:
            print(f"{r[0]:<3} {r[1]:<20} {r[2]:<4} {r[3]:<6} {r[4]}")
    else:
        print("No students found.")
    cursor.close()
    conn.close()

def update_student():
    try:
        id_input = int(input("Enter student ID to update: ").strip())
    except ValueError:
        print("Invalid ID.")
        return
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT name, age, grade, email FROM students WHERE id=%s', (id_input,))
    student = cursor.fetchone()
    if not student:
        print("Student not found.")
        cursor.close()
        conn.close()
        return

    print(f"Current - Name: {student[0]}, Age: {student[1]}, Grade: {student[2]}, Email: {student[3]}")
    new_name = input("New name (leave blank to keep): ").strip() or student[0]
    new_age_input = input("New age (leave blank to keep): ").strip()
    new_grade = input("New grade (leave blank to keep): ").strip().upper() or student[2]
    new_email = input("New email (leave blank to keep): ").strip() or student[3]

    try:
        new_age = int(new_age_input) if new_age_input else student[1]
    except ValueError:
        new_age = student[1]

    try:
        cursor.execute('''
            UPDATE students SET name=%s, age=%s, grade=%s, email=%s WHERE id=%s
        ''', (new_name, new_age, new_grade, new_email, id_input))
        conn.commit()
        print("Student updated.")
    except IntegrityError:
        print("Error: Email must be unique.")
    finally:
        cursor.close()
        conn.close()

def delete_student():
    try:
        id_input = int(input("Enter student ID to delete: ").strip())
    except ValueError:
        print("Invalid ID.")
        return
    confirm = input("Are you sure you want to delete this student? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Cancelled.")
        return
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM students WHERE id=%s', (id_input,))
    conn.commit()
    if cursor.rowcount:
        print("Student deleted.")
    else:
        print("Student not found.")
    cursor.close()
    conn.close()

def menu():
    print("""
==== Student Management ====
1. Add student
2. View students
3. Update student
4. Delete student
5. Exit
""")

def main():
    while True:
        menu()
        choice = input("Enter choice (1-5): ").strip()
        if choice == '1':
            add_student()
        elif choice == '2':
            view_students()
        elif choice == '3':
            update_student()
        elif choice == '4':
            delete_student()
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
