
from flask import render_template
from blog import app

@app.route("/base")
def index():
   return render_template("base.html")