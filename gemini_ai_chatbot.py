from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Configure the API key
genai.configure(api_key="AIzaSyCPJIlX1AAv5yOr4NzRTZC3rqDi6Cvwacw")

# Load the Gemini Pro model and start a chat session
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])


@app.route('/chat', methods=['POST'])
def chat_route():
    # Extract the message from the request
    message = request.json.get('message')

    # Send the message to the Gemini Pro model and get the response
    response = chat.send_message(message, stream=True)

    # Process the response from the model
    response_text = ""
    for chunk in response:
        response_text += f"{chunk.text}\n"

    # Return the response as JSON
    return jsonify({'response': response_text})


@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Chatbot using Gemini AI</title>
            <style>
                body {
                    background: linear-gradient(to right, #ece9e6, #ffffff);
                    font-family: Arial, sans-serif;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    width:auto
                    margin: 0;
                    # border:1px solid blue;
                    background:pink;
                }
                h1 {
                    color: #333;
                }
                form {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    # border:1px solid blue;
                }
                input[type="text"] {
                    padding: 10px;
                    # margin-bottom: 10px;
                    margin:auto;
                    background-color:aqua;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    width: 300px;
                }
                button {
                margin:10px;
                    padding: 10px 20px;
                    color: blue;
                    background:violet;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                    font-size: 16px;
                }
                button:hover {
                    background-color: #0056b3;
                }
                #response {
                    # margin-top: 20px;
                    margin:auto;
                    background-color:aqua;
                    padding: 10px;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    width: 300px;
                    # background-color: #f9f9f9;
                    min-height: 50px;
                    text-align: left;
                }
            </style>
        </head>
        <body>
            <div>
                <h1>Chatbot using Gemini AI</h1>
                <form action="/chat" method="post" id="chatForm">
                    <input type="text" name="message" id="message" placeholder="Type your message here" required>
                    <button type="submit">Send</button>
                </form>
                <div id="response"></div>
            </div>
            <script>
                document.getElementById('chatForm').onsubmit = async (e) => {
                    e.preventDefault();
                    const message = document.getElementById('message').value;
                    const responseDiv = document.getElementById('response');
                    responseDiv.innerHTML = 'Loading...';
                    const response = await fetch('/chat', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ message })
                    });
                    const result = await response.json();
                    if (response.ok) {
                        responseDiv.innerHTML = result.response;
                    } else {
                        responseDiv.innerHTML = 'Error: ' + result.error;
                    }
                };
            </script>
        </body>
    </html>
    '''


if __name__ == '__main__':
    app.run(debug=True)