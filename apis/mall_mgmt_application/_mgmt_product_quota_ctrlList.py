import os

from util.client import client

data = {
    "endTime": "",  # 操作时间结束
    "operator": "",  # 操作人
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 页面大小
    "serialNo": "",  # 商品编码
    "startTime": "",  # 操作时间开始
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_quota_ctrlList(data=data, headers=headers):
    """
    销售分配量操作日志列表
    /mgmt/product/quota/ctrlList

    参数说明:
    - endTime: 操作时间结束
    - operator: 操作人
    - pageNum: 页码
    - pageSize: 页面大小
    - serialNo: 商品编码
    - startTime: 操作时间开始
    - storeCode: 服务中心编号
    """

    url = "/mgmt/product/quota/ctrlList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
