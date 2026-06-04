import os

from util.client import client

data = {
    "continueAmount": 0,  # 连续邀请最低数量
    "continueCalculation": 0,  # 连续邀请计算方式：1-固定 2-等级倍数
    "continueReward": 0,  # 连续邀请奖励
    "greaterCalculation": 0,  # 等级>=5计算方式：1-固定 2-等级倍数
    "greaterCalculationReward": 0,  # 等级>=5 奖励
    "icon": "",  # icon配置地址
    "id": 0,  # 主键Id
    "inviteName": "",  # 拉新名称
    "inviteType": 0,  # 拉新类型：1-邀请注册 2-连续任务
    "lessCalculation": 0,  # 等级<5计算方式：1-固定 2-等级倍数
    "lessCalculationReward": 0,  # 等级<5 奖励
    "remarks": "",  # 任务描述
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_rights_invite_editInvite(data=data, headers=headers):
    """
    编辑拉新奖励
    /mgmt/rights/invite/editInvite

    参数说明:
    - continueAmount: 连续邀请最低数量
    - continueCalculation: 连续邀请计算方式：1-固定 2-等级倍数
    - continueReward: 连续邀请奖励
    - greaterCalculation: 等级>=5计算方式：1-固定 2-等级倍数
    - greaterCalculationReward: 等级>=5 奖励
    - icon: icon配置地址
    - id: 主键Id
    - inviteName: 拉新名称
    - inviteType: 拉新类型：1-邀请注册 2-连续任务
    - lessCalculation: 等级<5计算方式：1-固定 2-等级倍数
    - lessCalculationReward: 等级<5 奖励
    - remarks: 任务描述
    """

    url = "/mgmt/rights/invite/editInvite"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
