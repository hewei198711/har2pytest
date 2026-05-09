import os

from util.client import client

params = {
    "id": "",  # 活动id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _appStore_complex_promotionInfo(params=params, headers=headers):
    """
    获取具体签约购活动详情(包含商品信息)
    /appStore/complex/promotionInfo

    参数说明:
    - id: 活动id
    """

    url = "/appStore/complex/promotionInfo"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
