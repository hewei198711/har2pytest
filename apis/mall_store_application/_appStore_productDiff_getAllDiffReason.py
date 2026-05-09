import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_productDiff_getAllDiffReason(headers=headers):
    """
    获取所有货损货差详情理由
    /appStore/productDiff/getAllDiffReason
    """

    url = "/appStore/productDiff/getAllDiffReason"
    with client.get(url=url, headers=headers) as r:
        return r
