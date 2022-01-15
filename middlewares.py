from flask import Flask, redirect
from views import render_template

def add_middlewares(app:Flask):
    app.register_error_handler(404, handle_404)

def handle_404(e) -> str:
    return render_template("404.html"), 404
