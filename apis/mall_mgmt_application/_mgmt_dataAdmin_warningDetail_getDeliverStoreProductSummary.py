import os

from util.client import client

params = {
    "orderDate": 0,  # 报单月份
    "productNo": "",  # 产品编号
    "ruleId": 0,  # 规则id
    "storeCode": "",  # 门店编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_warningDetail_getDeliverStoreProductSummary(params=params, headers=headers):
    """
    数据中心管理后台-预警清单明细管理-服务中心当月交付指定产品汇总统计
    /mgmt/dataAdmin/warningDetail/getDeliverStoreProductSummary

    参数说明:
    - orderDate: 报单月份
    - productNo: 产品编号
    - ruleId: 规则id
    - storeCode: 门店编号
    """

    url = "/mgmt/dataAdmin/warningDetail/getDeliverStoreProductSummary"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
