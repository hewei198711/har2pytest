import os

from util.client import client

data = {
    "cardNo": "",  # 会员卡号
    "endTime": "",  # 编辑时间止区
    "id": 0,  # 活动主键
    "memberId": 0,  # TODO: 添加参数说明
    "memberType": 0,  # TODO: 添加参数说明
    "mobile": "",  # 手机号
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页数量
    "realName": "",  # 会员姓名
    "startTime": "",  # 编辑时间起区
    "type": 0,  # 领券中心导入顾客类型：0-上架对象，1-领取对象
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_combine_pageMemberLog(data=data, headers=headers):
    """
    可购顾客编辑记录
    /mgmt/prmt/combine/pageMemberLog

    参数说明:
    - cardNo: 会员卡号
    - endTime: 编辑时间止区
    - id: 活动主键
    - mobile: 手机号
    - pageNum: 当前页
    - pageSize: 每页数量
    - realName: 会员姓名
    - startTime: 编辑时间起区
    - type: 领券中心导入顾客类型：0-上架对象，1-领取对象
    """

    url = "/mgmt/prmt/combine/pageMemberLog"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
