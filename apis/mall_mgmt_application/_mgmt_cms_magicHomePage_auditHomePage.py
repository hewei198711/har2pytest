import os

from util.client import client

data = {
    "audit": 0,  # 审核结果: 0:审核不通过; 1:审核通过
    "auditRemark": "",  # 审核意见
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_magicHomePage_auditHomePage(data=data, headers=headers):
    """
    审核魔法首页
    /mgmt/cms/magicHomePage/auditHomePage

    参数说明:
    - audit: 审核结果: 0:审核不通过; 1:审核通过
    - auditRemark: 审核意见
    - id: id
    """

    url = "/mgmt/cms/magicHomePage/auditHomePage"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
