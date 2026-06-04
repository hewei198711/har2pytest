import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_damage_getAllDiffDesc(headers=headers):
    """
    获取所有详情描述配置
    /mgmt/order/damage/getAllDiffDesc
    """

    url = "/mgmt/order/damage/getAllDiffDesc"
    with client.get(url=url, headers=headers) as r:
        return r
