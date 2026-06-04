import os

from util.client import client

data = {
    "fittingsList": [
        {
            "amount": "",
            "fittingsName": "",
            "fittingsNo": "",
            "fittingsType": 0,
            "id": 0,
            "price": 0.0,
            "productCode": "",
            "quantity": 0,
            "repairNo": "",
        }
    ],  # 配件队列
    "id": 0,  # 返修单ID
    "systemCode": 0,  # 查询系统编码
    "totalAmount": "",  # 维修费用合计
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_factory_updateFittings(data=data, headers=headers):
    """
    返修单修改配件信息
    /mgmt/order/factory/updateFittings

    参数说明:
    - fittingsList: 配件队列
    - fittingsList.amount: 费用
    - fittingsList.fittingsName: 配件名称
    - fittingsList.fittingsNo: 配件编号
    - fittingsList.fittingsType: 类型：1->维修；2->更换
    - fittingsList.id: 配件ID
    - fittingsList.price: 配件单价
    - fittingsList.productCode: 产品编号
    - fittingsList.quantity: 配件数量
    - fittingsList.repairNo: 返厂维修单单号
    - id: 返修单ID
    - systemCode: 查询系统编码
    - totalAmount: 维修费用合计
    """

    url = "/mgmt/order/factory/updateFittings"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
