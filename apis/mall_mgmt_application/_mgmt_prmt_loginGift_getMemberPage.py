import os

from util.client import client

params = {
    "cardNo": "",  # 会员卡号
    "disabled": False,  # 是否已禁用
    "endTime": "",  # 领取时间止区
    "id": 0,  # 活动主键
    "mobile": "",  # 手机号
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页数量
    "realName": "",  # 会员姓名
    "received": False,  # 是否已领取
    "selectedIds": [],  # 选中记录id
    "startTime": "",  # 领取时间起区
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_loginGift_getMemberPage(params=params, headers=headers):
    """
    分页查询活动顾客
    /mgmt/prmt/loginGift/getMemberPage

    参数说明:
    - cardNo: 会员卡号
    - disabled: 是否已禁用
    - endTime: 领取时间止区
    - id: 活动主键
    - mobile: 手机号
    - pageNum: 当前页
    - pageSize: 每页数量
    - realName: 会员姓名
    - received: 是否已领取
    - selectedIds: 选中记录id
    - startTime: 领取时间起区
    """

    url = "/mgmt/prmt/loginGift/getMemberPage"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
