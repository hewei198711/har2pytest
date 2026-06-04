import os

from util.client import client

data = {
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 每页页数
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_miniProgramLink_getLinkList(data=data, headers=headers):
    """
    获取小程序链接列表
    /mgmt/cms/miniProgramLink/getLinkList

    参数说明:
    - pageNum: 页码
    - pageSize: 每页页数
    """

    url = "/mgmt/cms/miniProgramLink/getLinkList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
