import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_store_importStoreExtraInfoList(headers=headers):
    """
    批量导入服务中心额外信息
    /mgmt/store/importStoreExtraInfoList
    """

    url = "/mgmt/store/importStoreExtraInfoList"
    with client.post(url=url, headers=headers) as r:
        return r
