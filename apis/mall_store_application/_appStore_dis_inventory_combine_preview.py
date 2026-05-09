import os

from util.client import client

params = {
    "combineNum": 0,  # 套装组合数量
    "productCode": "",  # 产品编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_dis_inventory_combine_preview(params=params, headers=headers):
    """
    套装组合预览
    /appStore/dis-inventory/combine/preview

    参数说明:
    - combineNum: 套装组合数量
    - productCode: 产品编号
    """

    url = "/appStore/dis-inventory/combine/preview"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
