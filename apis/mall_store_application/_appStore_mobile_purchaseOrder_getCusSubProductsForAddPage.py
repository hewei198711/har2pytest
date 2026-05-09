import os

from util.client import client

params = {
    "productCode": "",  # 一级商品编码
    "subKeyword": "",  # 二级商品关键字
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_mobile_purchaseOrder_getCusSubProductsForAddPage(params=params, headers=headers):
    """
    APP提交定制品押货单页面的二级押货商品搜索
    /appStore/mobile/purchaseOrder/getCusSubProductsForAddPage

    参数说明:
    - productCode: 一级商品编码
    - subKeyword: 二级商品关键字
    """

    url = "/appStore/mobile/purchaseOrder/getCusSubProductsForAddPage"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
