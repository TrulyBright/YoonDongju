from flask import Flask, redirect
from views import render_template

def add_middlewares(app:Flask):
    app.register_error_handler(404, handle_404)
    app.register_error_handler(500, handle_500)
    app.register_error_handler(403, handle_403)
    app.register_error_handler(401, handle_401)

def handle_404(e):
    return render_template("error.html", code=404), 404

def handle_500(e):
    return render_template("error.html", code=500), 500

def handle_403(e):
    return render_template("error.html", code=403), 403

def handle_401(e):
    return render_template("error.html", code=401), 401