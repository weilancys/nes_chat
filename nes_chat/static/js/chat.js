
socket = io();

if (!socket) {
    alert("socket init failed, please refresh the page to try again.");
}

socket.on('connect', function () {
    const nickname = document.querySelector('#nickname').value;
    const room = document.querySelector('#room').value;

    socket.emit('join', nickname, room);
});