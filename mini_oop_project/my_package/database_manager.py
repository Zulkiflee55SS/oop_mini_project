import mysql.connector

class DatabaseManager:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="parttime_db"
        )
        self.cursor = self.connection.cursor()

    def fetch_all(self, query, params=None):
        self.cursor.execute(query, params)  # ส่ง params ไปที่ execute
        return self.cursor.fetchall()  # ดึงข้อมูลทั้งหมดจากผลลัพธ์ของ query


    def execute(self, query, params=None):
        # ใช้ฟังก์ชันนี้สำหรับการรันคำสั่ง SQL ที่ไม่ต้องการผลลัพธ์
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        self.connection.commit()  # ทำการบันทึกการเปลี่ยนแปลง

    def close(self):
        self.cursor.close()
        self.connection.close()
