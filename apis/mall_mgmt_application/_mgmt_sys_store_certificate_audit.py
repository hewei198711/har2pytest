import os

from util.client import client

data = {
    "auditOpinion": "",  # 审核意见
    "auditStatus": 0,  # 审核状态：0->待审核;1->审核通过;2->驳回
    "downloadDeadline": "",  # 下载有效期
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_store_certificate_audit(data=data, headers=headers):
    """
    发起公司证件审核
    /mgmt/sys/store/certificate/audit

    参数说明:
    - auditOpinion: 审核意见
    - auditStatus: 审核状态：0->待审核;1->审核通过;2->驳回
    - downloadDeadline: 下载有效期
    - id: id
    """

    url = "/mgmt/sys/store/certificate/audit"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
