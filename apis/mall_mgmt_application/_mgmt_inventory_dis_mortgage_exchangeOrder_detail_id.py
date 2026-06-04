import os

from util.client import client

params = {
    "id": 0,  # 换货单id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_dis_mortgage_exchangeOrder_detail_id(params=params, headers=headers):
    """
    详情
    /mgmt/inventory/dis/mortgage/exchangeOrder/detail/{id}

    参数说明:
    - id: 换货单id
    """

    url = f"/mgmt/inventory/dis/mortgage/exchangeOrder/detail/{params['id']}"
    with client.get(url=url, headers=headers) as r:
        return r
