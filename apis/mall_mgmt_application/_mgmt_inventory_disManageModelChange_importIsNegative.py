import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_inventory_disManageModelChange_importIsNegative(headers=headers):
    """
    批量导入(点我上传):查询是否有负库存:存在返回true
    /mgmt/inventory/disManageModelChange/importIsNegative
    """

    url = "/mgmt/inventory/disManageModelChange/importIsNegative"
    with client.post(url=url, headers=headers) as r:
        return r
