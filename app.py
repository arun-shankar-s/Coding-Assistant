from agent import run_agent
from tools import memory
from flask import Flask,render_template,request,jsonify

app=Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat",methods=["POST"])
def chat():
    user_message=request.json.get("message")
    response=run_agent(user_message)
    return jsonify({
        "response":response
    })

@app.route("/memory")
def get_memory():
    return jsonify({
        "memory":memory.notes
    })

if __name__=="__main__":
    app.run(debug=True)