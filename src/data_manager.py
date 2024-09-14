import json
import os

# File paths for storing data
WORKERS_FILE = os.path.join('data', 'workers.json')
JOBS_FILE = os.path.join('data', 'jobs.json')

class DataManager:
    @staticmethod
    def load_data(file_path):
        if not os.path.exists(file_path):
            return []
        with open(file_path, 'r') as file:
            return json.load(file)

    @staticmethod
    def save_data(file_path, data):
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def load_workers():
        return DataManager.load_data(WORKERS_FILE)

    @staticmethod
    def save_workers(workers):
        DataManager.save_data(WORKERS_FILE, workers)

    @staticmethod
    def load_jobs():
        return DataManager.load_data(JOBS_FILE)

    @staticmethod
    def save_jobs(jobs):
        DataManager.save_data(JOBS_FILE, jobs)
