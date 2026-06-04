import os

from util.client import client

data = {
    "endTime": "",  # 活动结束时间
    "id": 0,  # 活动id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_editPromotionEndTime(data=data, headers=headers):
    """
    编辑活动结束时间
    /mgmt/prmt/editPromotionEndTime

    参数说明:
    - endTime: 活动结束时间
    - id: 活动id
    """

    url = "/mgmt/prmt/editPromotionEndTime"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
