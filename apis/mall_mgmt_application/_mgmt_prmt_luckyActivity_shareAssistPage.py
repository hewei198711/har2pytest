import os

from util.client import client

params = {
    "activityId": 0,  # 抽奖活动id
    "assistCard": "",  # 助力人会员卡号
    "assistEndTime": "",  # 助力结束时间
    "assistMemberType": 0,  # 助力人顾客身份 1-普通顾客 2-优惠顾客 3-云商 4-微店
    "assistMobile": "",  # 助力人手机号
    "assistName": "",  # 助力人姓名
    "assistStartTime": "",  # 助力开始时间
    "shareCard": "",  # 分享人会员卡号
    "shareMemberType": 0,  # 分享人顾客身份 1-普通顾客 2-优惠顾客 3-云商 4-微店
    "shareMobile": "",  # 分享人手机号
    "shareName": "",  # 分享人姓名
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_luckyActivity_shareAssistPage(params=params, headers=headers):
    """
    shareAssistPage
    /mgmt/prmt/luckyActivity/shareAssistPage

    参数说明:
    - activityId: 抽奖活动id
    - assistCard: 助力人会员卡号
    - assistEndTime: 助力结束时间
    - assistMemberType: 助力人顾客身份 1-普通顾客 2-优惠顾客 3-云商 4-微店
    - assistMobile: 助力人手机号
    - assistName: 助力人姓名
    - assistStartTime: 助力开始时间
    - shareCard: 分享人会员卡号
    - shareMemberType: 分享人顾客身份 1-普通顾客 2-优惠顾客 3-云商 4-微店
    - shareMobile: 分享人手机号
    - shareName: 分享人姓名
    """

    url = "/mgmt/prmt/luckyActivity/shareAssistPage"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
