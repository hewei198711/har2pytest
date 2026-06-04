import os

from util.client import client

data = {
    "endTime": "",  # 结束时间
    "id": 0,  # 活动id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_loginGift_modifyEndTime(data=data, headers=headers):
    """
    修改结束时间
    /mgmt/prmt/loginGift/modifyEndTime

    参数说明:
    - endTime: 结束时间
    - id: 活动id
    """

    url = "/mgmt/prmt/loginGift/modifyEndTime"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
