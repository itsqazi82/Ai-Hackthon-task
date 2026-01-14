const socket = io();
const canvas = document.getElementById("board");
const ctx = canvas.getContext("2d");

let drawing = false;

// mouse events
canvas.addEventListener("mousedown", () => drawing = true);
canvas.addEventListener("mouseup", () => drawing = false);

canvas.addEventListener("mousemove", (e) => {
    if (!drawing) return;

    const data = {
        x: e.offsetX,
        y: e.offsetY,
        color: "black",
        stroke: 2
    };

    drawPoint(data);
    socket.emit("draw", data);   // 👈 JSON backend ko bheja
});

// local draw
function drawPoint(data) {
    ctx.fillStyle = data.color;
    ctx.beginPath();
    ctx.arc(data.x, data.y, data.stroke, 0, Math.PI * 2);
    ctx.fill();
}

// receive from others
socket.on("draw", (data) => {
    drawPoint(data);   // 👈 JSON yahan use hota hai
});
