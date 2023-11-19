// Establish a WebSocket connection to the server
var socket = io.connect('http://' + document.domain + ':' + location.port);

// Function to add messages to the chat window
function addMessageToChat(msg, isSelf) {
    var chatMessages = document.getElementById('chat-messages');

    // Sample format for received and sent messages
    var message = '<div style="margin-bottom: 10px;">' +
                        '<div style="display: inline-block; background-color: ' + (isSelf ? 'white' : '#F0F8FF') + '; color: black; padding: 10px; border-radius: 10px;">' +
                            msg.message +
                            '<br>' +
                            '<span style="font-size: 10px;">' + (isSelf ? 'You' : msg.name) + '</span>' +
                        '</div>' +
                    '</div>';

    // Append the message to the chat area
    chatMessages.innerHTML += message;

    // Scroll to the bottom of the chat area
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Function to send a message to the server
function sendMessage() {
    var messageInput = document.getElementById('message-input');
    var message = messageInput.value.trim();

    if (message !== '') {
        // Emit the message to the server
        socket.emit('event', { message: message });

        // Add the sent message to the chat window
        addMessageToChat({ message: message }, true);

        // Clear the message input
        messageInput.value = '';
    }
}

// Event listener for receiving messages from the server
socket.on('message response', function (msg) {
    // Add the received message to the chat window
    addMessageToChat(msg, false);
});

// Additional functions or event listeners can be added as needed
// Remember to adjust the HTML accordingly and include this script in your HTML
