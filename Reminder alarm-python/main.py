from datetime import datetime, timedelta
import time
import threading
import tkinter as tk
from tkinter import messagebox

def show_reminder():
    reminder_text = entry_text.get()
    messagebox.showinfo("Reminder", reminder_text)

def set_reminder():
    global entry_text, entry_time, remaining_label, count_thread
    reminder_text = entry_text.get()
    reminder_time = entry_time.get()

    try:
        current_time = datetime.now()
        target_time = datetime.strptime(reminder_time, "%H:%M")
        target_datetime = datetime.combine(current_time.date(), target_time.time())

        if target_datetime < current_time:
            target_datetime += timedelta(days=1)

        time_difference = target_datetime - current_time
        seconds_to_wait = time_difference.total_seconds()

        count_thread = threading.Thread(target=countdown, args=(seconds_to_wait,))
        count_thread.start()

        threading.Timer(seconds_to_wait, show_reminder).start()
    except ValueError:
        print("Invalid time format.")

def countdown(seconds):
    global remaining_label, count_thread
    while seconds > 0:
        minutes, secs = divmod(seconds, 60)
        time_format = '{:02d}:{:02d}'.format(int(minutes), int(secs))
        remaining_label.config(text=f"Remaining Time: {time_format}")
        time.sleep(1)
        seconds -= 1

    remaining_label.config(text="Remaining Time: 00:00")
    count_thread.join()

def on_closing():
    if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
        window.destroy()

def create_reminder():
    global entry_text, entry_time, remaining_label, window
    window = tk.Tk()
    window.title("Reminder")
    window.configure(bg="#f9f9f9")
    window.geometry("350x300")
    window.resizable(False, False)
    window.protocol("WM_DELETE_WINDOW", on_closing)

    label_title = tk.Label(window, text="Reminder", font=("Arial", 20, "bold"), bg="#f9f9f9")
    label_title.pack(pady=20)

    frame_input = tk.Frame(window, bg="#f9f9f9")
    frame_input.pack()

    label_text = tk.Label(frame_input, text="Reminder Text:", font=("Arial", 12), bg="#f9f9f9")
    label_text.grid(row=0, column=0, pady=10)

    entry_text = tk.Entry(frame_input, width=30, font=("Arial", 12))
    entry_text.grid(row=0, column=1, pady=10, padx=10)

    label_time = tk.Label(frame_input, text="Reminder Time (HH:MM):", font=("Arial", 12), bg="#f9f9f9")
    label_time.grid(row=1, column=0, pady=10)

    entry_time = tk.Entry(frame_input, width=30, font=("Arial", 12))
    entry_time.grid(row=1, column=1, pady=10, padx=10)

    button_create = tk.Button(window, text="Create Reminder", command=set_reminder, width=20, font=("Arial", 12), bg="#4caf50", fg="white")
    button_create.pack(pady=20)

    remaining_label = tk.Label(window, text="Remaining Time: ", font=("Arial", 14), bg="#f9f9f9")
    remaining_label.pack()

    window.mainloop()

create_reminder()
