from data.infrastructure.database import Database

class UserRepository:
    database : Database

    def __init__(self):
        self.database = Database()

    
    def read_all_users(self):
        self.database.get_cursor().execute("select * from user")
        all_users = self.database.get_cursor().fetchall()

        return all_users