from data.infrastructure.database import Database

class UserRepository():
    database : Database

    def __init__(self):
        self.database = Database()

    
    def read_all(self):
        self.database.get_cursor().execute("select * from user")
        all_users = self.database.get_cursor().fetchall()

        return all_users
    
    def read_by_id(self, id: int):
        self.database.get_cursor().execute(f"select * from user where id = {id}")
        user = self.database.get_cursor().fetchone()

        return user