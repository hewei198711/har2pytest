import os

from util.client import client

data = {
    "enable": 0,  # 是否启用, 0:禁用; 1:启用
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_perfectInfo_enablePerfectInfo(data=data, headers=headers):
    """
    修改完美资讯启用状态
    /mgmt/cms/perfectInfo/enablePerfectInfo

    参数说明:
    - enable: 是否启用, 0:禁用; 1:启用
    - id: id
    """

    url = "/mgmt/cms/perfectInfo/enablePerfectInfo"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
