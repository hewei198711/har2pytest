import os

from util.client import client

params = {
    "damageId": 0,  # damageId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_damage_getCargoDamageDetail(params=params, headers=headers):
    """
    货损货差详情
    /mgmt/order/damage/getCargoDamageDetail

    参数说明:
    - damageId: damageId
    """

    url = "/mgmt/order/damage/getCargoDamageDetail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
