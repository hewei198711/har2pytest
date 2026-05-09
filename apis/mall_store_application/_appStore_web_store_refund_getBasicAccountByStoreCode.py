import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_web_store_refund_getBasicAccountByStoreCode(headers=headers):
    """
    获取本服务中心的银行卡基本户信息
    /appStore/web/store/refund/getBasicAccountByStoreCode
    """

    url = "/appStore/web/store/refund/getBasicAccountByStoreCode"
    with client.get(url=url, headers=headers) as r:
        return r
