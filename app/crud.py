from sqlalchemy.orm import Session
from app.models import User
from app.database import SessionLocal

def get_user_by_username(username: str, db: Session = SessionLocal()):
    return db.query(User).filter(User.username == username).first()

def create_user(username: str, password: str, db: Session = SessionLocal()):
    db_user = User(username=username, password=password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
