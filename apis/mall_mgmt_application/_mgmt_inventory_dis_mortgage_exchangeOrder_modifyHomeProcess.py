import os

from util.client import client

data = {
    "disposalProofName": "",  # 报废凭证名称,最多9个，逗号隔开
    "disposalProofUrl": "",  # 报废凭证,最多9个，逗号隔开
    "expressAmount": 0.0,  # 物流金额
    "expressCompany": "",  # 快递公司
    "expressNo": "",  # 快递单号
    "expressProofName": "",  # 快递凭证名称
    "expressProofUrl": "",  # 快递凭证url
    "expressToHome": {
        "expectTime": "",
        "senderAddress": "",
        "senderArea": "",
        "senderName": "",
        "senderPhone": "",
        "transId": "",
    },  # 上门取件参数
    "orderId": 0,  # 换货单id
    "processRemark": "",  # 退回说明
    "returnType": 0,  # 退回方式 1服务中心报废 2自带 3邮寄 4上门取件
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_dis_mortgage_exchangeOrder_modifyHomeProcess(data=data, headers=headers):
    """
    修改上门取件退回处理
    /mgmt/inventory/dis/mortgage/exchangeOrder/modifyHomeProcess

    参数说明:
    - disposalProofName: 报废凭证名称,最多9个，逗号隔开
    - disposalProofUrl: 报废凭证,最多9个，逗号隔开
    - expressAmount: 物流金额
    - expressCompany: 快递公司
    - expressNo: 快递单号
    - expressProofName: 快递凭证名称
    - expressProofUrl: 快递凭证url
    - expressToHome: 上门取件参数
    - expressToHome.expectTime: 期望上门时间 yyyy-MM-dd HH:mm
    - expressToHome.senderAddress: 寄件人详细地址
    - expressToHome.senderArea: 寄件人省市区, 省市区之间用逗号,隔开
    - expressToHome.senderName: 寄件人姓名
    - expressToHome.senderPhone: 寄件人手机
    - expressToHome.transId: 业务id, 防止订单重复提交
    - orderId: 换货单id
    - processRemark: 退回说明
    - returnType: 退回方式 1服务中心报废 2自带 3邮寄 4上门取件
    """

    url = "/mgmt/inventory/dis/mortgage/exchangeOrder/modifyHomeProcess"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
