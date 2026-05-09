import os

from util.client import client

params = {
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_common_isOpenSignControl(params=params, headers=headers):
    """
    查询服务中心是否开启签署控制
    /appStore/store/common/isOpenSignControl

    参数说明:
    - storeCode: storeCode
    """

    url = "/appStore/store/common/isOpenSignControl"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
