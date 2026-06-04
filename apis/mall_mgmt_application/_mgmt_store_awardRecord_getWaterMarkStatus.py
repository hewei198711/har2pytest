import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_awardRecord_getWaterMarkStatus(headers=headers):
    """
    获取海报水印开关状态
    /mgmt/store/awardRecord/getWaterMarkStatus
    """

    url = "/mgmt/store/awardRecord/getWaterMarkStatus"
    with client.get(url=url, headers=headers) as r:
        return r
