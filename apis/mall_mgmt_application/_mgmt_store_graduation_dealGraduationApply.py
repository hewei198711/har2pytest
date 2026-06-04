import os

from util.client import client

data = {
    "auditOpinion": "",  # 意见
    "id": 0,  # 列表数据主键id
    "verifyStatus": 0,  # 状态  2通过 3驳回
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_graduation_dealGraduationApply(data=data, headers=headers):
    """
    受理--后台
    /mgmt/store/graduation/dealGraduationApply

    参数说明:
    - auditOpinion: 意见
    - id: 列表数据主键id
    - verifyStatus: 状态  2通过 3驳回
    """

    url = "/mgmt/store/graduation/dealGraduationApply"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
