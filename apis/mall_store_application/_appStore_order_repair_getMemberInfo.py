import os

from util.client import client

params = {
    "customerCard": "",  # customerCard
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_order_repair_getMemberInfo(params=params, headers=headers):
    """
    根据会员卡号查询会员信息
    /appStore/order/repair/getMemberInfo

    参数说明:
    - customerCard: customerCard
    """

    url = "/appStore/order/repair/getMemberInfo"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
