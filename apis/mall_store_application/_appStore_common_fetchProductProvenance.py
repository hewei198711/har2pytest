import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _appStore_common_fetchProductProvenance(headers=headers):
    """
    获取商品产地信息列表
    /appStore/common/fetchProductProvenance
    """

    url = "/appStore/common/fetchProductProvenance"
    with client.get(url=url, headers=headers) as r:
        return r
