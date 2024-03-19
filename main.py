#!/usr/bin/env python3
from flask import app
import mss


@app.get("/")
def home():
    return


@app.get("/screen")
def screen(num: int = 0):
    return
