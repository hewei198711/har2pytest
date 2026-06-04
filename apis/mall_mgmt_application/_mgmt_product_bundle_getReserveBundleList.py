import os

from util.client import client

params = {
    "pageNum": "",  # 页码
    "pageSize": "",  # 页面大小
    "serialNo": "",  # 产品编码
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_bundle_getReserveBundleList(params=params, headers=headers):
    """
    查询保留套装列表
    /mgmt/product/bundle/getReserveBundleList

    参数说明:
    - pageNum: 页码
    - pageSize: 页面大小
    - serialNo: 产品编码
    - storeCode: 服务中心编号
    """

    url = "/mgmt/product/bundle/getReserveBundleList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
