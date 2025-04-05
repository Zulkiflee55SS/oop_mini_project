import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from my_package.database_manager import DatabaseManager

class ViewStudentsWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("ดูรายชื่อนักเรียน")
        self.master.geometry("1000x700")

        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 14))
        style.configure("Treeview.Heading", font=("Arial", 16, "bold"))

        frame = tk.Frame(master)
        frame.pack(fill="both", expand=True)

        columns = ("ID", "ชื่อ", "แผนก", "เบอร์โทร", "วันว่าง", "งานที่เลือก")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=160, anchor="center")

        self.tree.pack(fill="both", expand=True)
        input_frame = tk.Frame(master)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="กรอก ID นักเรียน:", font=("Arial", 16)).grid(row=0, column=0, padx=10)
        self.student_id_entry = tk.Entry(input_frame, font=("Arial", 16), width=20)
        self.student_id_entry.grid(row=0, column=1, padx=10)

        delete_button = tk.Button(input_frame, text="ลบ", font=("Arial", 14), bg="#ff6666", fg="white", width=10, command=self.delete_student)
        delete_button.grid(row=0, column=2, padx=10)

        update_button = tk.Button(input_frame, text="อัปเดต", font=("Arial", 14), bg="#4da6ff", fg="white", width=10, command=self.update_student)
        update_button.grid(row=0, column=3, padx=10)
        filter_frame = tk.Frame(master)
        filter_frame.pack(pady=20)

        tk.Label(filter_frame, text="ค้นหาชื่อนักเรียน:", font=("Arial", 16)).grid(row=0, column=0, padx=10)
        self.search_entry = tk.Entry(filter_frame, font=("Arial", 16), width=30)
        self.search_entry.grid(row=0, column=1, padx=10)

        search_button = tk.Button(filter_frame, text="ค้นหา", font=("Arial", 14), bg="#66cc66", fg="white", width=10, command=self.search_student)
        search_button.grid(row=0, column=2, padx=10)

        clear_button = tk.Button(filter_frame, text="ล้าง", font=("Arial", 14), bg="#999999", fg="white", width=10, command=self.load_data)
        clear_button.grid(row=0, column=3, padx=10)

        self.load_data()

    def load_data(self):
        self.tree.delete(*self.tree.get_children())
        try:
            db = DatabaseManager()
            query = """
                SELECT s.student_id, s.name, s.department, s.phone, s.available_days, j.job_name
                FROM students s
                JOIN jobs j ON s.job_id = j.job_id
            """
            results = db.fetch_all(query)

            if results:
                for row in results:
                    self.tree.insert('', tk.END, values=row)
            else:
                messagebox.showinfo("ไม่มีข้อมูล", "ไม่พบข้อมูลนักเรียนในฐานข้อมูล")

            db.close()

        except Exception as e:
            messagebox.showerror("ข้อผิดพลาด", f"เกิดข้อผิดพลาดในการดึงข้อมูล: {str(e)}")

    def search_student(self):
        keyword = self.search_entry.get().lower()
        for item in self.tree.get_children():
            values = self.tree.item(item)["values"]
            name = str(values[1]).lower()
            if keyword not in name:
                self.tree.detach(item)
            else:
                self.tree.reattach(item, '', 'end')

    def delete_student(self):
        student_id = self.student_id_entry.get()
        if not student_id:
            messagebox.showwarning("กรุณากรอก ID", "กรุณากรอก ID นักเรียนที่ต้องการลบ")
            return

        confirm = messagebox.askyesno("ยืนยันการลบ", "คุณแน่ใจว่าต้องการลบข้อมูลนี้?")
        if confirm:
            db = DatabaseManager()
            query = "DELETE FROM students WHERE student_id = %s"
            db.execute(query, (student_id,))
            db.connection.commit()
            self.remove_from_treeview(student_id)
            db.close()
            messagebox.showinfo("สำเร็จ", f"ลบข้อมูลนักเรียน ID {student_id} สำเร็จ")

    def remove_from_treeview(self, student_id):
        for item in self.tree.get_children():
            if self.tree.item(item)['values'][0] == student_id:
                self.tree.delete(item)
                break

    def update_student(self):
        student_id = self.student_id_entry.get()
        if not student_id:
            messagebox.showwarning("กรุณากรอก ID", "กรุณากรอก ID นักเรียนที่ต้องการอัปเดต")
            return

        db = DatabaseManager()
        query = """
            SELECT s.name, s.department, s.phone, s.available_days
            FROM students s
            WHERE s.student_id = %s
        """
        result = db.fetch_all(query, (student_id,))
        db.close()

        if not result:
            messagebox.showwarning("ไม่พบข้อมูล", "ไม่พบข้อมูลของนักเรียนที่กรอก ID มา")
            return

        current_data = result[0]
        self.show_update_form(student_id, current_data)

    def show_update_form(self, student_id, current_data):
        update_window = tk.Toplevel(self.master)
        update_window.title("อัปเดตข้อมูลนักเรียน")
        update_window.geometry("500x600")

        label_font = ("Arial", 14)
        entry_font = ("Arial", 14)
        button_font = ("Arial", 14)

        tk.Label(update_window, text="ชื่อ-นามสกุล", font=label_font).pack(pady=5)
        name_entry = tk.Entry(update_window, width=40, font=entry_font)
        name_entry.pack(pady=5)
        name_entry.insert(0, current_data[0])

        tk.Label(update_window, text="แผนก", font=label_font).pack(pady=5)
        department_entry = tk.Entry(update_window, width=40, font=entry_font)
        department_entry.pack(pady=5)
        department_entry.insert(0, current_data[1])

        tk.Label(update_window, text="เบอร์โทร", font=label_font).pack(pady=5)
        phone_entry = tk.Entry(update_window, width=40, font=entry_font)
        phone_entry.pack(pady=5)
        phone_entry.insert(0, current_data[2])

        tk.Label(update_window, text="วันว่าง (คั่นด้วย ,)", font=label_font).pack(pady=5)
        available_days_entry = tk.Entry(update_window, width=40, font=entry_font)
        available_days_entry.pack(pady=5)
        available_days_entry.insert(0, current_data[3])

        def confirm_update():
            new_name = name_entry.get()
            new_department = department_entry.get()
            new_phone = phone_entry.get()
            new_available_days = available_days_entry.get()

            if not new_name or not new_department or not new_phone or not new_available_days:
                messagebox.showerror("ข้อผิดพลาด", "กรุณากรอกข้อมูลให้ครบ")
                return

            db = DatabaseManager()
            query = """
                UPDATE students
                SET name = %s, department = %s, phone = %s, available_days = %s
                WHERE student_id = %s
            """
            db.execute(query, (new_name, new_department, new_phone, new_available_days, student_id))
            db.connection.commit()
            db.close()

            self.update_treeview(student_id, new_name, new_department, new_phone, new_available_days)
            messagebox.showinfo("สำเร็จ", "อัปเดตข้อมูลนักเรียนเรียบร้อยแล้ว")
            update_window.destroy()

        tk.Button(update_window, text="อัปเดตข้อมูล", command=confirm_update,
                  bg="green", fg="white", font=button_font, width=15, height=1).pack(pady=10)

        tk.Button(update_window, text="ย้อนกลับ", command=update_window.destroy,
                  bg="gray", fg="white", font=button_font, width=15, height=1).pack(pady=5)

    def update_treeview(self, student_id, new_name, new_department, new_phone, new_available_days):
        for item in self.tree.get_children():
            if self.tree.item(item)['values'][0] == student_id:
                self.tree.item(item, values=(student_id, new_name, new_department, new_phone, new_available_days, ""))
                break