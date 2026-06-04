import os

from util.client import client

data = {
    "auditFileName": "",  # 审核附件名称
    "auditFileUrl": "",  # 审核附件url
    "auditPass": False,  # TODO: 添加参数说明
    "auditRemark": "",  # 审核备注
    "auditResult": 0,  # 审核结果 0不通过 1通过
    "id": 0,  # 押货退货单id
    "reasonFirst": "",  # 一级原因
    "reasonFirstId": 0,  # 一级原因id
    "reasonFirstRemark": "",  # 一级原因备注
    "reasonSecond": "",  # 二级原因
    "reasonSecondId": 0,  # 二级原因id
    "reasonSecondRemark": "",  # 二级原因备注
    "returnAddress": "",  # 退回地址信息
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_dis_mortgage_returnOrder_audit(data=data, headers=headers):
    """
    审批
    /mgmt/inventory/dis/mortgage/returnOrder/audit

    参数说明:
    - auditFileName: 审核附件名称
    - auditFileUrl: 审核附件url
    - auditRemark: 审核备注
    - auditResult: 审核结果 0不通过 1通过
    - id: 押货退货单id
    - reasonFirst: 一级原因
    - reasonFirstId: 一级原因id
    - reasonFirstRemark: 一级原因备注
    - reasonSecond: 二级原因
    - reasonSecondId: 二级原因id
    - reasonSecondRemark: 二级原因备注
    - returnAddress: 退回地址信息
    """

    url = "/mgmt/inventory/dis/mortgage/returnOrder/audit"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
