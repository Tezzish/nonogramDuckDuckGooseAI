# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_socketio import SocketIO, emit
from nonogram_handler import nonogram_handler

app = Flask(__name__)
socketio = SocketIO(app)
handler = None
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/nonogram')
def nonogram():
    # Get the grid size from the URL parameters
    grid_size = request.args.get('grid_size', '5')

    global handler
    handler = nonogram_handler(int(grid_size))

    print(f"Generating grid with size: {grid_size}")

    # create a new nonogram
    handler.generate_nonogram()
    
    if handler.nonogram is None:
        print("Nonogram is None")
        return redirect(url_for('index'))
    
    context = {
        'grid_size': grid_size,
        'clues': handler.nonogram.clues,
        'mistakes': handler.mistakes
    }

    return render_template('nonogram.html', grid_context = context, mistakes = handler.mistakes)

# # When the user makes a move, send the move to the server
@socketio.on('move')
def make_move(move):
    game_over = handler.game_over
    if game_over:
        emit('game over', broadcast = True)
        print("1 game over")
        return redirect(url_for('game_over'))
    else:
        # if valid and correct
        if handler.make_move((move['x'], move['y'])):
            #if solved
            if handler.is_solved():
                emit('solved', broadcast = True)
                print("solved")
            # if not solved
            else:
                emit('not solved', broadcast = True)
                print("not solved")
        # if not valid and correct then we check if game over
        elif not handler.game_over:
            emit('incorrect', broadcast = True)
            print("incorrect")
        
        else:
            emit('game over', broadcast = True)
            print("2 game over")
            return redirect(url_for('game_over'))
    
@app.route('/game_over')
def game_over():
    return render_template('game_over.html')

@app.route('/solved')
def solved():
    return render_template('solved.html')

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 8000, debug = True)
    