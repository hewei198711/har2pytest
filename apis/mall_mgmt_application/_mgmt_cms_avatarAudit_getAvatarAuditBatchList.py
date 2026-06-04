import os

from util.client import client

data = {
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 每页页数
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_avatarAudit_getAvatarAuditBatchList(data=data, headers=headers):
    """
    获取用户头像审核批次列表
    /mgmt/cms/avatarAudit/getAvatarAuditBatchList

    参数说明:
    - pageNum: 页码
    - pageSize: 每页页数
    """

    url = "/mgmt/cms/avatarAudit/getAvatarAuditBatchList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
