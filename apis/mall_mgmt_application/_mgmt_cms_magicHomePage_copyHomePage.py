import os

from util.client import client

data = {
    "id": 0,  # id
    "location": 0,  # 端口(显示位置): 2:APP; 3:小程序
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_magicHomePage_copyHomePage(data=data, headers=headers):
    """
    复制魔法首页
    /mgmt/cms/magicHomePage/copyHomePage

    参数说明:
    - id: id
    - location: 端口(显示位置): 2:APP; 3:小程序
    """

    url = "/mgmt/cms/magicHomePage/copyHomePage"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
