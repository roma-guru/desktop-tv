from base64 import b64encode
from io import BytesIO
import time

# import ngrok
import numpy as np

# from dotenv import load_dotenv
from flask import Flask, Response, render_template, request
from mss import mss, tools

from jpeg import to_jpeg

# load_dotenv()
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/screen")
def screen():
    mon_num = int(request.args.get("mon_num", 0))
    fmt = request.args.get("fmt", "png")

    def frames():
        with mss() as sct:
            mon = sct.monitors[mon_num]
            while True:
                shot = sct.grab(mon)
                if fmt == "png":
                    img_bytes = tools.to_png(shot.rgb, shot.size)
                else:
                    img_bytes = to_jpeg(shot.rgb, shot.size)

                yield (
                    f"--frame\r\nContent-Type: image/{fmt}\r\n"
                    "Content-Size:%d\r\n\r\n%s\r\n".encode()
                    % (len(img_bytes), img_bytes)
                )

    if fmt not in ["png", "jpeg", "jpg"]:
        return "Invalid format", 400
    return Response(frames(), mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == "__main__":
    # listener = ngrok.forward("localhost:8080", authtoken_from_env=True)
    # print(f"Ingress established at: {listener.url()}")
    app.run(port=8080, debug=True)
