import os

from util.client import client

data = {
    "changeReason": "",  # 调整原因(款项类型对应交易类型名称)
    "companyCode": "",  # 分公司code
    "dealRemark": "",  # 处理备注
    "id": 0,  # 主键id
    "sourceType": 0,  # 款项类型 5、无法识别款确认押货款、6无法识别款退款、 15无法识别款不处理
    "storeCode": "",  # 服务中心code
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_remit_unknownRemit_deal(data=data, headers=headers):
    """
    未知款项流水处理
    /mgmt/inventory/remit/unknownRemit/deal

    参数说明:
    - changeReason: 调整原因(款项类型对应交易类型名称)
    - companyCode: 分公司code
    - dealRemark: 处理备注
    - id: 主键id
    - sourceType: 款项类型 5、无法识别款确认押货款、6无法识别款退款、 15无法识别款不处理
    - storeCode: 服务中心code
    """

    url = "/mgmt/inventory/remit/unknownRemit/deal"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
