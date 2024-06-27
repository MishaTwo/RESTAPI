import os
from .database import session, User
from . import app
from flask import render_template, request, redirect, jsonify, json
from dotenv import load_dotenv


@app.route("/swagger.json")
def swagger():
    with open("swagger.json", "r") as file:
        return jsonify(json.load(file))