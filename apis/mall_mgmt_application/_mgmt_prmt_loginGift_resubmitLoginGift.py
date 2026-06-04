import os

from util.client import client

data = {
    "id": 0,  # id
    "remarks": "",  # 备注
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_loginGift_resubmitLoginGift(data=data, headers=headers):
    """
    再次提交登录有礼活动
    /mgmt/prmt/loginGift/resubmitLoginGift

    参数说明:
    - id: id
    - remarks: 备注
    """

    url = "/mgmt/prmt/loginGift/resubmitLoginGift"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
