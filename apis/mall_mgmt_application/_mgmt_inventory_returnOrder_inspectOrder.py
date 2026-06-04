import os

from util.client import client

data = {
    "expressSubsidy": 0.0,  # 运费补贴
    "inspectRemarks": "",  # 验货备注
    "inspectStatus": 0,  # 验货意见 0不通过 1通过
    "orderId": 0,  # 退货单id
    "orderReturnRealAmount": 0.0,  # 物品实退金额总额
    "productList": [{"id": 0, "productRealAmount": 0.0, "productRealNum": 0}],  # 物品列表
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_returnOrder_inspectOrder(data=data, headers=headers):
    """
    后台押货退货验货
    /mgmt/inventory/returnOrder/inspectOrder

    参数说明:
    - expressSubsidy: 运费补贴
    - inspectRemarks: 验货备注
    - inspectStatus: 验货意见 0不通过 1通过
    - orderId: 退货单id
    - orderReturnRealAmount: 物品实退金额总额
    - productList: 物品列表
    - productList.id: 物品id
    - productList.productRealAmount: 退货单实退金额总额
    - productList.productRealNum: 物品实退数量
    """

    url = "/mgmt/inventory/returnOrder/inspectOrder"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
