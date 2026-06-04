import os

from util.client import client

data = {
    "auditResult": 0,  # 审核结果 1：审核通过 0：审核不通过;
    "id": 0,  # 用户头像审核记录id
    "remark": "",  # 审核备注
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_avatarAudit_avatarManualAudit(data=data, headers=headers):
    """
    头像人工审核
    /mgmt/cms/avatarAudit/avatarManualAudit

    参数说明:
    - auditResult: 审核结果 1：审核通过 0：审核不通过;
    - id: 用户头像审核记录id
    - remark: 审核备注
    """

    url = "/mgmt/cms/avatarAudit/avatarManualAudit"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
