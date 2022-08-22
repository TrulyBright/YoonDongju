import requests
import json
import urllib.parse
import hashlib
import hmac
import base64
import requests
import time
import models
import crud
from settings import get_settings
from sqlalchemy.orm import Session


def make_signature(access_key: str, secret_key: str, timestamp: str, uri: str):
    secret_key = bytes(secret_key, "UTF-8")
    message = bytes(f"POST {uri}\n{timestamp}\n{access_key}", "UTF-8")
    signingKey = base64.b64encode(
        hmac.new(secret_key, message, digestmod=hashlib.sha256).digest()
    )
    return signingKey


def send_new_club_member_message(
    club_member: models.ClubMember, db: Session, tel: str, invite_informal_chat: bool
):
    print("asdasdf")
    settings = get_settings()
    url = "https://sens.apigw.ntruss.com"
    uri = f"/sms/v2/services/{urllib.parse.quote(settings.ncloud_sms_service_id)}/messages"
    timestamp = str(int(time.time() * 1000))
    data = json.dumps(
        {
            "type": "SMS",
            "from": settings.ncloud_sms_service_phone_number,
            "content": f"""{club_member.name}/{club_member.student_id}/{club_member.dept_and_major}/{tel}/잡담방 초대 {'O' if invite_informal_chat else 'X'}""",
            "messages": [{"to": crud.get_club_information(db=db)["HR_chief_tel"]}],
        }
    )
    response = requests.post(
        url=url + uri,
        data=data,
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "x-ncp-apigw-timestamp": timestamp,
            "x-ncp-iam-access-key": settings.ncloud_access_key,
            "x-ncp-apigw-signature-v2": make_signature(
                settings.ncloud_access_key, settings.ncloud_secret_key, timestamp, uri
            ),
        },
    )
    return response.status_code == 202
