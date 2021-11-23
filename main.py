from flask import Flask
import db
import routes

db.initalize("notices")
db.initalize("users")
app = Flask("YoonDong-ju", static_url_path="")
app.config["UPLOAD_DIR"] = "./uploaded" # "/uploaded"가 아니라 "./uploaded"임에 유의.
routes.setup_routes(app)

if __name__ == "__main__": # 로컬에서 실행
    app.run()