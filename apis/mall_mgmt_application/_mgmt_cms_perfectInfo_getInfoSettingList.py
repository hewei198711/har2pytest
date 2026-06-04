import os

from util.client import client

data = {
    "enableStatus": 0,  # 启用状态: 0.禁用 1.启用 传null则为全部
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 每页页数
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_perfectInfo_getInfoSettingList(data=data, headers=headers):
    """
    完美资讯列表
    /mgmt/cms/perfectInfo/getInfoSettingList

    参数说明:
    - enableStatus: 启用状态: 0.禁用 1.启用 传null则为全部
    - pageNum: 页码
    - pageSize: 每页页数
    """

    url = "/mgmt/cms/perfectInfo/getInfoSettingList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
