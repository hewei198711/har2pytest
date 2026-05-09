import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_msg_goEasy_getEasyOTP(headers=headers):
    """
    获取OTP
    /appStore/msg/goEasy/getEasyOTP
    """

    url = "/appStore/msg/goEasy/getEasyOTP"
    with client.get(url=url, headers=headers) as r:
        return r
