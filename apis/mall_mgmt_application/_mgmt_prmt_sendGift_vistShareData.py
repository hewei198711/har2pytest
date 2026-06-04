import os

from util.client import client

data = {
    "endTime": "",  # 结束时间(yyyy-MM-dd)
    "promotionId": 0,  # 活动id
    "startTime": "",  # 开始时间(yyyy-MM-dd)
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_sendGift_vistShareData(data=data, headers=headers):
    """
    活动主页数据统计
    /mgmt/prmt/sendGift/vistShareData

    参数说明:
    - endTime: 结束时间(yyyy-MM-dd)
    - promotionId: 活动id
    - startTime: 开始时间(yyyy-MM-dd)
    """

    url = "/mgmt/prmt/sendGift/vistShareData"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
