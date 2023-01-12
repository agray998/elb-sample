from flask import Flask
from src import application, db

with application.app_context():
    db.drop_all()
    db.create_all()

if __name__ == '__main__':
    application.run(debug = True, host = '0.0.0.0')
# blah
