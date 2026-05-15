import os

from util.client import client

data = {
    "invtMortgageReturnOrderProductVOList": [
        {"productCode": "", "productNum": 0, "productRemarks": ""}
    ],  # 押货退货单货物列表
    "invtMortgageReturnOrderVO": {
        "evidenceList": [],
        "evidenceNameList": [],
        "orderMark": 0,
        "reasonFirst": "",
        "reasonFirstId": 0,
        "reasonFirstRemarks": "",
        "reasonSecond": "",
        "reasonSecondRemarks": "",
    },  # 押货退货单信息
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_purchaseReturnOrder_save(data=data, headers=headers):
    """
    提交退货单
    /appStore/purchaseReturnOrder/save

    参数说明:
    - invtMortgageReturnOrderProductVOList: 押货退货单货物列表
    - invtMortgageReturnOrderProductVOList.productCode: 物品编号
    - invtMortgageReturnOrderProductVOList.productNum: 退货数量
    - invtMortgageReturnOrderProductVOList.productRemarks: 商品备注
    - invtMortgageReturnOrderVO: 押货退货单信息
    - invtMortgageReturnOrderVO.evidenceList: 退货凭据
    - invtMortgageReturnOrderVO.evidenceNameList: 退货凭据名称
    - invtMortgageReturnOrderVO.orderMark: 订单标识 1普通押货退货 2套装组合退货 3套装拆分退货
    - invtMortgageReturnOrderVO.reasonFirst: 一级原因
    - invtMortgageReturnOrderVO.reasonFirstId: 一级原因id
    - invtMortgageReturnOrderVO.reasonFirstRemarks: 一级原因备注
    - invtMortgageReturnOrderVO.reasonSecond: 二级原因
    - invtMortgageReturnOrderVO.reasonSecondRemarks: 二级原因备注
    """

    url = "/appStore/purchaseReturnOrder/save"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
