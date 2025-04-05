from .database_manager import DatabaseManager

class Job:
    def __init__(self, job_id, name):
        self.job_id = job_id
        self.name = name

    @staticmethod
    def get_all_jobs():
        db = DatabaseManager()
        jobs_data = db.fetch("SELECT job_id, job_name FROM jobs")
        jobs = [Job(job_id, name) for job_id, name in jobs_data]
        db.close()
        return jobs
