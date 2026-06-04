import os

from util.client import client

data = {
    "behaviorColleteTimeZone": "",  # 行为时间查询区间
    "behaviorType": 0,  # 行为类型: 2.浏览页面 3.搜索兑换品 4.浏览兑换品分类 5.浏览兑换品 6.提交兑换单 7.取消兑换单 8.加入兑换车 9.banner图点击 10.banner图曝光 null或不传为总表
    "oneId": 0,  # oneId
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
    "sortColumn": "",  # 排序字段
    "sortType": "",  # 排序方式 asc:正序 desc:倒序
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_ecBehaviorData_getDetailDataList(data=data, headers=headers):
    """
    查询行为详情数据列表
    /mgmt/dataAdmin/ecBehaviorData/getDetailDataList

    参数说明:
    - behaviorColleteTimeZone: 行为时间查询区间
    - behaviorType: 行为类型: 2.浏览页面 3.搜索兑换品 4.浏览兑换品分类 5.浏览兑换品 6.提交兑换单 7.取消兑换单 8.加入兑换车 9.banner图点击 10.banner图曝光 null或不传为总表
    - oneId: oneId
    - sortColumn: 排序字段
    - sortType: 排序方式 asc:正序 desc:倒序
    """

    url = "/mgmt/dataAdmin/ecBehaviorData/getDetailDataList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
