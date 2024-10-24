from sqlalchemy.orm import Session
from data.infrastructure.database import SessionManager

class SessionRepository():
    db: Session

    def __init__(self):
        self.session_manager = SessionManager()
        self.db = next(self.session_manager.get_db())
        self.close = self.session_manager.close(self.db)

    def close_db(self):
        self.session_manager.close_all(self.db)