import os

from util.client import client

data = {
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
    "promotionLinkId": 0,  # 推广链接id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_promotionLink_getLinkDetailPage(data=data, headers=headers):
    """
    获取第三方软件推广链接详情数据列表分页
    /mgmt/cms/promotionLink/getLinkDetailPage

    参数说明:
    - promotionLinkId: 推广链接id
    """

    url = "/mgmt/cms/promotionLink/getLinkDetailPage"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
