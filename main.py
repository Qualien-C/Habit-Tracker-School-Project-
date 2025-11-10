import mysql.connector
from tabulate import tabulate
import datetime
import sys

# DATABASE CONNECTION

def connect_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",            
            password="CHANGE IT TO YOUR MYSQL PASSWORD", # DON'T FORGET!!
            database="habit_tracker"
        )
    except mysql.connector.Error as err:
        print(f"❌ Database connection failed: {err}")
        sys.exit()

# USER AUTHENTICATION

def signup():
    print("\n========= SIGNUP =========")
    username = input("Enter new username: ")
    password = input("Enter new password (visible): ")

    try:
        mydb = connect_db()
        mycursor = mydb.cursor()
        mycursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        mydb.commit()
        print("✅ Account created successfully! You can now log in.")
    except mysql.connector.IntegrityError:
        print("⚠️ Username already exists! Try another one.")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        mydb.close()

def login():
    print("\n========= LOGIN =========")
    username = input("Enter username: ")
    password = input("Enter password (visible): ")

    try:
        mydb = connect_db()
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = mycursor.fetchone()
        if user:
            print(f"✅ Welcome back, {username}!")
            habit_menu(user[0], username)
        else:
            print("❌ Invalid username or password.")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        mydb.close()

# HABIT TRACKER MENU

