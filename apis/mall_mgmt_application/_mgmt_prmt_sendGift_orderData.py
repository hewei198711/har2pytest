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


def _mgmt_prmt_sendGift_orderData(data=data, headers=headers):
    """
    订单数据统计
    /mgmt/prmt/sendGift/orderData

    参数说明:
    - endTime: 结束时间(yyyy-MM-dd)
    - promotionId: 活动id
    - startTime: 开始时间(yyyy-MM-dd)
    """

    url = "/mgmt/prmt/sendGift/orderData"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
