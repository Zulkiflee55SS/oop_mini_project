class Student:
    def __init__(self, name, department, phone, available_days, job_id):
        self.name = name
        self.department = department
        self.phone = phone
        self.available_days = available_days  # list of strings
        self.job_id = job_id

    def save_to_db(self, db):
        available_str = ",".join(self.available_days)
        query = """
            INSERT INTO students (name, department, phone, available_days, job_id)
            VALUES (%s, %s, %s, %s, %s)
        """
        db.execute(query, (self.name, self.department, self.phone, available_str, self.job_id))
