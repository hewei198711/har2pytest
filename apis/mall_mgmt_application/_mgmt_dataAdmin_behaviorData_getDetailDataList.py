import os

from util.client import client

data = {
    "behaviorColleteTimeZone": "",  # 行为时间查询区间
    "behaviorType": 0,  # 行为类型: 1.注册 2.浏览页面 3.浏览商品 4.收藏商品 5.分享商品 6.加购商品 7.购买商品 null或其它为全部
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
    "sharerCardNo": "",  # 分享经销商卡号
    "sortColumn": "",  # 排序字段
    "sortType": "",  # 排序方式 asc:正序 desc:倒序
    "userId": 0,  # 会员id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_behaviorData_getDetailDataList(data=data, headers=headers):
    """
    查询行为详情数据列表(用户)
    /mgmt/dataAdmin/behaviorData/getDetailDataList

    参数说明:
    - behaviorColleteTimeZone: 行为时间查询区间
    - behaviorType: 行为类型: 1.注册 2.浏览页面 3.浏览商品 4.收藏商品 5.分享商品 6.加购商品 7.购买商品 null或其它为全部
    - sharerCardNo: 分享经销商卡号
    - sortColumn: 排序字段
    - sortType: 排序方式 asc:正序 desc:倒序
    - userId: 会员id
    """

    url = "/mgmt/dataAdmin/behaviorData/getDetailDataList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
