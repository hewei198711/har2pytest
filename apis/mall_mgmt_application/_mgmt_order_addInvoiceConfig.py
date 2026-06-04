import os

from util.client import client

data = {
    "enterElecInvoiceReview": 0,  # 企业普通电子发票隔月开票是否需审核  0->否 1->是
    "enterPaperInvoiceReview": 0,  # 企业专用纸质发票隔月开票是否需审核  0->否 1->是
    "perElecInvoiceReview": 0,  # 个人普通电子发票隔月开票是否需审核  0->否 1->是
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_addInvoiceConfig(data=data, headers=headers):
    """
    新增订单发票配置信息
    /mgmt/order/addInvoiceConfig

    参数说明:
    - enterElecInvoiceReview: 企业普通电子发票隔月开票是否需审核  0->否 1->是
    - enterPaperInvoiceReview: 企业专用纸质发票隔月开票是否需审核  0->否 1->是
    - perElecInvoiceReview: 个人普通电子发票隔月开票是否需审核  0->否 1->是
    """

    url = "/mgmt/order/addInvoiceConfig"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
