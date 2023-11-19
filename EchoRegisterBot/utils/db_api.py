


import sqlite3



class Users:
    def __init__(self):
        self.connection = sqlite3.connect("D:\home\code\EchoRegisterBot\database\database_echo.db")
        self.cursor = self.connection.cursor()
        
        
    def add_user(self, user_id, username, is_admin=0, worker=0, accept=0):
        result = self.cursor.execute("INSERT INTO users (user_id, username, is_admin, worker, accept) VALUES (?, ?, ?, ?, ?)", (user_id, username, is_admin, worker, accept,))
        self.connection.commit()
        return result
    
    
    def select_user_state(self):
        result = self.cursor.execute("SELECT user_id FROM users WHERE accept = ?", (3,)).fetchall()
        return result
    
    
    def delete_user(self, user_id):
        self.cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        self.connection.commit()
    
    
    def select_blocked_users(self):
        result = self.cursor.execute("SELECT user_id, username FROM users WHERE accept = ?", (2,)).fetchall()
        return result
    
    
    def update_user_state_accept(self):
        self.cursor.execute("UPDATE users SET accept = ? WHERE accept = ?", (1, 3))
        self.connection.commit()
        
        
    def update_user_state_decline(self):
        self.cursor.execute("UPDATE users SET accept = ? WHERE accept = ?", (2, 3))
        self.connection.commit()
    
    
    def update_user_state_unblock(self, user_id):
        self.cursor.execute("UPDATE users SET accept = ? WHERE user_id = ?", (0, user_id))
        self.connection.commit()
    
    
    def user_exists(self, user_id):
        result = self.cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
        exists = result.fetchone()
        return exists is not None
    
    
    def is_user_admin(self, user_id):
        result = self.cursor.execute("SELECT user_id FROM users WHERE user_id = ? AND is_admin = ?", (user_id, 1)).fetchone()
        print(f"Результат запроса: {result}")  # Добавим отладочный вывод
        return result is not None



    def get_admin_user_ids(self):
        admin_user_ids = []
        results = self.cursor.execute("SELECT user_id FROM users WHERE is_admin = ?", (1,)).fetchall()
        for result in results:
            admin_user_ids.append(result[0])  # Добавляем user_id в список admin_user_ids
        return admin_user_ids