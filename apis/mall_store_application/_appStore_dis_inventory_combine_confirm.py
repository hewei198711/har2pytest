import os
from urllib.parse import urlencode

from util.client import client

data = {
    "combineNum": 0,  # 套装组合数量
    "productCode": "",  # 产品编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _appStore_dis_inventory_combine_confirm(data=data, headers=headers):
    """
    确认套装组合
    /appStore/dis-inventory/combine/confirm

    参数说明:
    - combineNum: 套装组合数量
    - productCode: 产品编号
    """

    url = "/appStore/dis-inventory/combine/confirm"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
