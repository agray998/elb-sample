from flask import Flask
from src import application, db

if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    application.run(debug = True, host = '0.0.0.0')
# blah
