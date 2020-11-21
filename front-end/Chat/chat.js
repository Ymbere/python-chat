// Variables
let namespace = "ws://127.0.0.1:5000/lobby";
let socket = io(namespace);
let messageToSend = "";
let messageResponses = "";
let messageResponseLen = messageResponses.length;
let chatHistory = $(".chat-history");
let button = document.getElementById("send-message");
let textarea = $("#message-to-send");
let chatHistoryList = chatHistory.find("ul");
const user = localStorage.getItem("user")

const getCurrentTime = () => {
    return new Date()
        .toLocaleTimeString()
        .replace(/([\d]+:[\d]{2})(:[\d]{2})(.*)/, "$1$3");
};

const addMessage = () => {
    messageToSend = textarea.val();
    // Send message if is not empty
    if (messageToSend.trim() !== "") {
        currentTime = getCurrentTime();
        socket.emit(
            "lobby_publisher",
            { data: messageToSend, time: currentTime, owner: user }
        );
        textarea.val("")
    }
};

const addMessageEnter = (event) => {
    // enter was pressed
    if (event.keyCode === 13) {
        addMessage();
    }
}

// Events
button.addEventListener('click', () => addMessage())
textarea.on("keyup", addMessageEnter.bind(this));

let templateResponse = Handlebars.compile(
    $("#message-response-template").html()
);

let templateSend = Handlebars.compile(
    $("#message-template").html()
)

const keepMessagesAtFifty = () => {
    if (chatHistoryList.children().length === 50) {
        console.log("Passou na função que remove a mensagem")
        chatHistoryList.children().eq(0).remove();
    }
}

const buildChat = () => {
    const owner = messageResponses.owner
    if (owner !== user) {
        let parsedResponse = {
            response: messageResponses.data,
            time: messageResponses.time,
            owner: messageResponses.owner
        };
        keepMessagesAtFifty()
        chatHistoryList.append(templateResponse(parsedResponse));
    } else {
        let parsedMessage = {
            messageOutput: messageResponses.data,
            time: messageResponses.time,
            owner: messageResponses.owner
        }
        keepMessagesAtFifty()
        chatHistoryList.append(templateSend(parsedMessage));
    }
};

const scrollToBottom = () => {
    chatHistory.scrollTop(chatHistory[0].scrollHeight);
}

//Socket IO stuff
socket.on("connect", function () {
    console.warn("on connect");
});

socket.on("lobby_consumer", function (msg, cb) {
    console.log("array de mensagens agora", messageResponses);
    console.log("received");
    console.log("Mensagem recebida: ", JSON.stringify(msg));
    messageResponses = msg;
    buildChat();
    scrollToBottom()
    console.warn("Novo array de mensagens: ", messageResponses);
    if (cb) cb();
});
