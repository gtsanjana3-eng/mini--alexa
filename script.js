async function sendMessage(messageText = null) {

    let message;

    if (messageText) {
        message = messageText;
    } else {
        message = document.getElementById('message').value;
    }

    const response = await fetch('/chat', {

        method: 'POST',

        headers: {
            'Content-Type': 'application/json'
        },

        body: JSON.stringify({
            message: message
        })
    });

    const data = await response.json();

    document.getElementById('chatbox').innerHTML +=
        "<p><b>You:</b> " + message + "</p>" +
        "<p><b>Alexa:</b> " + data.reply + "</p>";
}



function startVoice() {

    const SpeechRecognition =
        window.SpeechRecognition ||
        window.webkitSpeechRecognition;

    if (!SpeechRecognition) {

        alert("Voice recognition not supported");

        return;
    }

    const recognition =
        new SpeechRecognition();

    recognition.lang = 'en-US';

    recognition.start();

    recognition.onresult = function(event) {

        const voiceText =
            event.results[0][0].transcript;

        document.getElementById('message').value =
            voiceText;

        sendMessage(voiceText);
    };

    recognition.onerror = function(event) {

        alert("Voice error: " + event.error);
    };
}