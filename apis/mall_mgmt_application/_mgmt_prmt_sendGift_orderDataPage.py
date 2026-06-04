import os

from util.client import client

data = {
    "endTime": "",  # 结束时间(yyyy-MM-dd)
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页数量
    "promotionId": 0,  # 活动id
    "startTime": "",  # 开始时间(yyyy-MM-dd)
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_sendGift_orderDataPage(data=data, headers=headers):
    """
    订单数据明细
    /mgmt/prmt/sendGift/orderDataPage

    参数说明:
    - endTime: 结束时间(yyyy-MM-dd)
    - pageNum: 当前页
    - pageSize: 每页数量
    - promotionId: 活动id
    - startTime: 开始时间(yyyy-MM-dd)
    """

    url = "/mgmt/prmt/sendGift/orderDataPage"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
