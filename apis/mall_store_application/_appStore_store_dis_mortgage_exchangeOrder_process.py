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
    "expressToHome": "",  # 上门取件参数
    "orderId": 0,  # 换货单id
    "processRemark": "",  # 退回说明
    "returnType": 0,  # 退回方式 1服务中心报废 2自带 3邮寄 4上门取件
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_dis_mortgage_exchangeOrder_process(data=data, headers=headers):
    """
    退回
    /appStore/store/dis/mortgage/exchangeOrder/process

    参数说明:
    - disposalProofName: 报废凭证名称,最多9个，逗号隔开
    - disposalProofUrl: 报废凭证,最多9个，逗号隔开
    - expressAmount: 物流金额
    - expressCompany: 快递公司
    - expressNo: 快递单号
    - expressProofName: 快递凭证名称
    - expressProofUrl: 快递凭证url
    - expressToHome: 上门取件参数
    - orderId: 换货单id
    - processRemark: 退回说明
    - returnType: 退回方式 1服务中心报废 2自带 3邮寄 4上门取件
    """

    url = "/appStore/store/dis/mortgage/exchangeOrder/process"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
