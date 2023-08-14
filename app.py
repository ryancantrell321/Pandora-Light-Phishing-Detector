# importing necessary modules:

import requests as rq
import socket as sk
from flask import Flask, render_template, request

# Initializing Flask Web Application:
app = Flask(__name__)

status_1 = True
status_2 = False


# Defining top-level domain and IP Address Constraints using the socket module:
def valid_url(domain):
    try:
        sk.gethostbyname(domain)
        return status_1
    except sk.gaierror:
        return status_2


def valid_ip_address(ip_address):
    try:
        sk.inet_aton(ip_address)
        return status_1
    except sk.error:
        return status_2


# Configuring API Endpoint for URLScan:
API_endpoint = "https://urlscan.io/api/v1/scan/"
API_key = "648b27e4-8f59-4f65-be57-401356fc7afb"


# Configuring Phishing Algorithm:

def phishing_algorithm(url):
    headers = {"API-KEY": API_key}
    pl = {"url": url}
    rp = rq.post(API_endpoint, headers=headers, json=pl)

    if rp.status_code == 200:
        result_json = rp.json()
        return "Phishing" in result_json.get("verdicts", {}).values()
    return status_2


# Configuring the response feedback on the HTML file:
@app.route("/", methods=["GET", "POST"])
def index_html():
    result = None
    correct_input = status_1

    if request.method == "POST":
        url = request.form["url"]
        if valid_url(url) or valid_ip_address(url):
            result = phishing_algorithm(url)
        else:
            correct_input = status_2
    return render_template("index.html", result=result, correct_input=correct_input)


if __name__ == "__main__":
    app.run(debug=True)
