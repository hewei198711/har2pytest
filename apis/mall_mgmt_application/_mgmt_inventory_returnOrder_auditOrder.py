import os

from util.client import client

data = {
    "auditFileName": "",  # 审核附件名称
    "auditFileUrl": "",  # 审核附件url
    "auditRemarks": "",  # 审核备注
    "auditStatus": 0,  # 审核结果 0不通过 1通过
    "id": 0,  # 押货退货单id
    "reasonFirst": "",  # 一级原因
    "reasonFirstId": 0,  # 一级原因id
    "reasonFirstRemarks": "",  # 一级原因备注
    "reasonSecond": "",  # 二级原因
    "reasonSecondId": 0,  # 二级原因id
    "reasonSecondRemarks": "",  # 二级原因备注
    "returnInfo": "",  # 退回地址信息
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_returnOrder_auditOrder(data=data, headers=headers):
    """
    后台审批押货退货单
    /mgmt/inventory/returnOrder/auditOrder

    参数说明:
    - auditFileName: 审核附件名称
    - auditFileUrl: 审核附件url
    - auditRemarks: 审核备注
    - auditStatus: 审核结果 0不通过 1通过
    - id: 押货退货单id
    - reasonFirst: 一级原因
    - reasonFirstId: 一级原因id
    - reasonFirstRemarks: 一级原因备注
    - reasonSecond: 二级原因
    - reasonSecondId: 二级原因id
    - reasonSecondRemarks: 二级原因备注
    - returnInfo: 退回地址信息
    """

    url = "/mgmt/inventory/returnOrder/auditOrder"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
