import os

from util.client import client

data = {
    "endTime": "",  # 结束时间
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 页面大小
    "serialNo": "",  # 商品编码
    "startTime": "",  # 开始时间
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_quota_distLogList(data=data, headers=headers):
    """
    销售分配量记录列表
    /mgmt/product/quota/distLogList

    参数说明:
    - endTime: 结束时间
    - pageNum: 页码
    - pageSize: 页面大小
    - serialNo: 商品编码
    - startTime: 开始时间
    - storeCode: 服务中心编号
    """

    url = "/mgmt/product/quota/distLogList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
