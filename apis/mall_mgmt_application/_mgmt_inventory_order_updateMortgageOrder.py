import os

from util.client import client

data = {
    "invtMortgageProductVOList": [
        {"id": 0, "productCode": "", "productMortgagePrice": 0.0, "productNum": 0, "productSecCode": ""}
    ],  # TODO: 添加参数说明
    "isBatchCancel": False,  # 批量取消标志
    "updateInvtMortgageOrderVO": {"id": 0, "orderRemarks": ""},  # TODO: 添加参数说明
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_order_updateMortgageOrder(data=data, headers=headers):
    """
    修改押货单
    /mgmt/inventory/order/updateMortgageOrder

    参数说明:
    - invtMortgageProductVOList.id: 物品id
    - invtMortgageProductVOList.productCode: 物品编码
    - invtMortgageProductVOList.productMortgagePrice: 物品押货价
    - invtMortgageProductVOList.productNum: 物品数量
    - invtMortgageProductVOList.productSecCode: 物品二级编码
    - isBatchCancel: 批量取消标志
    - updateInvtMortgageOrderVO.id: 押货单id
    - updateInvtMortgageOrderVO.orderRemarks: 押货单备注
    """

    url = "/mgmt/inventory/order/updateMortgageOrder"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
