from flask import Flask
import db
import auth
import routes
import middlewares

db.initalize()
app = Flask("YoonDong-ju", static_url_path="/static")
app.config["UPLOAD_DIR"] = "./uploaded" # "/uploaded"가 아니라 "./uploaded"임에 유의.
routes.setup_routes(app)
middlewares.add_middlewares(app)
auth.setup_auth(app)

if __name__ == "__main__": # 로컬에서 실행
    app.run(debug=True)