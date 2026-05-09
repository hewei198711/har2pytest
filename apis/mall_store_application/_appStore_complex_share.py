import os

from util.client import client

data = {
    "id": 0,  # 活动id
    "shareType": 0,  # 分享类型:1-保存到相册,2-分享给朋友或群
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _appStore_complex_share(data=data, headers=headers):
    """
    分享签约购活动4.0
    /appStore/complex/share

    参数说明:
    - id: 活动id
    - shareType: 分享类型:1-保存到相册,2-分享给朋友或群
    """

    url = "/appStore/complex/share"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
