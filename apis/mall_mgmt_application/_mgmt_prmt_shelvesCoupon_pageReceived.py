import os

from util.client import client

params = {
    "cardNo": "",  # 会员卡号
    "getTimeEnd": "",  # 领取时间止区
    "getTimeStart": "",  # 领取时间起区
    "id": 0,  # 优惠券上架id
    "mobile": "",  # 手机号
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页数量
    "platform": 0,  # 领取平台:1-APP,2-PC,4-小程序
    "realName": "",  # 会员姓名
    "shelvesChannel": 0,  # 领取入口:1-商品详情,2-领券中心
    "state": 0,  # 优惠券状态:0-未领取,1-未使用,2-已使用,3-已作废,4-已失效,5-占用中
    "useTimeEnd": "",  # 使用时间止区
    "useTimeStart": "",  # 使用时间起区
    "usedPlatform": 0,  # 使用平台:1-APP,2-PC,4-小程序
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_shelvesCoupon_pageReceived(params=params, headers=headers):
    """
    分页查询领取列表
    /mgmt/prmt/shelvesCoupon/pageReceived

    参数说明:
    - cardNo: 会员卡号
    - getTimeEnd: 领取时间止区
    - getTimeStart: 领取时间起区
    - id: 优惠券上架id
    - mobile: 手机号
    - pageNum: 当前页
    - pageSize: 每页数量
    - platform: 领取平台:1-APP,2-PC,4-小程序
    - realName: 会员姓名
    - shelvesChannel: 领取入口:1-商品详情,2-领券中心
    - state: 优惠券状态:0-未领取,1-未使用,2-已使用,3-已作废,4-已失效,5-占用中
    - useTimeEnd: 使用时间止区
    - useTimeStart: 使用时间起区
    - usedPlatform: 使用平台:1-APP,2-PC,4-小程序
    """

    url = "/mgmt/prmt/shelvesCoupon/pageReceived"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
