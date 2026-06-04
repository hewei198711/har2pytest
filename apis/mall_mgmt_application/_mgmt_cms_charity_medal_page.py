import os

from util.client import client

data = {
    "medalTitle": "",  # 勋章名称
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 每页页数
    "status": 0,  # 状态: 1.启用 2.禁用
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_charity_medal_page(data=data, headers=headers):
    """
    公益购勋章列表分页查询
    /mgmt/cms/charity/medal/page

    参数说明:
    - medalTitle: 勋章名称
    - pageNum: 页码
    - pageSize: 每页页数
    - status: 状态: 1.启用 2.禁用
    """

    url = "/mgmt/cms/charity/medal/page"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
