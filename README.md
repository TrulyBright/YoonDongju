# Project YoonDong-ju: the official website of Yonsei Literature Club or 연세문학회
> 하늘을 우러러 한 점 버그가 없기를!
## Requirements
- npm
- nodejs
- python >= 3.10
## Solutions
- FastAPI
- Vue
- SQLite
## Run
1. `npm install`
1. `pip install -r requirements.txt`
1. `uvicorn main:app`
## Test
1. `test.env` 파일을 프로젝트 최상위 디렉토리에 생성하고 다음 값을 넣습니다.
    - `test_portal_id=연세포탈 ID(즉 학번)`
    - `test_portal_pw="연세포탈 비번"`
    - `test_real_name="견본 실명"`
    - `test_username="견본 ID"`
    - `test_password="견본 비번"`
1. 이후 프로젝트 최상위 디렉토리에서 `pytest`를 실행합니다.