import os

from util.client import client

params = {
    "customerCard": "",  # 会员卡号
    "customerName": "",  # 会员名称
    "endTime": "",  # 抽奖时间止区(yyyy-MM-dd)
    "extInfo": "",  # 兑奖码
    "id": 0,  # 活动id
    "isLucky": 0,  # 是否中奖(0:否；1：是)
    "luckyType": 0,  # 使用抽奖机会类型(1-原始抽奖 2-分享抽奖 3-分享助力抽奖)
    "memberType": 0,  # 顾客身份
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页数量
    "prizeSendState": 0,  # 派奖状态(1;待派奖；2：派奖成功；3：派奖失败；4：不派奖)
    "registerPhone": "",  # 注册手机号
    "startTime": "",  # 抽奖时间起区(yyyy-MM-dd)
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_luckyActivity_exportDistinctCustomerLuckyPage(params=params, headers=headers):
    """
    导出抽奖用户参与情况
    /mgmt/prmt/luckyActivity/exportDistinctCustomerLuckyPage

    参数说明:
    - customerCard: 会员卡号
    - customerName: 会员名称
    - endTime: 抽奖时间止区(yyyy-MM-dd)
    - extInfo: 兑奖码
    - id: 活动id
    - isLucky: 是否中奖(0:否；1：是)
    - luckyType: 使用抽奖机会类型(1-原始抽奖 2-分享抽奖 3-分享助力抽奖)
    - memberType: 顾客身份
    - pageNum: 当前页
    - pageSize: 每页数量
    - prizeSendState: 派奖状态(1;待派奖；2：派奖成功；3：派奖失败；4：不派奖)
    - registerPhone: 注册手机号
    - startTime: 抽奖时间起区(yyyy-MM-dd)
    """

    url = "/mgmt/prmt/luckyActivity/exportDistinctCustomerLuckyPage"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
