class Matcher:
    @staticmethod
    def match_workers_to_job(workers, job):
        matched_workers = []
        
        for worker in workers:
            skill_match = all(skill in worker['skills'] for skill in job['required_skills'])
            availability_match = all(day in worker['availability'] for day in job['days_needed'])
            location_match = worker['location'].lower() == job['location'].lower()

            if skill_match and availability_match and location_match:
                matched_workers.append(worker)

        return matched_workers
