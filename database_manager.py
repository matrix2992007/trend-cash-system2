import sqlite3

class SystemEngine:
    def __init__(self, db_name="trend_cash.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        # جدول المستخدمين: آيدي، يوزر، رصيد، عداد إحالات، عداد سحب
        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
            (user_id INTEGER PRIMARY KEY, 
             username TEXT, 
             balance REAL DEFAULT 0.0, 
             ref_count INTEGER DEFAULT 0, 
             withdraw_count INTEGER DEFAULT 0)''')
        self.conn.commit()

    def get_user_data(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
        return cursor.fetchone()

    def add_new_user(self, user_id, username):
        cursor = self.conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
        self.conn.commit()

    def get_goal(self, user_id):
        """تحديد الهدف: 13 للأول، 14 للتاني"""
        user = self.get_user_data(user_id)
        if not user or user[4] == 0: return 13
        if user[4] == 1: return 14
        return 16

    def update_referral(self, referrer_id):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE users SET ref_count = ref_count + 1 WHERE user_id=?", (referrer_id,))
        self.conn.commit()
