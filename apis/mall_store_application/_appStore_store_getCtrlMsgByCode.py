import os

from util.client import client

params = {
    "StoreCode": "",  # StoreCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_getCtrlMsgByCode(params=params, headers=headers):
    """
    店铺年审控制信息
    /appStore/store/getCtrlMsgByCode

    参数说明:
    - StoreCode: StoreCode
    """

    url = "/appStore/store/getCtrlMsgByCode"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
