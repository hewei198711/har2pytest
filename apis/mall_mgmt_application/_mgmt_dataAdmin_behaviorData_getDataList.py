import os

from util.client import client

data = {
    "behaviorColleteTimeZone": "",  # 行为时间查询区间
    "behaviorType": 0,  # 行为类型: 1.注册 2.浏览页面 3.浏览商品 4.收藏商品 5.分享商品 6.加购商品 7.购买商品 null或其它为全部
    "cardNo": "",  # 会员卡号
    "company": "",  # 服务中心所属分公司
    "isShare": 0,  # 是否企微带参 0:否 1:是
    "mobile": "",  # 注册手机号
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
    "sharerMobile": "",  # 经销商手机号
    "sharerName": "",  # 经销商姓名
    "storeCode": "",  # 服务中心编号
    "userName": "",  # 顾客姓名
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_behaviorData_getDataList(data=data, headers=headers):
    """
    查询行为数据
    /mgmt/dataAdmin/behaviorData/getDataList

    参数说明:
    - behaviorColleteTimeZone: 行为时间查询区间
    - behaviorType: 行为类型: 1.注册 2.浏览页面 3.浏览商品 4.收藏商品 5.分享商品 6.加购商品 7.购买商品 null或其它为全部
    - cardNo: 会员卡号
    - company: 服务中心所属分公司
    - isShare: 是否企微带参 0:否 1:是
    - mobile: 注册手机号
    - sharerMobile: 经销商手机号
    - sharerName: 经销商姓名
    - storeCode: 服务中心编号
    - userName: 顾客姓名
    """

    url = "/mgmt/dataAdmin/behaviorData/getDataList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
