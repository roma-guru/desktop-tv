from base64 import b64encode
from io import BytesIO

import ngrok
import numpy as np
from dotenv import load_dotenv
from flask import Flask, Response, render_template, request
from mss import mss, tools

#from jpeg import to_jpeg

load_dotenv()
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/screen")
def screen():
    def frames():
        with mss() as sct:
            mon = sct.monitors[0]
            while True:
                shot = sct.grab(mon)
                img_bytes = tools.to_png(shot.rgb, shot.size)
                # img_bytes = to_jpeg(np.array(shot)[:, :, :3])
                yield (
                    b"--frame\r\nContent-Type: image/png\r\nContent-Size:%d\r\n\r\n%s\r\n"
                    % (len(img_bytes), img_bytes)
                )

    return Response(frames(), mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == "__main__":
    # listener = ngrok.forward("localhost:8080", authtoken_from_env=True)
    # print(f"Ingress established at: {listener.url()}")
    app.run(port=8080, debug=True)
