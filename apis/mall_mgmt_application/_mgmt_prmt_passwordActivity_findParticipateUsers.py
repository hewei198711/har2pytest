import os

from util.client import client

data = {
    "customerCard": "",  # 会员卡号
    "enterpriseWechatAddBeginTime": "",  # 企微添加开始时间
    "enterpriseWechatAddEndTime": "",  # 企微添加结束时间
    "memberInvalidCardActive": 0,  # 是否失效卡激活(0:否；1：是)
    "memberSleep": 0,  # 是否沉睡顾客(0:否；1：是)
    "memberType": 0,  # 顾客身份
    "mobile": "",  # 手机号码
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页数量
    "promotionId": 0,  # 活动id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_passwordActivity_findParticipateUsers(data=data, headers=headers):
    """
    口令活动参与用户列表
    /mgmt/prmt/passwordActivity/findParticipateUsers

    参数说明:
    - customerCard: 会员卡号
    - enterpriseWechatAddBeginTime: 企微添加开始时间
    - enterpriseWechatAddEndTime: 企微添加结束时间
    - memberInvalidCardActive: 是否失效卡激活(0:否；1：是)
    - memberSleep: 是否沉睡顾客(0:否；1：是)
    - memberType: 顾客身份
    - mobile: 手机号码
    - pageNum: 当前页
    - pageSize: 每页数量
    - promotionId: 活动id
    """

    url = "/mgmt/prmt/passwordActivity/findParticipateUsers"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
