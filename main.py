from io import BytesIO
from base64 import b64encode

from dotenv import load_dotenv
from flask import Flask, render_template, send_file, request
from mss import mss
import ngrok

load_dotenv()
app = Flask(__name__)
sct = mss()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/screen")
def screen():
    num = 0
    fname = next(sct.save(mon=num, output="/tmp/mon-{mon}.png"))
    with open(fname, "rb") as scr:
        return (
            "<img src='data:image/png;base64,"
            f"{b64encode(scr.read()).decode()}' alt='Desktop TV'/>"
        )


if __name__ == "__main__":
    listener = ngrok.forward("localhost:8080", authtoken_from_env=True)
    print(f"Ingress established at: {listener.url()}")
    app.run(port=8080, debug=True)
