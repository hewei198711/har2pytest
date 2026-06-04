import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_store_importBatchAdjustLevel(headers=headers):
    """
    服务中心批量调整等级导入
    /mgmt/store/importBatchAdjustLevel
    """

    url = "/mgmt/store/importBatchAdjustLevel"
    with client.post(url=url, headers=headers) as r:
        return r
