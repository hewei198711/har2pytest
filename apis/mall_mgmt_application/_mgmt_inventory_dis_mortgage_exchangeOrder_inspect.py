import os

from util.client import client

data = {
    "expressSubsidy": 0.0,  # 运费补贴
    "inspectProofUrl": [],  # 验货凭证
    "inspectRemark": "",  # 验货备注
    "inspectResult": 0,  # 验货结果 0不通过 1通过
    "orderId": 0,  # 换货单id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_dis_mortgage_exchangeOrder_inspect(data=data, headers=headers):
    """
    验货
    /mgmt/inventory/dis/mortgage/exchangeOrder/inspect

    参数说明:
    - expressSubsidy: 运费补贴
    - inspectProofUrl: 验货凭证
    - inspectRemark: 验货备注
    - inspectResult: 验货结果 0不通过 1通过
    - orderId: 换货单id
    """

    url = "/mgmt/inventory/dis/mortgage/exchangeOrder/inspect"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
