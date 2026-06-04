import os

from util.client import client

data = {
    "id": 0,  # TODO: 添加参数说明
    "payEndTime": "",  # 尾款支付结束时间
    "payStartTime": "",  # 尾款支付开始时间
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_editPreSellPromotionTime(data=data, headers=headers):
    """
    预售活动尾款支付开始、结束时间编辑
    /mgmt/prmt/editPreSellPromotionTime

    参数说明:
    - payEndTime: 尾款支付结束时间
    - payStartTime: 尾款支付开始时间
    """

    url = "/mgmt/prmt/editPreSellPromotionTime"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
