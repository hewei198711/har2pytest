import os

from util.client import client

params = {
    "customerCard": "",  # customerCard
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_factory_getMemberInfo(params=params, headers=headers):
    """
    根据会员卡号查询会员信息
    /mgmt/order/factory/getMemberInfo

    参数说明:
    - customerCard: customerCard
    """

    url = "/mgmt/order/factory/getMemberInfo"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
