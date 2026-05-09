import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_dis_inventory_stat(headers=headers):
    """
    获取服务中心库存统计信息
    /appStore/dis-inventory/stat
    """

    url = "/appStore/dis-inventory/stat"
    with client.get(url=url, headers=headers) as r:
        return r
