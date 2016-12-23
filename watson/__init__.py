from flask import Flask


app = Flask(__name__)
from watson.views.site import site

app.register_blueprint(site)
