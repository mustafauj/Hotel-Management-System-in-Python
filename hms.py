import mysql.connector
import re
from tkinter import *
from tkinter import messagebox

class Booking:
    def __init__(self, master):
        self.master = master
        self.master.title("Sapphire Hotel Booking")
        self.master.geometry("500x400")
        self.master.config(bg="#ADD8E6")
        
        # Title Label
        Label(self.master, text="Welcome to Sapphire Hotel", font=("Arial", 20), bg="#ADD8E6").pack(pady=20)
        
        # Choice Buttons
        Button(self.master, text="Book a Room", command=self.book_room, width=20, height=2, bg="lightgreen").pack(pady=10)
        Button(self.master, text="Reserve a Table", command=self.reserve_table, width=20, height=2, bg="lightblue").pack(pady=10)
        Button(self.master, text="Book a Hall", command=self.book_hall, width=20, height=2, bg="lightcoral").pack(pady=10)
        Button(self.master, text="Exit", command=self.master.quit, width=20, height=2, bg="grey").pack(pady=10)

        # Ensure database and table exist
        self.create_database()

    def create_database(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Muj@7105"
            )
            cursor = conn.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS sapphire_hotel")
            cursor.execute("USE sapphire_hotel")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS bookings (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255),
                    age INT,
                    date VARCHAR(255),
                    email VARCHAR(255),
                    valid_id VARCHAR(255),
                    booking_type VARCHAR(255)
                )
            """)
            conn.commit()
            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def take_details(self, booking_type):
        self.new_window = Toplevel(self.master)
        self.new_window.title(f"{booking_type} Details")
        self.new_window.geometry("400x400")
        self.new_window.config(bg="#F0E68C")

        # Labels and entries for booking details
        Label(self.new_window, text="Enter First Name:", bg="#F0E68C").pack(pady=10)
        self.name_entry = Entry(self.new_window)
        self.name_entry.pack()

        Label(self.new_window, text="Enter Age:", bg="#F0E68C").pack(pady=10)
        self.age_entry = Entry(self.new_window)
        self.age_entry.pack()

        Label(self.new_window, text="Enter Booking Date (DD MM YYYY):", bg="#F0E68C").pack(pady=10)
        self.date_entry = Entry(self.new_window)
        self.date_entry.pack()

        Label(self.new_window, text="Enter Email:", bg="#F0E68C").pack(pady=10)
        self.email_entry = Entry(self.new_window)
        self.email_entry.pack()

        Label(self.new_window, text="Enter Valid ID:", bg="#F0E68C").pack(pady=10)
        self.id_entry = Entry(self.new_window)
        self.id_entry.pack()

        Button(self.new_window, text="Submit", command=lambda: self.submit_details(booking_type), bg="lightgreen").pack(pady=20)

    def submit_details(self, booking_type):
        name = self.name_entry.get()
        age = int(self.age_entry.get())
        date = self.date_entry.get()
        email = self.email_entry.get()
        valid_id = self.id_entry.get()

        if not self.is_valid_email(email):
            messagebox.showerror("Error", "Invalid Email Address")
            return

        if age < 18:
            messagebox.showwarning("Warning", "Sorry, you are unable to book.")
        else:
            messagebox.showinfo("Success", f"Dear {name}, your {booking_type} is confirmed for {date}. Thank you for choosing us!")

            # Connect to MySQL and insert the booking details
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="Muj@7105",
                    database="sapphire_hotel"
                )
                cursor = conn.cursor()
                sql = "INSERT INTO bookings (name, age, date, email, valid_id, booking_type) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (name, age, date, email, valid_id, booking_type))
                conn.commit()
                conn.close()
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Database Error: {err}")

    def is_valid_email(self, email):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email)

    def book_room(self):
        self.take_details("Room")

    def reserve_table(self):
        self.take_details("Table")

    def book_hall(self):
        self.take_details("Hall")


# Tkinter window initialization
root = Tk()
app = Booking(root)
root.mainloop()
