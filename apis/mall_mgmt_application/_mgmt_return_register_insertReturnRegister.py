import os

from util.client import client

data = {
    "commitTime": "",  # 下单时间
    "customer": "",  # 顾客姓名
    "customerCard": "",  # 顾客卡号
    "id": 0,  # 登记表id
    "orderAmount": 0.0,  # 实付金额
    "orderNo": "",  # 订单编号
    "orderStatus": 0,  # 订单状态  0->待审核 1->待支付 2->待发货 3->待收货 4->已取消 5->已退货 98->审核取消 99->已完成
    "products": [
        {
            "meterUnit": "",
            "packing": "",
            "productCode": "",
            "productName": "",
            "quantity": 0,
            "registerId": 0,
            "retailPrice": 0.0,
            "totalPrice": 0.0,
        }
    ],  # 退货商品信息
    "reason1": "",  # 退货一级原因
    "reason1Id": 0,  # 退货一级原因id
    "reason1Remark": "",  # 退货一级原因备注
    "refundAmount": 0.0,  # 退货金额
    "returnRemark": "",  # 退货情况
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_return_register_insertReturnRegister(data=data, headers=headers):
    """
    手工登记退货信息
    /mgmt/return/register/insertReturnRegister

    参数说明:
    - commitTime: 下单时间
    - customer: 顾客姓名
    - customerCard: 顾客卡号
    - id: 登记表id
    - orderAmount: 实付金额
    - orderNo: 订单编号
    - orderStatus: 订单状态  0->待审核 1->待支付 2->待发货 3->待收货 4->已取消 5->已退货 98->审核取消 99->已完成
    - products: 退货商品信息
    - products.meterUnit: 单位
    - products.packing: 规格
    - products.productCode: 商品编码
    - products.productName: 商品名称
    - products.quantity: 数量
    - products.registerId: 主表id
    - products.retailPrice: 零售价
    - products.totalPrice: 金额小计
    - reason1: 退货一级原因
    - reason1Id: 退货一级原因id
    - reason1Remark: 退货一级原因备注
    - refundAmount: 退货金额
    - returnRemark: 退货情况
    """

    url = "/mgmt/return/register/insertReturnRegister"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
