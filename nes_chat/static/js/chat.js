
socket = io();

if (!socket) {
    alert("socket init failed, please refresh the page to try again.");
}

function make_msg_node(msg, nickname, room, ts) {
    // msg wrapper
    const section = document.createElement("section");
    section.classList.add("message");
    if (nickname === document.querySelector('#nickname').value) {
        section.classList.add("-left");
    } else {
        section.classList.add("-right");
    }

    // icon
    const i = document.createElement("i");
    i.classList.add("nes-bcrikko"); // to be changed after avatar feature is finished.
    i.classList.add("is-small");

    // balloon
    const balloon = document.createElement("div");
    balloon.classList.add("nes-balloon");
    if (nickname === document.querySelector('#nickname').value) {
        balloon.classList.add("from-left");
    } else {
        balloon.classList.add("from-right");
    }

    // msg body inside balloon
    const p_name = document.createElement("p");
    const p_msg = document.createElement("p");
    p_name.innerHTML = `${nickname} ${new Date(ts * 1000).toLocaleString()}`;
    p_msg.innerHTML = msg;
    balloon.appendChild(p_name);
    balloon.appendChild(p_msg);


    // append icon and balloon to wrapper
    if (nickname === document.querySelector('#nickname').value) {
        section.appendChild(i);
        section.appendChild(balloon);
    } else {
        section.appendChild(balloon);
        section.appendChild(i);
    }

    return section;
}


socket.on('connect', function () {
    const nickname = document.querySelector('#nickname').value;
    const room = document.querySelector('#room').value;
    const message_form = document.querySelector(".message-form");
    const msg = document.querySelector("#msg");
    const message_list = document.querySelector(".message-list");
    const user_list = document.querySelector(".user-list");
    const online_count = document.querySelector(".online-count");
    const btn_send = document.querySelector("#btn-send");

    socket.emit('join', nickname, room);

    message_form.addEventListener("submit", function (e) {
        e.preventDefault();
        if (msg.value.trim() === "") {
            return false;
        }

        socket.emit('chat-msg', msg.value, nickname, room);
        msg.value = "";
    });

    socket.on('chat-msg', function (msg, nickname, room, ts) {
        const msg_node = make_msg_node(msg, nickname, room, ts);
        message_list.appendChild(msg_node);
        message_list.scrollTop = message_list.scrollHeight; // auto scroll to bottom
    });

    socket.on('update-users-list', function (users) {
        user_list.innerHTML = "";
        for (const user of users) {
            const li = document.createElement('li');
            li.textContent = user;
            user_list.appendChild(li);
        }
        online_count.textContent = users.length;
    });

    msg.addEventListener("keypress", function (e) {
        const key = e.keyCode;
        if (key === 13) {
            e.preventDefault();
            btn_send.click();
        }
    });
});

