import tkinter as tk
from my_package import RegisterForm
from my_package import ViewStudentsWindow

def show_register():
    top = tk.Toplevel(root)
    RegisterForm(top)
def show_viewer():
    top = tk.Toplevel(root)
    ViewStudentsWindow(top)
    
if __name__ == "__main__":
    root = tk.Tk()
    root.title("ระบบลงทะเบียนงานพิเศษ")
    root.geometry("400x300")
    tk.Label(root, text="เมนูหลัก", font=("Arial", 24)).pack(pady=20)
    tk.Button(root, text="สมัครงาน", command=show_register, width=20, font=("Arial", 16), relief="groove", bd=4).pack(pady=10)
    tk.Button(root, text="ดูรายชื่อผู้สมัคร", command=show_viewer, width=20, font=("Arial", 16), relief="groove", bd=4).pack(pady=10)
    tk.Button(root, text="ออกจากโปรแกรม", command=root.quit, bg="red", fg="white", font=("Arial", 14)).pack(pady=20)

    root.mainloop()
