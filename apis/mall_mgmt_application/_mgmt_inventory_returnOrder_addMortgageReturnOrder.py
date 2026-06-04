import os

from util.client import client

data = {
    "invtMortgageReturnOrderProductVOList": [
        {"productCode": "", "productNum": 0, "productRemarks": ""}
    ],  # TODO: 添加参数说明
    "invtMortgageReturnOrderVO": {
        "reasonFirst": "",
        "reasonFirstId": 0,
        "reasonFirstRemarks": "",
        "reasonSecond": "",
        "reasonSecondId": 0,
        "reasonSecondRemarks": "",
        "returnAddress": "",
        "returnProofName": "",
        "returnProofUrl": "",
        "storeCode": "",
    },  # TODO: 添加参数说明
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_returnOrder_addMortgageReturnOrder(data=data, headers=headers):
    """
    后台申请添加押货退货单
    /mgmt/inventory/returnOrder/addMortgageReturnOrder

    参数说明:
    - invtMortgageReturnOrderProductVOList.productCode: 物品编号
    - invtMortgageReturnOrderProductVOList.productNum: 退货数量
    - invtMortgageReturnOrderProductVOList.productRemarks: 商品备注
    - invtMortgageReturnOrderVO.reasonFirst: 一级原因
    - invtMortgageReturnOrderVO.reasonFirstId: 一级原因id
    - invtMortgageReturnOrderVO.reasonFirstRemarks: 一级原因备注
    - invtMortgageReturnOrderVO.reasonSecond: 二级原因
    - invtMortgageReturnOrderVO.reasonSecondId: 二级原因id
    - invtMortgageReturnOrderVO.reasonSecondRemarks: 二级原因备注
    - invtMortgageReturnOrderVO.returnAddress: 退货地址
    - invtMortgageReturnOrderVO.returnProofName: 退货凭证名称,逗号隔开,最多3个
    - invtMortgageReturnOrderVO.returnProofUrl: 退货凭证url,逗号隔开,最多3个
    - invtMortgageReturnOrderVO.storeCode: 服务中心编号
    """

    url = "/mgmt/inventory/returnOrder/addMortgageReturnOrder"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
