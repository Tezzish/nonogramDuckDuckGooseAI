



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
            cell.classList.add('black');
            // send the coordinates of the cell to the server
            const data = {y : cell.cellIndex, x : cell.parentNode.rowIndex};
            socket.emit('move', data);
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
    console.log("checkWin");
}

var socket = null;
document.addEventListener('DOMContentLoaded', function () {
    socket = io.connect('127.0.0.1:8000');
});

createGrid(contextData.size);
checkWin();
addListeners();