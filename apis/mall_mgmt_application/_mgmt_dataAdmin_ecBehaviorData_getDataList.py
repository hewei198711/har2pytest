import os

from util.client import client

data = {
    "behaviorColleteTimeZone": "",  # 行为时间查询区间
    "behaviorTypeList": [],  # 行为类型: 2.浏览页面 3.搜索兑换品 4.浏览兑换品分类 5.浏览兑换品 6.提交兑换单 7.取消兑换单 8.加入兑换车 9.banner图点击 10.banner图曝光
    "cardNo": "",  # 会员卡号
    "certificatesNo": "",  # 证件号码
    "channelList": [],  # 渠道
    "mobile": "",  # 注册手机号
    "oneId": "",  # oneId
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_ecBehaviorData_getDataList(data=data, headers=headers):
    """
    查询行为数据
    /mgmt/dataAdmin/ecBehaviorData/getDataList

    参数说明:
    - behaviorColleteTimeZone: 行为时间查询区间
    - behaviorTypeList: 行为类型: 2.浏览页面 3.搜索兑换品 4.浏览兑换品分类 5.浏览兑换品 6.提交兑换单 7.取消兑换单 8.加入兑换车 9.banner图点击 10.banner图曝光
    - cardNo: 会员卡号
    - certificatesNo: 证件号码
    - channelList: 渠道
    - mobile: 注册手机号
    - oneId: oneId
    """

    url = "/mgmt/dataAdmin/ecBehaviorData/getDataList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
