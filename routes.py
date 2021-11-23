from flask import Flask
import views

def setup_routes(app: Flask):
    app.add_url_rule("/", view_func=views.index)