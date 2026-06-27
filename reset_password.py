from app.db.database import SessionLocal
from app.models.user import User
from app.services.auth import hash_password

db = SessionLocal()
USERNAME = 'admin'
NEW_PASSWORD = 'Admin@1234'
user = db.query(User).filter(User.username == USERNAME).first()
if user:
    user.hashed_password = hash_password(NEW_PASSWORD)
    db.commit()
    print(f'Password reset for {USERNAME} — new password: {NEW_PASSWORD}')
else:
    print(f'User {USERNAME} not found')
    for u in db.query(User).all():
        print(f'  - {u.username} ({u.email})')
db.close()
