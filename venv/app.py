from flask import Flask

app = Flask(__name__)

@app.route('/')
def hellpo_world():
    return 'hello world'