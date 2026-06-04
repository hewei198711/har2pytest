import os

from util.client import client

params = {
    "combineNum": 0,  # 组合数量
    "productCode": "",  # 产品编号
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dis_inventory_combine_forward(params=params, headers=headers):
    """
    套装组合展示
    /mgmt/dis-inventory/combine/forward

    参数说明:
    - combineNum: 组合数量
    - productCode: 产品编号
    - storeCode: 服务中心编号
    """

    url = "/mgmt/dis-inventory/combine/forward"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
