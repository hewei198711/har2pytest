import os

from util.client import client

data = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_loginGift_deleteImportMember(data=data, headers=headers):
    """
    删除登录有礼活动导入顾客
    /mgmt/prmt/loginGift/deleteImportMember

    参数说明:
    - id: id
    """

    url = "/mgmt/prmt/loginGift/deleteImportMember"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
