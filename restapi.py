from flask import Flask, request
from backend1 import handle_query, detect_intent, generate_sql_query, get_chatgpt_response, get_packages2
app = Flask(__name__)

@app.route("/travelbot",  methods=["POST"])
def travelz():
    
    data = request.get_json()
    prompt = data.get("prompt")
    return handle_query(prompt)

@app.route("/intentdetect",  methods=["POST"])
def intent():
    
    data = request.get_json()
    prompt = data.get("prompt")
    output =  detect_intent(prompt)
    if output == "Database":
        return "Database"
    else:
        return "General Knowledge"
    
@app.route("/sqlquery",  methods=["POST"])
def sqlquery():
    
    data = request.get_json()
    prompt = data.get("prompt")
    return generate_sql_query(prompt)

@app.route("/gptresponse",  methods=["POST"])
def gptresponse():
    
    data = request.get_json()
    prompt = data.get("prompt")
    return get_chatgpt_response(prompt)

@app.route("/getpackage",  methods=["POST"])
def getpackage():
    
    data = request.get_json()
    prompt = data.get("prompt")
    return get_packages2(prompt)

if __name__ == "__main__":
    app.run(host="localhost", debug=True, port=5100)


