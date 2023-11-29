# app.py

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_socketio import SocketIO, emit
from nonogram_handler import nonogram_handler

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/nonogram')
def nonogram():
    # Get the grid size from the URL parameters
    grid_size = request.args.get('grid_size', '5')

    # Create a new nonogram handler
    handler = nonogram_handler(grid_size)

    print(f"Generating grid with size: {grid_size}")

    # create a new nonogram
    # if game over, then redirect to game over page
    if handler.game_over == True:
        return redirect(url_for('game_over'))
    # else generate a new nonogram
    else:
        handler.generate_nonogram()
    
    return render_template('nonogram.html', grid_size = grid_size, clues = handler.nonogram.clues, mistakes = handler.mistakes)

# # When the user makes a move, send the move to the server
# @socketio.on('move')
# def make_move(move):
#     print(f"Move: {move}")


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 8000, debug = True)