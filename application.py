from flask import Flask
from src import application

if __name__ == '__main__':
    application.run(debug = True, host = '0.0.0.0')
# blah
