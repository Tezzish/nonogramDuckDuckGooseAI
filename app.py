# app.py

from flask import Flask, render_template, request, redirect, url_for, flash, session  

app = Flask(__name__)

@app.route('/')
def Index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 8000, debug = True)