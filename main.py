from flask import Flask
from routes import setup_routes

app = Flask("YoonDong-ju")
setup_routes(app)

if __name__ == "__main__": # 로컬에서 실행
    app.run()