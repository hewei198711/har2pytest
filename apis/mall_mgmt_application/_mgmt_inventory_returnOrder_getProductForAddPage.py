import os

from util.client import client

params = {
    "productCode": "",  # 商品一级或二级编码
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_returnOrder_getProductForAddPage(params=params, headers=headers):
    """
    添加退货单时的商品搜索
    /mgmt/inventory/returnOrder/getProductForAddPage

    参数说明:
    - productCode: 商品一级或二级编码
    - storeCode: 服务中心编号
    """

    url = "/mgmt/inventory/returnOrder/getProductForAddPage"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
