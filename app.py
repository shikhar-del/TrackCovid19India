from flask import Flask,request,render_template,redirect
import requests
app = Flask(__name__)

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_cases")
def get_cases():
    #contact API
    response = requests.get("https://api.covid19india.org/data.json")
    response.raise_for_status()

    obj = response.json()

    return render_template("get_cases.html",obj=obj["statewise"])

@app.route("/zones",methods=["GET","POST"])
def zone():
    if request.method == "GET":
        return render_template("zones.html")

    district = request.form["district"]
    res = requests.get("https://api.covid19india.org/zones.json")
    res.raise_for_status()

    obj = res.json()
    dist = []

    for row in obj["zones"]:
        if (district.lower()) in (row["district"].lower()):
            dist.append(row)

    return render_template("get_zones.html",obj = dist)

@app.route("/services",methods=["GET","POST"])
def services():
    if request.method == "GET":
        return render_template("services.html")

    res = requests.get("https://api.covid19india.org/resources/resources.json")
    res.raise_for_status()

    obj = res.json()
    dist = request.form["district"]
    x = []
    for row in obj["resources"]:
        # if (row["city"].lower()).startswith(dist.lower()):
        if dist.lower() in row["city"].lower():
            x.append(row)

    return render_template("get_services.html",obj=x)

@app.route("/credits")
def credits():
    return render_template("credits.html")