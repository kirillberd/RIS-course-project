from flask import Flask


app = Flask(__name__)

@app.route("/")
def main_menu():
    return "Test"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000, debug=True)