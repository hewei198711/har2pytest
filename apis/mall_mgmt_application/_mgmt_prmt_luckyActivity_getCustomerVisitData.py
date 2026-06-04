import os

from util.client import client

data = {
    "activityId": 0,  # 活动id
    "from": 0,  # TODO: 添加参数说明
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "platform": 0,  # 访问平台 分享平台:1-APP,2-PC,4-小程序
    "shareCustomerCardNo": "",  # 分享人会员卡号
    "shareCustomerMemberType": 0,  # 分享人顾客身份
    "shareCustomerMobile": "",  # 分享人注册手机号
    "shareCustomerRealName": "",  # 分享人会员姓名
    "visitCustomerCardNo": "",  # 访问人会员卡号
    "visitCustomerMemberType": 0,  # 访问人顾客身份
    "visitCustomerMobile": "",  # 访问人注册手机号
    "visitCustomerRealName": "",  # 访问人会员姓名
    "visitEndTime": "",  # 访问截止时间 yyyy-MM-dd HH:mm:ss
    "visitStartTime": "",  # 访问开始时间 yyyy-MM-dd HH:mm:ss
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_luckyActivity_getCustomerVisitData(data=data, headers=headers):
    """
    查询顾客访问记录
    /mgmt/prmt/luckyActivity/getCustomerVisitData

    参数说明:
    - activityId: 活动id
    - pageNum: 页数
    - pageSize: 每页显示数
    - platform: 访问平台 分享平台:1-APP,2-PC,4-小程序
    - shareCustomerCardNo: 分享人会员卡号
    - shareCustomerMemberType: 分享人顾客身份
    - shareCustomerMobile: 分享人注册手机号
    - shareCustomerRealName: 分享人会员姓名
    - visitCustomerCardNo: 访问人会员卡号
    - visitCustomerMemberType: 访问人顾客身份
    - visitCustomerMobile: 访问人注册手机号
    - visitCustomerRealName: 访问人会员姓名
    - visitEndTime: 访问截止时间 yyyy-MM-dd HH:mm:ss
    - visitStartTime: 访问开始时间 yyyy-MM-dd HH:mm:ss
    """

    url = "/mgmt/prmt/luckyActivity/getCustomerVisitData"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
