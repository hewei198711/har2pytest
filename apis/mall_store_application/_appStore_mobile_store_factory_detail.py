import os

from util.client import client

params = {
    "repairNo": "",  # repairNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_mobile_store_factory_detail(params=params, headers=headers):
    """
    获取返厂维修单详情
    /appStore/mobile/store/factory/detail

    参数说明:
    - repairNo: repairNo
    """

    url = "/appStore/mobile/store/factory/detail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
