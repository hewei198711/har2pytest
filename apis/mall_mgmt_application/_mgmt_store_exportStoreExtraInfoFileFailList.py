import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_exportStoreExtraInfoFileFailList(headers=headers):
    """
    导出服务中心额外信息失败记录
    /mgmt/store/exportStoreExtraInfoFileFailList
    """

    url = "/mgmt/store/exportStoreExtraInfoFileFailList"
    with client.get(url=url, headers=headers) as r:
        return r
