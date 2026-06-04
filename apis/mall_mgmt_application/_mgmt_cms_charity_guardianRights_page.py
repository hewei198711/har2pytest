import os

from util.client import client

data = {
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 每页页数
    "rightsTitle": "",  # 权益名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_charity_guardianRights_page(data=data, headers=headers):
    """
    公益购守护者权益列表分页查询
    /mgmt/cms/charity/guardianRights/page

    参数说明:
    - pageNum: 页码
    - pageSize: 每页页数
    - rightsTitle: 权益名称
    """

    url = "/mgmt/cms/charity/guardianRights/page"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
