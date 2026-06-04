import os

from util.client import client

data = {
    "auditOpinion": "",  # 审批意见
    "id": 0,  # 列表数据主键id
    "verifyStatus": 0,  # 审核状态  1审核通过  2不通过
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_other_auditOtherApply(data=data, headers=headers):
    """
    审核其他申请记录
    /mgmt/store/other/auditOtherApply

    参数说明:
    - auditOpinion: 审批意见
    - id: 列表数据主键id
    - verifyStatus: 审核状态  1审核通过  2不通过
    """

    url = "/mgmt/store/other/auditOtherApply"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
