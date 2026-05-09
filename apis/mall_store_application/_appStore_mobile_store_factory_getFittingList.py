import os

from util.client import client

data = {
    "fittingSerialnos": [],  # 配件编码查询集合
    "productSerialnos": [],  # 产品编码查询集合
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_mobile_store_factory_getFittingList(data=data, headers=headers):
    """
    通过商品编码集或配件编码集查询配件集信息
    /appStore/mobile/store/factory/getFittingList

    参数说明:
    - fittingSerialnos: 配件编码查询集合
    - productSerialnos: 产品编码查询集合
    """

    url = "/appStore/mobile/store/factory/getFittingList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
