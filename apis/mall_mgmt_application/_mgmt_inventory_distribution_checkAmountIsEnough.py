import os

from util.client import client

data = {
    "list": [{"amount": 0, "productCode": "", "storeCode": ""}],  # TODO: 添加参数说明
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_distribution_checkAmountIsEnough(data=data, headers=headers):
    """
    查询服务中心分配量是否足够
    /mgmt/inventory/distribution/checkAmountIsEnough

    参数说明:
    - list.amount: 押货数量
    - list.productCode: 商品code
    - list.storeCode: 服务中心code
    """

    url = "/mgmt/inventory/distribution/checkAmountIsEnough"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
