import os

from util.client import client

params = {
    "returnRatio": "",  # 退货额度比例(0.00-1.00)
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_return_config_getReturnAmount(params=params, headers=headers):
    """
    实时计算押货余额极限值
    /mgmt/inventory/return/config/getReturnAmount

    参数说明:
    - returnRatio: 退货额度比例(0.00-1.00)
    - storeCode: 服务中心编号
    """

    url = "/mgmt/inventory/return/config/getReturnAmount"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
