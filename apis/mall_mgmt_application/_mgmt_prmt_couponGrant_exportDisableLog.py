import os

from util.client import client

params = {
    "cardNo": "",  # 会员卡号
    "endTime": "",  # 编辑时间止区
    "id": 0,  # 活动主键
    "mobile": "",  # 手机号
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页数量
    "realName": "",  # 会员姓名
    "startTime": "",  # 编辑时间起区
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_couponGrant_exportDisableLog(params=params, headers=headers):
    """
    导出不派发顾客编辑记录
    /mgmt/prmt/couponGrant/exportDisableLog

    参数说明:
    - cardNo: 会员卡号
    - endTime: 编辑时间止区
    - id: 活动主键
    - mobile: 手机号
    - pageNum: 当前页
    - pageSize: 每页数量
    - realName: 会员姓名
    - startTime: 编辑时间起区
    """

    url = "/mgmt/prmt/couponGrant/exportDisableLog"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
