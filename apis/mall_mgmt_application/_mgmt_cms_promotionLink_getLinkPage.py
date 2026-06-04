import os

from util.client import client

data = {
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_promotionLink_getLinkPage(data=data, headers=headers):
    """
    获取第三方软件推广链接列表分页
    /mgmt/cms/promotionLink/getLinkPage
    """

    url = "/mgmt/cms/promotionLink/getLinkPage"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
