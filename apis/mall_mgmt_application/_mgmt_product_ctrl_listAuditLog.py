import os

from util.client import client

data = {
    "auditTypeResult": 0,  # 审核意见 0-全部，1-产品审核通过，2-产品审核不通过，3-财务审核通过，4-财务审核不通过
    "endTime": 0,  # 结束时间时间戳
    "operator": "",  # 操作人
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 页面大小
    "productId": "",  # 商品id
    "startTime": 0,  # 开始时间时间戳
    "versionId": "",  # 商品版本id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_ctrl_listAuditLog(data=data, headers=headers):
    """
    商品版本审核历史列表
    /mgmt/product/ctrl/listAuditLog

    参数说明:
    - auditTypeResult: 审核意见 0-全部，1-产品审核通过，2-产品审核不通过，3-财务审核通过，4-财务审核不通过
    - endTime: 结束时间时间戳
    - operator: 操作人
    - pageNum: 页码
    - pageSize: 页面大小
    - productId: 商品id
    - startTime: 开始时间时间戳
    - versionId: 商品版本id
    """

    url = "/mgmt/product/ctrl/listAuditLog"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
