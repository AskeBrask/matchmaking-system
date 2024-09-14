import tkinter as tk
from tkinter import messagebox, ttk
from data_manager import DataManager
from matcher import Matcher

class ApplicationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Temp Worker Matchmaking System")
        self.root.geometry("500x500")

        # Frame for buttons (top)
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Tilføj Vikar", command=self.add_worker_gui).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Tilføj Job", command=self.add_job_gui).grid(row=0, column=1, padx=10)
        tk.Button(button_frame, text="Match Vikar til Job", command=self.match_workers_gui).grid(row=0, column=2, padx=10)

        # Frame for match results (bottom)
        self.result_frame = tk.Frame(root)
        self.result_frame.pack(pady=10, fill='both', expand=True)

        # Scrollable result area
        self.result_label = tk.Text(self.result_frame, wrap='word', height=15)
        self.result_label.pack(side="left", fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(self.result_frame, command=self.result_label.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.result_label.config(yscrollcommand=self.scrollbar.set)

    def clear_results(self):
        self.result_label.delete(1.0, tk.END)

    def add_worker_gui(self):
        def submit_worker():
            name = entry_name.get()
            skills = entry_skills.get().split(',')
            availability = entry_availability.get().split(',')
            location = entry_location.get()
            
            # Validate experience
            try:
                experience_years = int(entry_experience.get())
            except ValueError:
                messagebox.showerror("Fejl", "Ugyldigt input! Indtast et gyldigt tal for erfaring (år).")
                return

            workers = DataManager.load_workers()
            new_worker = {
                "id": len(workers) + 1,
                "name": name,
                "skills": [skill.strip() for skill in skills],
                "availability": [day.strip() for day in availability],
                "location": location,
                "experience_years": experience_years
            }
            workers.append(new_worker)
            DataManager.save_workers(workers)
            messagebox.showinfo("Success", f"Vikar {name} er blevet tilføjet!")
            add_worker_window.destroy()

        add_worker_window = tk.Toplevel(self.root)
        add_worker_window.title("Tilføj Vikar")

        # GUI elements for adding worker
        tk.Label(add_worker_window, text="Navn:").grid(row=0)
        entry_name = tk.Entry(add_worker_window)
        entry_name.grid(row=0, column=1)

        tk.Label(add_worker_window, text="Færdigheder (komma adskilt):").grid(row=1)
        entry_skills = tk.Entry(add_worker_window)
        entry_skills.grid(row=1, column=1)

        tk.Label(add_worker_window, text="Tilgængelighed (dage, komma adskilt):").grid(row=2)
        entry_availability = tk.Entry(add_worker_window)
        entry_availability.grid(row=2, column=1)

        tk.Label(add_worker_window, text="Lokation:").grid(row=3)
        entry_location = tk.Entry(add_worker_window)
        entry_location.grid(row=3, column=1)

        tk.Label(add_worker_window, text="Erfaring (år):").grid(row=4)
        entry_experience = tk.Entry(add_worker_window)
        entry_experience.grid(row=4, column=1)

        tk.Button(add_worker_window, text="Tilføj Vikar", command=submit_worker).grid(row=5, column=1)

    def add_job_gui(self):
        def submit_job():
            title = entry_title.get()
            required_skills = entry_required_skills.get().split(',')
            days_needed = entry_days_needed.get().split(',')
            location = entry_location.get()

            jobs = DataManager.load_jobs()
            new_job = {
                "id": len(jobs) + 1,
                "title": title,
                "required_skills": [skill.strip() for skill in required_skills],
                "days_needed": [day.strip() for day in days_needed],
                "location": location
            }
            jobs.append(new_job)
            DataManager.save_jobs(jobs)
            messagebox.showinfo("Success", f"Jobbet {title} er blevet tilføjet!")
            add_job_window.destroy()

        add_job_window = tk.Toplevel(self.root)
        add_job_window.title("Tilføj Job")

        # GUI elements for adding job
        tk.Label(add_job_window, text="Job Titel:").grid(row=0)
        entry_title = tk.Entry(add_job_window)
        entry_title.grid(row=0, column=1)

        tk.Label(add_job_window, text="Færdigheder (komma adskilt):").grid(row=1)
        entry_required_skills = tk.Entry(add_job_window)
        entry_required_skills.grid(row=1, column=1)

        tk.Label(add_job_window, text="Dage (komma adskilt):").grid(row=2)
        entry_days_needed = tk.Entry(add_job_window)
        entry_days_needed.grid(row=2, column=1)

        tk.Label(add_job_window, text="Lokation:").grid(row=3)
        entry_location = tk.Entry(add_job_window)
        entry_location.grid(row=3, column=1)

        tk.Button(add_job_window, text="Tilføj Job", command=submit_job).grid(row=4, column=1)

    def match_workers_gui(self):
        workers = DataManager.load_workers()
        jobs = DataManager.load_jobs()

        match_window = tk.Toplevel(self.root)
        match_window.title("Match Vikarer til Job")

        tk.Label(match_window, text="Vælg et job:").grid(row=0)

        job_list = [f"{job['title']} i {job['location']}" for job in jobs]
        selected_job = tk.StringVar()
        tk.OptionMenu(match_window, selected_job, *job_list).grid(row=1)

        def perform_match():
            job_index = job_list.index(selected_job.get())
            selected_job_data = jobs[job_index]

            matched_workers = Matcher.match_workers_to_job(workers, selected_job_data)

            self.clear_results()

            if matched_workers:
                result_text = "\n".join([f"Vikar: {worker['name']}, Færdigheder: {', '.join(worker['skills'])}" for worker in matched_workers])
            else:
                result_text = "Ingen vikarer matchede jobkravene."

            self.result_label.insert(tk.END, result_text)

        tk.Button(match_window, text="Match Vikarer", command=perform_match).grid(row=2)

