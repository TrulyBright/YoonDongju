# Backend
## Run
1. `pip install -r requirements.txt`
1. `uvicorn main:app`
## Test
1. `test.env` 파일을 생성하고 다음 값을 넣습니다.
    - `test_portal_id=연세포탈 ID(즉 학번)`
    - `test_portal_pw="연세포탈 비번"`
    - `test_real_name="견본 실명"`
    - `test_username="견본 ID"`
    - `test_password="견본 비번. main.py에서 정한 정규표현식 패턴과 맞아야 합니다."`
1. `prod.env` 파일을 생성하고 다음 값을 넣습니다.
    - `jwt_secret="무작위로 생성된 hexadecimal digit 32자리. production 배포 중에는 바뀌면 안 됩니다."`
1. 이후 `pytest`를 실행합니다.