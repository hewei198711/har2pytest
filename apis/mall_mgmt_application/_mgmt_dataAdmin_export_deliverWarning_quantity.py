import os

from util.client import client

data = {
    "dimension": 0,  # 统计维度 1：按购货人统计 2：按产品统计
    "orderDate": 0,  # 报单月份
    "pageNum": 0,  # 页码(不传默认为1)
    "pageSize": 0,  # 每页大小(不传默认为10)
    "productNo": "",  # 产品编号
    "ruleId": 0,  # 规则id
    "storeCode": "",  # 门店编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_export_deliverWarning_quantity(data=data, headers=headers):
    """
    交付预警-销售数量-明细导出
    /mgmt/dataAdmin/export/deliverWarning/quantity

    参数说明:
    - dimension: 统计维度 1：按购货人统计 2：按产品统计
    - orderDate: 报单月份
    - pageNum: 页码(不传默认为1)
    - pageSize: 每页大小(不传默认为10)
    - productNo: 产品编号
    - ruleId: 规则id
    - storeCode: 门店编号
    """

    url = "/mgmt/dataAdmin/export/deliverWarning/quantity"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
