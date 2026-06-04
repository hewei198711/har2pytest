import os

from util.client import client

data = {
    "endTime": 0,  # 结束时间时间戳
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 页面大小
    "startTime": 0,  # 开始时间时间戳
    "serialNo": "",  # 套装产品编码
    "splitStatus": 0,  # 拆分状态，1-未拆分，2-已拆分
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_bundle_getSaleOffBundleList(data=data, headers=headers):
    """
    查询拆分套装列表
    /mgmt/product/bundle/getSaleOffBundleList

    参数说明:
    - endTime: 结束时间时间戳
    - pageNum: 页码
    - pageSize: 页面大小
    - startTime: 开始时间时间戳
    - serialNo: 套装产品编码
    - splitStatus: 拆分状态，1-未拆分，2-已拆分
    """

    url = "/mgmt/product/bundle/getSaleOffBundleList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
