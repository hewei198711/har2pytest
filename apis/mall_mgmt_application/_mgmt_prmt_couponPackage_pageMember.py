import os

from util.client import client

params = {
    "id": 0,  # 活动主键
    "importKey": "",  # 导入操作键
    "memberCard": "",  # 会员卡号
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页数量
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_couponPackage_pageMember(params=params, headers=headers):
    """
    分页查询导入派发顾客
    /mgmt/prmt/couponPackage/pageMember

    参数说明:
    - id: 活动主键
    - importKey: 导入操作键
    - memberCard: 会员卡号
    - pageNum: 当前页
    - pageSize: 每页数量
    """

    url = "/mgmt/prmt/couponPackage/pageMember"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
