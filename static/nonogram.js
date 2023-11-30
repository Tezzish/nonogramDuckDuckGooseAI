var socket = null;

function connectSocket() {
    document.addEventListener('DOMContentLoaded', function () {
        // connect to the socket
        console.log("connecting")
        socket = io.connect('127.0.0.1:8000');
        // add the event listeners for the socket
        socket.on('solved', function () {
            console.log('Server says: Puzzle Solved!');
            // Handle the solved event response as needed
        });
    
        // Example: Listening for 'not solved' event
        socket.on('not solved', function () {
            console.log('Server says: Puzzle Not Solved!');
            // Handle the not solved event response as needed
        });
    });    
}

//create a grid in the html with a given size
function createGrid(size) {
    const table = document.createElement('table');

    for (let i = 0; i < size; i++) {
        const row = document.createElement('tr');

        for (let j = 0; j < size; j++) {
            const cell = document.createElement('td');
            row.appendChild(cell);
        }

        table.appendChild(row);
    }

    document.body.appendChild(table);
}

// add a listener to every cell on the grid to change the color when clicked
function addListeners() {
    const cells = document.querySelectorAll('td');

    cells.forEach(cell => {
        cell.addEventListener('click', () => {
            //if the cell is has an x, we don't want to change the color
            if (cell.innerHTML === 'X') {
                return;
            }
            cell.classList.add('black');
            // send the coordinates of the cell to the server
            const data = {y : cell.cellIndex - 1, x : cell.parentNode.rowIndex - 1};
            socket.emit('move', data);
        });
        // on right click, toggle the inner content to an x
        cell.addEventListener('contextmenu', (e) => {
            e.preventDefault();
            if (cell.innerHTML === 'X') {
                cell.innerHTML = '';
            } else {
                cell.innerHTML = 'X';
            }
        });
    });
}

function checkWin() {
    const button = document.createElement('button');
    button.innerHTML = 'Check';
    button.addEventListener('click', () => {
        // var socket = io.connect('127.0.0.1:8000');
        socket.emit('check');
    });
    document.body.appendChild(button);
}


// for each row and column, add the clues
const clues = JSON.parse(contextData.clues);
const row_clues = clues[0];
const col_clues = clues[1];

function addClues() {
    //add the row clues to the left of the grid
    const table = document.querySelector('table');
    //the rows of the table
    const rows = table.querySelectorAll('tr');
    //for each row, create a new td and add the clue
    for (let i = 0; i < row_clues.length; i++) {
        const clue = document.createElement('td');
        //add the classes
        clue.classList.add('row-clue');
        clue.classList.add('clue');
        //separator between the numbers in the clue
        clue.innerHTML = row_clues[i].join('  ');
        //add the clue to the row
        rows[i].insertBefore(clue, rows[i].firstChild);
    }

    // add the column clues on top of the grid
    const cells = table.querySelectorAll('td');
    // create a new tr for the column clues
    const row = document.createElement('tr');
    // add an empty td to the left of the clues because we need to offset the column clues
    const empty = document.createElement('td');
    empty.classList.add('clue');
    // make empty have no border
    empty.style.border = 'none';
    row.appendChild(empty);
    // for each column, create a new td and add the clue
    // same thing as for the rows
    for (let i = 0; i < col_clues.length; i++) {
        const clue = document.createElement('td');
        clue.classList.add('col-clue');
        clue.classList.add('clue');
        clue.innerHTML = col_clues[i].join('<br><br>');
        row.appendChild(clue);
    }
    //add the row to the table
    table.insertBefore(row, cells[0].parentNode);

}

connectSocket();
createGrid(contextData.size);
checkWin();
addListeners();
addClues();