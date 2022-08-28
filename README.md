# Backend
## Production Settings
`prod.env` 파일을 생성하고 다음 값을 넣습니다.
```
jwt_secret=무작위로 생성된 32-digit hexadecimal. production 배포 중에는 바뀌면 안 됩니다.`
allow_origins=CORS용 allow-origins. JSON Array 꼴이어야 합니다.
driver_path=Selenium용 driver의 Absolute Path.
ncloud_access_key=Naver Cloud Platform access key.
ncloud_secret_key=Naver Cloud Platform secret key.
ncloud_sms_service_id=Naver Cloud Platform SENS SMS Service ID.
ncloud_sms_service_phone_number=Naver Cloud Platform SENS SMS 서비스에 등록된 발신번호.
```
## Run
1. 위에 있는 `Production Settings`를 완료합니다.
1. `pip install -r requirements.txt`를 실행합니다.
1. `gunicorn -k uvicorn.workers.UvicornWorker main:app -w (할당할 스레드 수)`를 실행합니다.
## Test
1. 위에 있는 `Production Settings`를 완료합니다.
2. `test.env` 파일을 생성하고 다음 값을 넣습니다.
```
test_portal_id=연세포탈 ID(즉 학번)
test_portal_pw=연세포탈 비번
test_real_name=견본 실명
test_username=견본 ID
test_password=견본 비번. main.py에서 정한 정규표현식 패턴과 맞아야 합니다.
test_new_pw=변경용 견본 비번. '비밀번호 찾기'가 이 비밀번호를 이용하여 시험됩니다.
test_HR_chief_tel=견본 전화번호. 실용 환경에서는 인사행정팀장의 전화번호가 됩니다.
```
3. 이후 `pytest`를 실행합니다.
## API Reference
https://api.yonseimunhak.com/docs

https://api.yonseimunhak.com/redoc
## Notes
- 500 에러인데 클라이언트에서는 CORS 에러로 보일 때가 종종 있으니 조심하세요.
## Code Convention
[Black](https://github.com/psf/black)
