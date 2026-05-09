import os

from util.client import client

data = {
    "attachmentList": [],  # 附件列表(退回快递凭证)
    "id": 0,  # 返修单ID
    "returnExpressName": "",  # 退回完美的物流公司
    "returnExpressNo": "",  # 退回完美的运单号
    "returnRemark": "",  # 退回备注
    "returnType": 0,  # 退回方式：1->邮寄；2->自带
    "systemCode": 0,  # 查询系统编码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_mobile_store_factory_turnBackFactoryOrder(data=data, headers=headers):
    """
    返厂维修单退回
    /appStore/mobile/store/factory/turnBackFactoryOrder

    参数说明:
    - attachmentList: 附件列表(退回快递凭证)
    - id: 返修单ID
    - returnExpressName: 退回完美的物流公司
    - returnExpressNo: 退回完美的运单号
    - returnRemark: 退回备注
    - returnType: 退回方式：1->邮寄；2->自带
    - systemCode: 查询系统编码
    """

    url = "/appStore/mobile/store/factory/turnBackFactoryOrder"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
