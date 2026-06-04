import os

from util.client import client

data = {
    "expressSubsidy": 0.0,  # 运费补贴
    "inspectRemark": "",  # 验货备注
    "inspectResult": 0,  # 验货意见 0不通过 1通过
    "orderId": 0,  # 退货单id
    "productList": [{"productCode": "", "returnRealNum": 0}],  # 商品列表
    "returnRealAmount": 0.0,  # 物品实退金额总额
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_dis_mortgage_returnOrder_inspect(data=data, headers=headers):
    """
    验货
    /mgmt/inventory/dis/mortgage/returnOrder/inspect

    参数说明:
    - expressSubsidy: 运费补贴
    - inspectRemark: 验货备注
    - inspectResult: 验货意见 0不通过 1通过
    - orderId: 退货单id
    - productList: 商品列表
    - productList.productCode: 商品编码
    - productList.returnRealNum: 物品实退数量
    - returnRealAmount: 物品实退金额总额
    """

    url = "/mgmt/inventory/dis/mortgage/returnOrder/inspect"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
