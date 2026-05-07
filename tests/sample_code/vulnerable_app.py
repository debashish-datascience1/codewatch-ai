"""
Deliberately vulnerable Flask application — used as input for CodeWatch AI demos.
DO NOT deploy this code. Every function below contains one or more known vulnerabilities.
"""

import hashlib
import logging
import os
import pickle
import sqlite3
import subprocess

import yaml
from flask import Flask, jsonify, redirect, render_template_string, request

app = Flask(__name__)

# CWE-798: Hardcoded credentials and weak secret key
SECRET_KEY = "dev_secret_123"
DB_PASSWORD = "admin123"
API_TOKEN = "tok_hardcoded_12345"

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# CWE-209: DEBUG mode exposes stack traces in production
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = SECRET_KEY


# ── CWE-89: SQL Injection ────────────────────────────────────────────────────
@app.route("/user")
def get_user():
    username = request.args.get("username", "")
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    # Direct string concatenation into SQL — classic SQL injection
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return jsonify(rows)


# ── CWE-78: OS Command Injection ─────────────────────────────────────────────
@app.route("/ping")
def ping_host():
    host = request.args.get("host", "")
    # shell=True with user input allows arbitrary command execution
    result = subprocess.check_output("ping -c 1 " + host, shell=True)
    return result.decode()


# ── CWE-79: Cross-Site Scripting (XSS) ───────────────────────────────────────
@app.route("/hello")
def hello():
    name = request.args.get("name", "World")
    # User input rendered directly into HTML without escaping
    template = f"<h1>Hello, {name}!</h1>"
    return render_template_string(template)


# ── CWE-22: Path Traversal ───────────────────────────────────────────────────
@app.route("/file")
def read_file():
    filename = request.args.get("name", "")
    # No sanitization — attacker can request ../../etc/passwd
    with open(f"./uploads/{filename}") as f:
        return f.read()


# ── CWE-327: Broken Cryptography ─────────────────────────────────────────────
@app.route("/register", methods=["POST"])
def register():
    password = request.form.get("password", "")
    # MD5 is cryptographically broken for password storage
    password_hash = hashlib.md5(password.encode()).hexdigest()
    logger.info(f"Registering user with password: {password}")  # CWE-532: logs password
    return jsonify({"hash": password_hash})


# ── CWE-502: Insecure Deserialization ────────────────────────────────────────
@app.route("/load", methods=["POST"])
def load_data():
    raw = request.get_data()
    # pickle.loads on untrusted data allows arbitrary code execution
    data = pickle.loads(raw)
    return jsonify(data)


# ── CWE-502: yaml.load without SafeLoader ────────────────────────────────────
@app.route("/config", methods=["POST"])
def load_config():
    raw_yaml = request.get_data(as_text=True)
    # yaml.load() can execute arbitrary Python via !!python/object tags
    config = yaml.load(raw_yaml)
    return jsonify(config)


# ── CWE-918: Server-Side Request Forgery (SSRF) ───────────────────────────────
@app.route("/fetch")
def fetch_url():
    import requests as req
    url = request.args.get("url", "")
    # No URL validation — attacker can target internal services
    resp = req.get(url)
    return resp.text


# ── CWE-306: Missing Authentication on Admin Endpoint ────────────────────────
@app.route("/admin/delete_user", methods=["POST"])
def delete_user():
    # No authentication check — anyone can delete users
    user_id = request.form.get("user_id")
    conn = sqlite3.connect("users.db")
    conn.execute(f"DELETE FROM users WHERE id = {user_id}")  # also SQL injection
    conn.commit()
    return jsonify({"deleted": user_id})


# ── CWE-601: Open Redirect ────────────────────────────────────────────────────
@app.route("/redirect")
def open_redirect():
    next_url = request.args.get("next", "/")
    # No validation — attacker can redirect to phishing sites
    return redirect(next_url)


if __name__ == "__main__":
    app.run(debug=True)
