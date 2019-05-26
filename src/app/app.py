from flask import Flask
from flask import render_template
from redis import Redis
import os

app = Flask(__name__)
redis = Redis(host='redis', port=6379)

@app.route('/')
def hello():
    redis.incr('hits')
    cnt = redis.get('hits').decode("utf-8")
    return render_template('displayMenu.html', hits=cnt)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=80)