#Importing the necessary libraries
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from fpdf import FPDF
import matplotlib.pyplot as plt
import mysql.connector
import csv, os, re
from datetime import datetime

# My local host MySQL deatils
MYSQL_USER = "root"
MYSQL_PASSWORD = "Manurse2024//!"
MYSQL_HOST = "localhost"
MYSQL_DB = "fluid_calculator"

# Connecting to MySQL server and creating the database 
conn_init = mysql.connector.connect(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWORD)
cursor_init = conn_init.cursor()
cursor_init.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DB}")
conn_init.commit()
cursor_init.close()
conn_init.close()

conn = mysql.connector.connect(
    host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWORD, database=MYSQL_DB)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS patients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    age FLOAT,
    weight FLOAT,
    date_of_visit DATE,
    dehydration_level VARCHAR(50),
    shock BOOLEAN,
    bolus_volume FLOAT,
    rehydration_volume FLOAT,
    total_fluid_volume FLOAT,
    rate_per_hour FLOAT,
    duration_hours INT,
    timestamp DATETIME
);""")
conn.commit()

# Determining the Fluid Calculation Guidelines adopted from WHO fluid Replacement Guidelines 
# Calculation based on age, weight,level of dehyadration and whether the patient is in shock
def calculate_fluid(age, weight, dehydration_level, shock):
    bolus = 0
    rehydration = 0
    duration = 0

    if dehydration_level == "mild":
        return 0, 0, 0, 0, 0

    if shock and dehydration_level == "severe":
        if age <= 1:
            bolus = 20 * weight
        else:
            bolus = 30 * weight

    if dehydration_level == "moderate":
        rehydration = 75 * weight
        duration = 4
    elif dehydration_level == "severe":
        rehydration = 100 * weight
        duration = 3 if age <= 1 else 6

    total = bolus + rehydration
    rate = rehydration / duration if duration else 0
    return round(bolus, 2), round(rehydration, 2), round(total, 2), round(rate, 2), duration

#Creating functionality for patients logs to be exported into a local csv file
def export_to_csv(data):
    file_exists = os.path.isfile("fluid_log.csv")
    with open("fluid_log.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Name", "Age", "Weight", "Date", "Dehydration", "Shock",
                             "Bolus", "Rehydration", "Total", "Rate", "Duration", "Timestamp"])
        writer.writerow(data)

#Creating functionality for patients logs to be exported into a pdf file
def export_to_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Fluid Replacement Report", ln=True, align='C')
    pdf.ln(10)

    labels = ["Name", "Age", "Weight", "Date", "Dehydration", "Shock", "Bolus (ml)",
              "Rehydration (ml)", "Total Fluid (ml)", "Rate (ml/hr)", "Duration (hrs)", "Timestamp"]
    
    for label, value in zip(labels, data):
        pdf.cell(200, 10, txt=f"{label}: {value}", ln=True)
    pdf.output(f"{data[0]}_fluid_report.pdf")

# Creating functionality to visualize patient fluid totals using a bar chart
def plot_summary():
    try:
        names, totals = [], []
        with open("fluid_log.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                names.append(row["Name"])
                totals.append(float(row["Total"]))
        plt.bar(names, totals, color='skyblue')
        plt.xticks(rotation=45)
        plt.title("Fluid Totals per Patient")
        plt.xlabel("Patient")
        plt.ylabel("Total Fluids (ml)")
        plt.tight_layout()
        plt.show()
    except Exception as e:
        messagebox.showerror("Plot Error", str(e))

# Submitting patient input, calculating fluids, and saving to database, CSV, and PDF
def on_submit():
    name = name_entry.get()
    age = age_entry.get()
    weight = weight_entry.get()
    level = level_var.get()
    shock = shock_var.get()
    date = date_entry.get_date()

    if not re.match("^[A-Za-z ]+$", name):
        messagebox.showerror("Input Error", "Name must only contain letters and spaces.")
        return

    try:
        age = float(age)
        weight = float(weight)
        shock_flag = 1 if shock else 0
        bolus, rehydration, total, rate, duration = calculate_fluid(age, weight, level, shock_flag)
        now = datetime.now()

        cursor.execute("""
            INSERT INTO patients (name, age, weight, date_of_visit, dehydration_level, shock, bolus_volume,
            rehydration_volume, total_fluid_volume, rate_per_hour, duration_hours, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (name, age, weight, date, level, shock_flag, bolus, rehydration, total, rate, duration, now))
        conn.commit()

        data = [name, age, weight, date, level, "Yes" if shock else "No",
                bolus, rehydration, total, rate, duration, now.strftime("%Y-%m-%d %H:%M:%S")]

        export_to_csv(data)
        export_to_pdf(data)

        result_text = (
            f"💉 Bolus Volume: {bolus} mL\n"
            f"💧 Rehydration Volume: {rehydration} mL\n"
            f"🧪 Total Fluids Required: {total} mL\n"
            f"⏱️ Infusion Rate: {rate} mL/hour\n"
            f"🕓 Duration: {duration} hours"
        )
        result_label.config(text=result_text, foreground="blue", font=("Segoe UI", 10, "bold"))
    except ValueError:
        messagebox.showerror("Invalid Input", "Age and weight must be numbers.")

# Creating the main application window and initialising the GUI
root = tk.Tk()
root.title("Advanced Fluid Calculator")
root.geometry("500x600")

# Configuring ttk styles for a clean user interface experience
style = ttk.Style()
style.configure("TLabel", font=("Segoe UI", 10))
style.configure("TButton", font=("Segoe UI", 10))
style.configure("TEntry", font=("Segoe UI", 10))

# Adding input fields and widgets for user interaction
ttk.Label(root, text="Patient Name:").pack(pady=(10, 0))
name_entry = ttk.Entry(root, width=30)
name_entry.pack()

ttk.Label(root, text="Age (years):").pack()
age_entry = ttk.Entry(root, width=30)
age_entry.pack()

ttk.Label(root, text="Weight (kg):").pack()
weight_entry = ttk.Entry(root, width=30)
weight_entry.pack()

ttk.Label(root, text="Date of Visit:").pack()
date_entry = DateEntry(root, width=30)
date_entry.pack()

ttk.Label(root, text="Dehydration Level:").pack()
level_var = tk.StringVar()
level_var.set("mild")
ttk.OptionMenu(root, level_var, "mild", "moderate", "severe").pack()

shock_var = tk.BooleanVar()
ttk.Checkbutton(root, text="Is the patient in shock?", variable=shock_var).pack()

# Adding action buttons and result display area
ttk.Button(root, text="Calculate", command=on_submit).pack(pady=10)
ttk.Button(root, text="Show Chart", command=plot_summary).pack()

ttk.Label(root, text="📊 Fluid Prescription Summary:", font=("Segoe UI", 10, "bold")).pack(pady=(10, 0))
result_label = ttk.Label(root, text="")
result_label.pack()

# Running the GUI application loop and closing DB connection on exit
root.mainloop()
conn.close()
