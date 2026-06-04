import os

from util.client import client

data = {
    "activityId": 0,  # 活动id
    "customerCardNo": "",  # 会员卡号
    "customerMemberType": 0,  # 顾客身份
    "customerMobile": "",  # 注册手机号
    "customerRealName": "",  # 会员姓名
    "from": 0,  # TODO: 添加参数说明
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "platform": 0,  # 操作平台 分享平台:1-APP,2-PC,4-小程序
    "shareEndTime": "",  # 分享截止时间 yyyy-MM-dd HH:mm:ss
    "shareStartTime": "",  # 分享开始时间 yyyy-MM-dd HH:mm:ss
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_luckyActivity_getCustomerShareData(data=data, headers=headers):
    """
    查询顾客分享记录
    /mgmt/prmt/luckyActivity/getCustomerShareData

    参数说明:
    - activityId: 活动id
    - customerCardNo: 会员卡号
    - customerMemberType: 顾客身份
    - customerMobile: 注册手机号
    - customerRealName: 会员姓名
    - pageNum: 页数
    - pageSize: 每页显示数
    - platform: 操作平台 分享平台:1-APP,2-PC,4-小程序
    - shareEndTime: 分享截止时间 yyyy-MM-dd HH:mm:ss
    - shareStartTime: 分享开始时间 yyyy-MM-dd HH:mm:ss
    """

    url = "/mgmt/prmt/luckyActivity/getCustomerShareData"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
