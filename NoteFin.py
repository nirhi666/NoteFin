import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import re

# Funktio luomaan uusi Post-it-lappu
def create_post_it(root, x, y, offset):
    post_it = tk.Toplevel(root)
    post_it.title("NoteFin Lappu")
    post_it.geometry(f"200x150+{x}+{y}")
    post_it.overrideredirect(1)  # Poistaa reunat
    post_it.configure(bg="#ffeb3b")

    note_text = tk.Text(post_it, height=7, width=20, bg="#ffeb3b", font=("Arial", 12), bd=0, highlightthickness=0)
    note_text.pack(padx=10, pady=(30, 10))

    window_locked = False
    minimized = False  # Tila lappua varten

    def move_window(event):
        if not window_locked:
            post_it.geometry(f'+{event.x_root}+{event.y_root}')

    note_text.bind("<B1-Motion>", move_window)

    def toggle_lock():
        nonlocal window_locked
        if window_locked:
            window_locked = False
            lock_button.config(text="Lukitse")
        else:
            window_locked = True
            lock_button.config(text="Vapauta")

    lock_button = tk.Button(post_it, text="Lukitse", command=toggle_lock, bg="#ffeb3b", font=("Arial", 10), bd=0)
    lock_button.place(x=5, y=5)

    def delete_note():
        if window_locked:
            messagebox.showwarning("Lukittu", "Et voi poistaa tätä lappua, koska se on lukittu, poista lukitus jos haluat poistaa tämän lapun!")
        else:
            if messagebox.askyesno("Poista muistiinpano", "Haluatko varmasti poistaa tämän muistilapun?"):
                post_it.destroy()

    close_button = tk.Button(post_it, text="X", command=delete_note, bg="#ffeb3b", font=("Arial", 10), bd=0, fg="black")
    close_button.place(x=170, y=0)

    def minimize_note():
        nonlocal minimized
        minimized = True
        post_it.withdraw()  # Piilotetaan lappu

    minimize_button = tk.Button(post_it, text="-", command=minimize_note, bg="#ffeb3b", font=("Arial", 10), bd=0, fg="black")
    minimize_button.place(x=145, y=0)

    def check_time():
        nonlocal minimized
        text_content = note_text.get("1.0", "end-1c")
        time_match = re.search(r'\b(\d{1,2}[:.,;]\d{2})\b', text_content)



        if time_match:
            alarm_time_str = time_match.group(1).replace('.', ':').replace(',', ':').replace(';', ':') #varmistetaan ettei sosialisti pääse ulisemaan väärästä aikamerkinnästä
            now = datetime.now()
            try:
                alarm_time = datetime.strptime(alarm_time_str, "%H:%M").replace(year=now.year, month=now.month, day=now.day)
                if alarm_time - timedelta(minutes=5) <= now <= alarm_time and minimized:
                    post_it.deiconify()  # Näytetään lappu
                    post_it.lift()  # Tuodaan etualalle
                    post_it.attributes("-topmost", True)  # Asetetaan topmost uudestaan
                    minimized = False  # Päivitetään tila
            except ValueError:
                pass

        root.after(15000, check_time)  # Tarkistus 15 sekunnin välein

    def check_window_position():
        x = post_it.winfo_x()
        y = post_it.winfo_y()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        if x < 0 or y < 0 or x > screen_width - 200 or y > screen_height - 150:
            new_x = 100 + offset
            new_y = 100 + offset
            post_it.geometry(f'+{new_x}+{new_y}')

        root.after(5000, check_window_position)

    check_time()
    check_window_position()

# Aktivaattori-ikkuna
def create_launcher(root):
    launcher = tk.Toplevel(root)
    launcher.title("Aktivaattori")
    launcher.geometry("60x60+10+10")
    launcher.overrideredirect(1)
    launcher.configure(bg="#ffeb3b")

    def keep_launcher_visible():
        launcher.deiconify()

    def move_launcher(event):
        launcher.geometry(f'+{event.x_root}+{event.y_root}')

    launcher.bind("<B1-Motion>", move_launcher)
    launcher.protocol("WM_DELETE_WINDOW", keep_launcher_visible)

    def check_launcher_position():
        x = launcher.winfo_x()
        y = launcher.winfo_y()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        if x < 0 or y < 0 or x > screen_width - 50 or y > screen_height - 50:
            launcher.geometry("+10+10")

        root.after(5000, check_launcher_position)

    check_launcher_position()

    def toggle_post_it():
        for toplevel in root.winfo_children():
            if isinstance(toplevel, tk.Toplevel) and toplevel != launcher:
                if toplevel.state() == "normal":
                    toplevel.withdraw()
                else:
                    toplevel.deiconify()
                    toplevel.lift()

    toggle_button = tk.Button(launcher, text="NoteFin", command=toggle_post_it, bg="#ffeb3b", font=("Arial", 12), bd=0)
    toggle_button.pack(fill=tk.BOTH, expand=True)

# Varmistetaan, että vähintään 3 lappua on olemassa
def ensure_notes():
    existing_notes = [
        toplevel for toplevel in root.winfo_children() if isinstance(toplevel, tk.Toplevel) and "Lappu" in toplevel.title()
    ]
    while len(existing_notes) < 3:
        create_post_it(root, 100 + len(existing_notes) * 20, 100 + len(existing_notes) * 20, len(existing_notes) * 20)
        existing_notes.append("new")

    root.after(5000, ensure_notes)  # Tarkistus 5 sekunnin välein

# Pääikkuna
root = tk.Tk()
root.withdraw()

# Luo kolme Post-it-lappua päällekkäin
for i in range(3):
    create_post_it(root, 100 + i * 20, 100 + i * 20, i * 20)

# Luo aktivaattori-ikkuna
create_launcher(root)

# Varmista, että laput pysyvät olemassa
ensure_notes()

# Käynnistetään sovellus
root.mainloop()
