import os

from util.client import client

params = {
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "sort": False,  # 排序用, 不用传
    "status": 0,  # 状态 1->启用 2->禁用
    "title": "",  # 法规名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_sys_informationLaw_list(params=params, headers=headers):
    """
    法规咨询(新)-列表
    /appStore/sys/informationLaw/list

    参数说明:
    - pageNum: 页数
    - pageSize: 页大小
    - sort: 排序用, 不用传
    - status: 状态 1->启用 2->禁用
    - title: 法规名称
    """

    url = "/appStore/sys/informationLaw/list"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
