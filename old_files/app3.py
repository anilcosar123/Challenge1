from flask import Flask

app3 = Flask(__name__)

@app3.route("/")
def main():
    return 'Welcome to hellsgdgs'

if __name__ == "__main__":
    app3.run(debug=True, host='0.0.0.0', port='80')