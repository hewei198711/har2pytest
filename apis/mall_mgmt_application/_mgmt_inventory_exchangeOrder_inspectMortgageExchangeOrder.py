import os

from util.client import client

data = {
    "expressSubsidy": 0.0,  # 运费补贴
    "inspectProof": [],  # 验货凭证
    "inspectRemarks": "",  # 验货备注
    "inspectStatus": 0,  # 验货结果 0不通过 1通过
    "orderId": 0,  # 换货单id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_exchangeOrder_inspectMortgageExchangeOrder(data=data, headers=headers):
    """
    后台押货换货单验货
    /mgmt/inventory/exchangeOrder/inspectMortgageExchangeOrder

    参数说明:
    - expressSubsidy: 运费补贴
    - inspectProof: 验货凭证
    - inspectRemarks: 验货备注
    - inspectStatus: 验货结果 0不通过 1通过
    - orderId: 换货单id
    """

    url = "/mgmt/inventory/exchangeOrder/inspectMortgageExchangeOrder"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
