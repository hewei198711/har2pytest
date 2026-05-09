import os
from urllib.parse import urlencode

from util.client import client

data = {
    "keyword": "",  # keyword
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _appStore_mobile_store_factory_getProductList(data=data, headers=headers):
    """
    根据关键字模糊查询商品信息
    /appStore/mobile/store/factory/getProductList

    参数说明:
    - keyword: keyword
    """

    url = "/appStore/mobile/store/factory/getProductList"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
