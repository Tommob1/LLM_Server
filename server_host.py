from flask import Flask, request, jsonify, render_template_string
from LLM_Server_Access import query_server

app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>NEURON Interface</title>
            <style>
                body { background-color: #000000; color: #00ff00; font-family: 'Courier New', monospace; }
                textarea, input { background-color: #333333; color: #00ff00; border: 1px solid #555; font-family: 'Courier New', monospace; }
                .container { width: 80%; margin: 0 auto; text-align: center; }
                .input-area, .output-area { margin: 20px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>NEURON Interface</h1>
                <div class="input-area">
                    <textarea id="input_text" rows="4" cols="50" placeholder="Enter your query here..."></textarea>
                    <br><br>
                    <button onclick="sendQuery()">Send</button>
                </div>
                <div class="output-area">
                    <textarea id="output_text" rows="20" cols="100" readonly></textarea>
                </div>
            </div>
            <script>
                function sendQuery() {
                    var inputText = document.getElementById('input_text').value;
                    fetch('/query', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ query: inputText })
                    }).then(response => response.json())
                      .then(data => {
                          document.getElementById('output_text').value += "USER: " + inputText + "\\n";
                          document.getElementById('output_text').value += "AI: " + data.response + "\\n\\n";
                      });
                }
            </script>
        </body>
        </html>
    """)

@app.route('/query', methods=['POST'])

def query():
    data = request.json
    user_input = data['query']
    response = query_server(user_input)
    return jsonify({'response' : response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)