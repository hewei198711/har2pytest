import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_inventory_summary(headers=headers):
    """
    获取服务中心库存统计信息
    /appStore/inventory/summary
    """

    url = "/appStore/inventory/summary"
    with client.get(url=url, headers=headers) as r:
        return r
