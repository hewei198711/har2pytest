import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_dis_mortgage_diffOrder_getAllDiffDesc(headers=headers):
    """
    获取所有详情描述配置
    /appStore/store/dis/mortgage/diffOrder/getAllDiffDesc
    """

    url = "/appStore/store/dis/mortgage/diffOrder/getAllDiffDesc"
    with client.get(url=url, headers=headers) as r:
        return r
