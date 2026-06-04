import os

from util.client import client

params = {
    "enableStatus": 0,  # 是否启用, 0:禁用; 1:启用
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 每页页数
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_thematic_getThematicBarList(params=params, headers=headers):
    """
    获取专题页列表
    /mgmt/cms/thematic/getThematicBarList

    参数说明:
    - enableStatus: 是否启用, 0:禁用; 1:启用
    - pageNum: 页码
    - pageSize: 每页页数
    """

    url = "/mgmt/cms/thematic/getThematicBarList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
