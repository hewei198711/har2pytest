import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_dis_inventory_settle_scope(headers=headers):
    """
    获取月结时间范围（包含未完成状态）
    /appStore/dis-inventory/settle-scope
    """

    url = "/appStore/dis-inventory/settle-scope"
    with client.get(url=url, headers=headers) as r:
        return r