def habit_menu(user_id, username):
    while True:
        print(f"\n===== {username.upper()}'S HABIT TRACKER =====")
        print("1. Add New Habit")
        print("2. View Habits")
        print("3. Edit Habit")
        print("4. Delete Habit")
        print("5. Mark Habit as Done")
        print("6. View Progress")
        print("7. Export Data")
        print("8. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_habit(user_id)
        elif choice == "2":
            view_habits(user_id)
        elif choice == "3":
            edit_habit(user_id)
        elif choice == "4":
            delete_habit(user_id)
        elif choice == "5":
            mark_habit_done(user_id)
        elif choice == "6":
            view_progress(user_id)
        elif choice == "7":
            export_data(user_id, username)
        elif choice == "8":
            print("👋 Logging out...\n")
            break
        else:
            print("⚠️ Invalid choice, try again.")

# ADD NEW HABIT

def add_habit(user_id):
    print("\n========= ADD NEW HABIT =========")
    name = input("Enter habit name: ")
    category = input("Enter category (e.g., Health, Study, Productivity): ")
    frequency = input("Enter frequency (daily/weekly/monthly): ")

    try:
        mydb = connect_db()
        mycursor = mydb.cursor()
        mycursor.execute(
            "INSERT INTO habits (user_id, habit_name, category, frequency) VALUES (%s, %s, %s, %s)",
            (user_id, name, category, frequency)
        )
        mydb.commit()
        print(f"✅ Habit '{name}' added successfully!")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        mydb.close()

# VIEW HABITS

def view_habits(user_id):
    print("\n========= YOUR HABITS =========")
    try:
        mydb = connect_db()
        mycursor = mydb.cursor()
        mycursor.execute("SELECT habit_id, habit_name, category, frequency FROM habits WHERE user_id=%s", (user_id,))
        rows = mycursor.fetchall()

        if not rows:
            print("No habits found.")
            return

        table = tabulate(rows, headers=["ID", "Habit Name", "Category", "Frequency"], tablefmt="fancy_grid")
        print(table)
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        mydb.close()

# EDIT HABIT

def edit_habit(user_id):
    view_habits(user_id)
    habit_id = input("Enter Habit ID to edit: ")
    print("Leave blank if you don't want to change a field.")

    new_name = input("New habit name: ")
    new_category = input("New category: ")
    new_frequency = input("New frequency: ")

    try:
        mydb = connect_db()
        mycursor = mydb.cursor()

        query = "UPDATE habits SET "
        updates = []
        values = []

        if new_name:
            updates.append("habit_name=%s")
            values.append(new_name)
        if new_category:
            updates.append("category=%s")
            values.append(new_category)
        if new_frequency:
            updates.append("frequency=%s")
            values.append(new_frequency)

        if updates:
            query += ", ".join(updates) + " WHERE habit_id=%s AND user_id=%s"
            values.extend([habit_id, user_id])
            mycursor.execute(query, tuple(values))
            mydb.commit()
            print("✅ Habit updated successfully!")
        else:
            print("⚠️ No changes made.")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        mydb.close()

# DELETE HABIT

def delete_habit(user_id):
    view_habits(user_id)
    habit_id = input("Enter Habit ID to delete: ")

    try:
        mydb = connect_db()
        mycursor = mydb.cursor()
        mycursor.execute("DELETE FROM habits WHERE habit_id=%s AND user_id=%s", (habit_id, user_id))
        mydb.commit()

        if mycursor.rowcount > 0:
            print("✅ Habit deleted successfully!")
        else:
            print("⚠️ Invalid Habit ID.")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        mydb.close()

# MARK HABIT AS DONE

def mark_habit_done(user_id):
    view_habits(user_id)
    habit_id = input("Enter Habit ID to mark as done: ")

    today = datetime.date.today()

    try:
        mydb = connect_db()
        mycursor = mydb.cursor()

        mycursor.execute(
            "INSERT INTO habit_log (habit_id, date, status) VALUES (%s, %s, %s)",
            (habit_id, today, True)
        )
        mydb.commit()
        print("✅ Habit marked as done for today!")
    except mysql.connector.errors.IntegrityError:
        print("⚠️ Already marked as done today!")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        mydb.close()

# VIEW PROGRESS

def view_progress(user_id):
    print("\n========= HABIT PROGRESS =========")
    try:
        mydb = connect_db()
        mycursor = mydb.cursor()
        mycursor.execute("SELECT habit_id, habit_name FROM habits WHERE user_id=%s", (user_id,))
        habits = mycursor.fetchall()

        if not habits:
            print("No habits found.")
            return

        for habit in habits:
            habit_id, name = habit
            mycursor.execute("SELECT COUNT(*) FROM habit_log WHERE habit_id=%s", (habit_id,))
            count = mycursor.fetchone()[0]
            mycursor.execute("SELECT MAX(date) FROM habit_log WHERE habit_id=%s", (habit_id,))
            last_done = mycursor.fetchone()[0]
            print(f"\n🧩 {name}: {count} completions | Last done: {last_done}")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        mydb.close()

# EXPORT DATA TO FILE

def export_data(user_id, username):
    try:
        mydb = connect_db()
        mycursor = mydb.cursor()
        mycursor.execute(
            "SELECT h.habit_name, h.category, h.frequency, l.date, l.status "
            "FROM habits h LEFT JOIN habit_log l ON h.habit_id = l.habit_id "
            "WHERE h.user_id=%s ORDER BY h.habit_id, l.date",
            (user_id,)
        )
        data = mycursor.fetchall()

        if not data:
            print("⚠️ No data to export.")
            return

        filename = f"{username}_habits_report.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"===== {username.upper()}'S HABIT REPORT =====\n\n")
            f.write(tabulate(data, headers=["Habit", "Category", "Frequency", "Date", "Status"], tablefmt="grid"))
        print(f"✅ Data exported successfully to '{filename}'")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        mydb.close()

# MAIN MENU

def main_menu():
    while True:
        print("\n========= PERSONAL TASK & HABIT TRACKER =========")
        print("1. Signup")
        print("2. Login")
        print("3. Exit")
        print("===============================================")
        choice = input("Enter choice: ")

        if choice == "1":
            signup()
        elif choice == "2":
            login()
        elif choice == "3":
            print("👋 Goodbye!")
            break
        else:
            print("⚠️ Invalid choice, try again.")

# PROGRAM ENTRY POINT

if __name__ == "__main__":
    main_menu()
