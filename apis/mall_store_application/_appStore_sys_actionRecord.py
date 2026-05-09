import os

from util.client import client

params = {
    "title": "",  # 优秀案例库title名称(一级title)
    "type": "",  # 行为类型  2-浏览， 3-点赞
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_sys_actionRecord(params=params, headers=headers):
    """
    浏览/点赞行为记录接口
    /appStore/sys/actionRecord

    参数说明:
    - title: 优秀案例库title名称(一级title)
    - type: 行为类型  2-浏览， 3-点赞
    """

    url = "/appStore/sys/actionRecord"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
