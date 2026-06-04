import os

from util.client import client

data = {
    "enableStatus": 0,  # 启用状态: 0.禁用 1.启用 传null则为全部
    "memberType": 0,  # 顾客身份 1->会员；2->VIP会员；3->云商；4->微店（云+）
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 每页页数
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_backgroundStyle_getBackgroundStyleList(data=data, headers=headers):
    """
    背景样式列表
    /mgmt/cms/backgroundStyle/getBackgroundStyleList

    参数说明:
    - enableStatus: 启用状态: 0.禁用 1.启用 传null则为全部
    - memberType: 顾客身份 1->会员；2->VIP会员；3->云商；4->微店（云+）
    - pageNum: 页码
    - pageSize: 每页页数
    """

    url = "/mgmt/cms/backgroundStyle/getBackgroundStyleList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
