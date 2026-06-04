import os

from util.client import client

data = {
    "id": 0,  # 专区id
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 每页页数
    "zoneName": "",  # 专区名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_magicZone_queryZonePage(data=data, headers=headers):
    """
    获取魔法专区分页列表
    /mgmt/cms/magicZone/queryZonePage

    参数说明:
    - id: 专区id
    - pageNum: 页码
    - pageSize: 每页页数
    - zoneName: 专区名称
    """

    url = "/mgmt/cms/magicZone/queryZonePage"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
