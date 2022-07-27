# Backend
## Run
1. `pip install -r requirements.txt`
1. `gunicorn -k uvicorn.workers.UvicornWorker main:app -w (할당할 스레드 수)`
## Test
1. `test.env` 파일을 생성하고 다음 값을 넣습니다.
    - `test_portal_id=연세포탈 ID(즉 학번)`
    - `test_portal_pw="연세포탈 비번"`
    - `test_real_name="견본 실명"`
    - `test_username="견본 ID"`
    - `test_password="견본 비번. main.py에서 정한 정규표현식 패턴과 맞아야 합니다."`
    - `test_new_pw="변경용 견본 비번. '비밀번호 찾기'가 이 비밀번호를 이용하여 시험됩니다."`
1. `prod.env` 파일을 생성하고 다음 값을 넣습니다.
    - `authjwt_secret_key="무작위로 생성된 32-digit hexadecimal. production 배포 중에는 바뀌면 안 됩니다.`
1. 이후 `pytest`를 실행합니다.