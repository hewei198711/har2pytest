import os

from util.client import client

params = {
    "key": "",  # key
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_share_selectErrorMember(params=params, headers=headers):
    """
    查询导入错误数据
    /mgmt/prmt/share/selectErrorMember

    参数说明:
    - key: key
    """

    url = "/mgmt/prmt/share/selectErrorMember"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
