var socket = null;
var last_cell = null;
// connect to the socket
function connectSocket() {
    document.addEventListener('DOMContentLoaded', function () {
        // connect to the socket
        socket = io.connect('127.0.0.1:8000');

        socket.on('solved', function () {
            // Handle the solved event response as needed
        });

        socket.on('not solved', function () {
            // Handle the not solved event response as needed
        });

        socket.on("game over", function () {
            // Handle the game over event response as needed
            window.location.href = '/game_over';
        });    
        socket.on("incorrect", function () {
            // Handle the incorrect event response as needed
            last_cell.classList.remove('black');
            last_cell.classList.add("red");
        });
        socket.on("solved", function () {
            // Handle the solved event response as needed
            window.location.href = '/solved';
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
            // if the cell is already black, do nothing
            if (cell.classList.contains('black')) {
                return;
            }
            // if the cell is white, make it black
            cell.classList.add('black');
            // if the cell is already black, we don't want to send anything to the server
            const data = {y : cell.cellIndex - 1, x : cell.parentNode.rowIndex - 1};
            socket.emit('move', data);
            last_cell = cell;
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
addListeners();
addClues();

// after every five cells, add a border to the grid
const cells = document.querySelectorAll('td');
// for each row except the first one, add a border after every 5 cells
// iterate through the tr's
trs = document.querySelectorAll('tr');
// for each tr, iterate through the td's
// start at 1 because we don't want to add a border to the first td
for (let i = 1; i < trs.length; i++) {
    tr = trs[i];
    for (let i = 1; i < tr.children.length; i++) {
        // if the index is divisible by 5, add a border
        if (i % 5 === 0) {
            tr.children[i].style.borderRight = '6px solid black';
        }
    }
}

// on every 5th tr (except the first one), add a border to the bottom
for (let i = 1; i < trs.length; i++) {
    if (i % 5 === 0) {
        // add a border to every td in the tr except the first one
        for (let j = 1; j < trs[i].children.length; j++) {
            trs[i].children[j].style.borderBottom = '6px solid black';
        }
    }
}