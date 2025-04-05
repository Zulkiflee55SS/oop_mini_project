import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from .database_manager import DatabaseManager
from .student import Student
from .job import Job

class RegisterForm:
    def __init__(self, root):
        self.root = root
        self.root.title("สมัครงานพิเศษ")
        self.root.geometry("500x600")

        self.days = ["จันทร์", "อังคาร", "พุธ", "พฤหัส", "ศุกร์", "เสาร์", "อาทิตย์"]
        self.day_vars = {}

        self.create_widgets()

    def create_widgets(self):
        label_font = ("Arial", 14)
        entry_font = ("Arial", 14)
        button_font = ("Arial", 14) 
        tk.Label(self.root, text="ชื่อ-นามสกุล", font=label_font).pack(pady=5)
        self.entry_name = tk.Entry(self.root, width=40, font=entry_font)
        self.entry_name.pack(pady=5)
        tk.Label(self.root, text="ชั้น/แผนก", font=label_font).pack(pady=5)
        self.entry_dept = tk.Entry(self.root, width=40, font=entry_font)
        self.entry_dept.pack(pady=5)
        tk.Label(self.root, text="เบอร์โทร", font=label_font).pack(pady=5)
        self.entry_phone = tk.Entry(self.root, width=40, font=entry_font)
        self.entry_phone.pack(pady=5)
        tk.Label(self.root, text="เลือกวันว่าง", font=label_font).pack(pady=5)
        days_frame = tk.Frame(self.root)
        days_frame.pack(pady=5)
        for day in self.days:
            var = tk.BooleanVar()
            cb = tk.Checkbutton(days_frame, text=day, variable=var, font=entry_font)
            cb.pack(side=tk.LEFT, padx=5)
            self.day_vars[day] = var
        tk.Label(self.root, text="เลือกงานที่สนใจ", font=label_font).pack(pady=5)
        self.job_combobox = ttk.Combobox(self.root, width=38, state="readonly", font=entry_font)
        self.job_combobox.pack(pady=5)
        self.load_jobs()
        tk.Button(self.root, text="สมัครงาน", command=self.submit_form,
                bg="green", fg="white", font=button_font, width=15, height=1).pack(pady=10)
        tk.Button(self.root, text="ย้อนกลับ", command=self.root.destroy,
                bg="gray", fg="white", font=button_font, width=15, height=2).pack(pady=5) 
        tk.Button(self.root, text="ออกจากโปรแกรม", command=self.root.quit,
                bg="red", fg="white", font=button_font, width=15, height=1).pack(pady=5)


    def load_jobs(self):
        try:
            db = DatabaseManager()
            query = "SELECT job_id, job_name FROM jobs"
            jobs = db.fetch_all(query)
            if jobs:
                self.jobs_dict = {} 
                job_names = []

                for job in jobs:
                    job_id, job_name = job
                    self.jobs_dict[job_name] = job_id
                    job_names.append(job_name)

                self.job_combobox['values'] = job_names
                self.job_combobox.set(job_names[0])
            else:
                messagebox.showinfo("ไม่มีข้อมูล", "ไม่พบข้อมูลงานในฐานข้อมูล")
            db.close()
        except Exception as e:
            messagebox.showerror("ข้อผิดพลาด", f"เกิดข้อผิดพลาดในการดึงข้อมูลงาน: {str(e)}")



    def submit_form(self):
        name = self.entry_name.get()
        dept = self.entry_dept.get()
        phone = self.entry_phone.get()
        available_days = [day for day, var in self.day_vars.items() if var.get()]
        job_name = self.job_combobox.get()

        if not name or not dept or not phone or not available_days or not job_name:
            messagebox.showerror("ผิดพลาด", "กรุณากรอกข้อมูลให้ครบ")
            return

        job_id = self.jobs_dict[job_name]
        student = Student(name, dept, phone, available_days, job_id)

        db = DatabaseManager()
        student.save_to_db(db)
        db.close()

        messagebox.showinfo("สำเร็จ", "สมัครงานเรียบร้อยแล้ว!")
        self.clear_form()

    def clear_form(self):
        self.entry_name.delete(0, tk.END)
        self.entry_dept.delete(0, tk.END)
        self.entry_phone.delete(0, tk.END)
        self.job_combobox.set("")
        for var in self.day_vars.values():
            var.set(False)
