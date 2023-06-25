#API FROM www.thenewsapi.com
from init import create_app
import requests as req
import json
from flask import Flask


app = create_app()




if __name__ == '__main__':
    app.run(debug=True)

