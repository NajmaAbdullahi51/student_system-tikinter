
import tkinter as tk
from tkinter import messagebox
import mysql.connector

# 1. MySQL Connection Setup
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",   # hubi inuu sax yahay
        database="test1db"
    )

# all Functions
def add_student():
    student_ID = ID_entry.get()
    student_name = name_entry.get()
    student_age = age_entry.get()
    tell = tell_entry.get()
    student_class = class_entry.get()
    semester = semester_entry.get()
    fee = fee_entry.get()

    if student_ID == "" or student_name == "" or student_age == "" or tell == "" or student_class == "" or semester == "" or fee == "":
        messagebox.showwarning("Fadlan buuxi", "Meel banaan lama ogola")
        return

    students.append([student_ID, student_name, student_age, tell, student_class, semester, fee])
    update_listbox()
    clear_textbox()

    # MySQL Insert
    try:
        conn = connect_db()
        cursor = conn.cursor()
        sql = """
        INSERT INTO students2
        (student_ID, student_name, student_age, student_tell,
         student_class, student_semester, student_fee)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        """
        cursor.execute(sql, (student_ID, student_name, student_age, tell, student_class, semester, fee))
        conn.commit()
        conn.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"xogta Lama kaydin: {err}")

def delete_student():
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("Dooro Shay", "Fadlan mid dooro")
        return

    student_id = students[selected[0]][0]
    students.pop(selected[0])
    update_listbox()

    # MySQL Delete
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students2 WHERE student_ID = %s", (student_id,))
        conn.commit()
        conn.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Lama tirtiri karo: {err}")

def updete_student():
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("Dooro Shay", "Fadlan mid dooro")
        return

    student_ID = ID_entry.get()
    student_name = name_entry.get()
    student_age = age_entry.get()
    tell = tell_entry.get()
    student_class = class_entry.get()
    semester = semester_entry.get()
    fee = fee_entry.get()

    students[selected[0]] = [student_ID, student_name, student_age, tell, student_class, semester, fee]
    update_listbox()
    clear_textbox()

    # MySQL Update
    try:
        conn = connect_db()
        cursor = conn.cursor()
        sql = """
        UPDATE students2 SET
        student_name=%s,
        student_age=%s,
        student_tell=%s,
        student_class=%s,
        student_semester=%s,
        student_fee=%s
        WHERE student_ID=%s
        """
        cursor.execute(sql, (student_name, student_age, tell, student_class, semester, fee, student_ID))
        conn.commit()
        conn.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"update ku walii madhicin: {err}")

def eeg_arday(event):
    selected = listbox.curselection()
    if not selected:
        return

    student = students[selected[0]]

    ID_entry.delete(0, tk.END)
    ID_entry.insert(0, student[0])

    name_entry.delete(0, tk.END)
    name_entry.insert(0, student[1])

    age_entry.delete(0, tk.END)
    age_entry.insert(0, student[2])

    tell_entry.delete(0, tk.END)
    tell_entry.insert(0, student[3])

    class_entry.delete(0, tk.END)
    class_entry.insert(0, student[4])

    semester_entry.delete(0, tk.END)
    semester_entry.insert(0, student[5])

    fee_entry.delete(0, tk.END)
    fee_entry.insert(0, student[6])

def update_listbox():
    listbox.delete(0, tk.END)
    for m in students:
        listbox.insert(
            tk.END,
            f"ID:{m[0]}, name:{m[1]}, age:{m[2]}, tell:{m[3]}, class:{m[4]}, semester:{m[5]}, fee:{m[6]}"
        )

def clear_textbox():
    ID_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    tell_entry.delete(0, tk.END)
    class_entry.delete(0, tk.END)
    semester_entry.delete(0, tk.END)
    fee_entry.delete(0, tk.END)

students = []

habi = tk.Tk()
habi.title("Student Management System")
habi.geometry("350x500")
habi.config(bg="lightgray")

# label ciwaanka
tk.Label(habi, text="STUDENT MANAGEMENT SYSTEM", font=("bold")).pack(pady=10)

# ID
tk.Label(habi, text="Student ID").pack()
ID_entry = tk.Entry(habi, width=30)
ID_entry.pack(pady=5)

# Name
tk.Label(habi, text=" student Name").pack()
name_entry = tk.Entry(habi, width=30)
name_entry.pack(pady=5)

# Age
tk.Label(habi, text="student Age").pack()
age_entry = tk.Entry(habi, width=30)
age_entry.pack(pady=5)

# Tell
tk.Label(habi, text="student Tell").pack()
tell_entry = tk.Entry(habi, width=30)
tell_entry.pack(pady=5)

# Class
tk.Label(habi, text="student Class").pack()
class_entry = tk.Entry(habi, width=30)
class_entry.pack(pady=5)

# Semester
tk.Label(habi, text="student Semester").pack()
semester_entry = tk.Entry(habi, width=30)
semester_entry.pack(pady=5)

# Fee
tk.Label(habi, text="student Fee").pack()
fee_entry = tk.Entry(habi, width=30)
fee_entry.pack(pady=5)

# Buttons
tk.Button(habi, text="Add Student", command=add_student, bg="green", fg="white").pack(pady=5)
tk.Button(habi, text="Update Student", command=updete_student, bg="lightblue", fg="white").pack(pady=5)
tk.Button(habi, text="Delete Student", command=delete_student, bg="red", fg="white").pack(pady=5)

# Listbox
listbox = tk.Listbox(habi, width=100)
listbox.pack(pady=10)
listbox.bind("<<ListboxSelect>>", eeg_arday)

habi.mainloop()
