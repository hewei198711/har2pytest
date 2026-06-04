import os

from util.client import client

params = {
    "key": "",  # 查询参数关键字
    "level": 0,  # level
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_msgadmin_param_search(params=params, headers=headers):
    """
    模板参数内容查询接口(无参返回全部,有参数模糊查询)
    /mgmt/msgadmin/param/search

    参数说明:
    - key: 查询参数关键字
    - level: level
    """

    url = "/mgmt/msgadmin/param/search"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
