import os

from util.client import client

data = {
    "cardNo": "",  # 会员卡号
    "dimension": 0,  # 统计维度 1：门店交付明细 2：公司交付明细
    "orderDate": 0,  # 报单月份
    "pageNum": 0,  # 页码(不传默认为1)
    "pageSize": 0,  # 每页大小(不传默认为10)
    "productNo": "",  # 产品编号
    "ruleId": 0,  # 规则id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_export_shopWarning_quantity(data=data, headers=headers):
    """
    购货预警-销售数量-明细导出
    /mgmt/dataAdmin/export/shopWarning/quantity

    参数说明:
    - cardNo: 会员卡号
    - dimension: 统计维度 1：门店交付明细 2：公司交付明细
    - orderDate: 报单月份
    - pageNum: 页码(不传默认为1)
    - pageSize: 每页大小(不传默认为10)
    - productNo: 产品编号
    - ruleId: 规则id
    """

    url = "/mgmt/dataAdmin/export/shopWarning/quantity"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
