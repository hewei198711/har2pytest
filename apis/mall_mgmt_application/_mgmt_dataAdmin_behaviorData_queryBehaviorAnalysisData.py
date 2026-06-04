import os

from util.client import client

data = {
    "modelType": "",  # 操作平台类型 APP、PC、WEIXIN_PROGRAM
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
    "plateformType": 0,  # 1.商城首页 2.专区
    "timeZoneEnd": "",  # 查询时间范围结束
    "timeZoneStart": "",  # 查询时间范围开始
    "timeZoneType": 0,  # 查询时间类型
    "zoneId": 0,  # 专区id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_behaviorData_queryBehaviorAnalysisData(data=data, headers=headers):
    """
    专区页、常规页查询数据看板明细
    /mgmt/dataAdmin/behaviorData/queryBehaviorAnalysisData

    参数说明:
    - modelType: 操作平台类型 APP、PC、WEIXIN_PROGRAM
    - plateformType: 1.商城首页 2.专区
    - timeZoneEnd: 查询时间范围结束
    - timeZoneStart: 查询时间范围开始
    - timeZoneType: 查询时间类型
    - zoneId: 专区id
    """

    url = "/mgmt/dataAdmin/behaviorData/queryBehaviorAnalysisData"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
