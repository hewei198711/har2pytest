import os

from util.client import client

data = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_perfectInfo_delPerfectInfo(data=data, headers=headers):
    """
    删除完美资讯
    /mgmt/cms/perfectInfo/delPerfectInfo

    参数说明:
    - id: id
    """

    url = "/mgmt/cms/perfectInfo/delPerfectInfo"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
