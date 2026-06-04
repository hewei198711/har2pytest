import os

from util.client import client

data = {
    "changeReason": "",  # 调整原因
    "dealRemark": "",  # 处理备注
    "id": 0,  # 主键id
    "sourceType": 0,  # 款项类型 3、超额押货款退款 4、超额押货款确认押货款
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_remit_overRemit_deal(data=data, headers=headers):
    """
    超额流水流水处理
    /mgmt/inventory/remit/overRemit/deal

    参数说明:
    - changeReason: 调整原因
    - dealRemark: 处理备注
    - id: 主键id
    - sourceType: 款项类型 3、超额押货款退款 4、超额押货款确认押货款
    """

    url = "/mgmt/inventory/remit/overRemit/deal"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
