import os

from util.client import client

params = {
    "cardNo": "",  # 会员卡号
    "endTime": "",  # 获奖时间止(yyyy-MM-dd)
    "mobile": "",  # 注册手机号
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页数量
    "realname": "",  # 会员姓名
    "rewardChannel": 0,  # 奖励渠道 3-邀请注册,4-连续邀请
    "startTime": "",  # 获奖时间起(yyyy-MM-dd)
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_rights_invite_getInviteData(params=params, headers=headers):
    """
    获取拉新奖励日志
    /mgmt/rights/invite/getInviteData

    参数说明:
    - cardNo: 会员卡号
    - endTime: 获奖时间止(yyyy-MM-dd)
    - mobile: 注册手机号
    - pageNum: 当前页
    - pageSize: 每页数量
    - realname: 会员姓名
    - rewardChannel: 奖励渠道 3-邀请注册,4-连续邀请
    - startTime: 获奖时间起(yyyy-MM-dd)
    """

    url = "/mgmt/rights/invite/getInviteData"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
