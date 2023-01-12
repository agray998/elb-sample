from src import application, db

with application.app_context():
    db.drop_all()
    db.create_all()
