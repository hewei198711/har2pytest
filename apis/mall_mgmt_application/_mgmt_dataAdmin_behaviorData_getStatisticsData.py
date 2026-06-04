import os

from util.client import client

data = {
    "behaviorType": 0,  # 行为类型: 1.注册 2.浏览页面 3.浏览商品 4.收藏商品 5.分享商品 6.加购商品 7.购买商品 null或其它为全部
    "endMonth": "",  # 截止月份
    "isShare": 0,  # 是否企微带参 0:否 1:是
    "memberType": 0,  # 用户类型 1.会员 2.VIP会员 3.云商 4.微店
    "startMonth": "",  # 起始月份
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_behaviorData_getStatisticsData(data=data, headers=headers):
    """
    查询概览页数据
    /mgmt/dataAdmin/behaviorData/getStatisticsData

    参数说明:
    - behaviorType: 行为类型: 1.注册 2.浏览页面 3.浏览商品 4.收藏商品 5.分享商品 6.加购商品 7.购买商品 null或其它为全部
    - endMonth: 截止月份
    - isShare: 是否企微带参 0:否 1:是
    - memberType: 用户类型 1.会员 2.VIP会员 3.云商 4.微店
    - startMonth: 起始月份
    """

    url = "/mgmt/dataAdmin/behaviorData/getStatisticsData"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
