import os

from util.client import client

data = {
    "exchangeType": 0,  # 处理方式
    "orderId": 0,  # 退换货单id
    "preAuditFileUrl": "",  # 预审批附件url
    "reasonFirst": "",  # 一级原因
    "reasonFirstId": 0,  # 一级原因id
    "reasonFirstRemarks": "",  # 一级原因备注
    "reasonSecond": "",  # 二级原因
    "reasonSecondId": 0,  # 二级原因id
    "reasonSecondRemarks": "",  # 二级原因备注
    "returnAddressInfo": "",  # 退货地址信息
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_returnOrder_updateReason(data=data, headers=headers):
    """
    修改退货原因
    /mgmt/inventory/returnOrder/updateReason

    参数说明:
    - exchangeType: 处理方式
    - orderId: 退换货单id
    - preAuditFileUrl: 预审批附件url
    - reasonFirst: 一级原因
    - reasonFirstId: 一级原因id
    - reasonFirstRemarks: 一级原因备注
    - reasonSecond: 二级原因
    - reasonSecondId: 二级原因id
    - reasonSecondRemarks: 二级原因备注
    - returnAddressInfo: 退货地址信息
    """

    url = "/mgmt/inventory/returnOrder/updateReason"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
