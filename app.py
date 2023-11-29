# app.py

from flask import Flask, render_template, request, redirect, url_for, flash, session  

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/nonogram')
def getRandomNonogram():
    # Get the grid size from the URL parameters
    grid_size = request.args.get('grid_size', '5')

    print(int(grid_size) + 10)

    print(f"Generating grid with size: {grid_size}")

    # Return a response (for demonstration purposes)
    return f"Generating grid with size: {grid_size}"

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 8000, debug = True)