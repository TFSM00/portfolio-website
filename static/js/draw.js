const grid = document.querySelector(".grid");
let rows = document.getElementsByClassName("gridRow");
let cells = document.getElementsByClassName("cell");
const DEFAULT_GRID_SIZE = 16;
const DEFAULT_COLOR = "gray";

let currentSize = DEFAULT_GRID_SIZE
const sizeDisplay = document.querySelector("p")

let mouseDown = 0;
document.body.onmousedown = () => mouseDown = 1;
document.body.onmouseup = () => mouseDown = 0;


function makeGrid(size) {
    grid.style.gridTemplateColumns = `repeat(${size}, 1fr)`
    grid.style.gridTemplateRows = `repeat(${size}, 1fr)`
  
    for (let i = 0; i < size * size; i++) {
        const gridElement = document.createElement('div');
        gridElement.classList.add("cell");
        gridElement.addEventListener('mouseover', colorCell);
        gridElement.addEventListener('mousedown', colorCell);
        grid.appendChild(gridElement);
    }
  }

function colorCell(e){   
    if (e.type === 'mouseover' && !mouseDown) return
    if (e.target.className === "cell") {
        e.target.style.backgroundColor = DEFAULT_COLOR;
    }
}
 
function clearGrid() {
    grid.innerHTML = "";
    makeGrid(currentSize);
}

function changeSize() {
    const sizeDisplay = document.querySelector("p");
    let valid_ans = false;
    const promptText = "Grid Size: Enter a number between 1 and 100";
    while (!valid_ans) {
        let input = prompt(promptText);
        
        if (input>=1 && input<=100) {
            valid_ans = true;
            currentSize = input;
            break;
        } 
    }

    sizeDisplay.textContent = `Current Grid Size: ${currentSize} x ${currentSize}`;
    grid.innerHTML = "";
    makeGrid(currentSize);
}


const squares = document.querySelectorAll(".cell");

squares.forEach( (square) => {
    square.addEventListener("mousedown", event => {
        paintEvent = colorCell(event, DEFAULT_COLOR);
        if(event.buttons == 1){
            window.addEventListener("mouseover", (e) => {
                colorCell(e, DEFAULT_COLOR)
            })
        }
    });
});


window.onload = () => {
    sizeDisplay.textContent = `Current Grid Size: ${DEFAULT_GRID_SIZE} x ${DEFAULT_GRID_SIZE}`
    makeGrid(DEFAULT_GRID_SIZE);
}