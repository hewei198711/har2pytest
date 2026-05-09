import os

from util.client import client

data = {
    "auditStatus": 0,  # 审核状态  1->通过 2->不通过
    "remarks": "",  # 备注
    "serviceNo": "",  # 售后单号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_mobile_orderReturn_audit(data=data, headers=headers):
    """
    售后单审核
    /appStore/mobile/orderReturn/audit

    参数说明:
    - auditStatus: 审核状态  1->通过 2->不通过
    - remarks: 备注
    - serviceNo: 售后单号
    """

    url = "/appStore/mobile/orderReturn/audit"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
