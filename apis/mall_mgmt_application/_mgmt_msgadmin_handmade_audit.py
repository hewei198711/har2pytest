import os

from util.client import client

data = {
    "auditOperator": "",  # 操作人
    "auditOperatorId": 0,  # 操作人Id
    "auditOpinion": "",  # 审核意见
    "auditStatus": 0,  # 审核状态 1通过,2不通过
    "files": [{"receiverName": "", "receiverUrl": ""}],  # 附件
    "planCode": "",  # 计划Code
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_msgadmin_handmade_audit(data=data, headers=headers):
    """
    审核
    /mgmt/msgadmin/handmade/audit

    参数说明:
    - auditOperator: 操作人
    - auditOperatorId: 操作人Id
    - auditOpinion: 审核意见
    - auditStatus: 审核状态 1通过,2不通过
    - files: 附件
    - files.receiverName: 文件名
    - files.receiverUrl: url地址
    - planCode: 计划Code
    """

    url = "/mgmt/msgadmin/handmade/audit"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
