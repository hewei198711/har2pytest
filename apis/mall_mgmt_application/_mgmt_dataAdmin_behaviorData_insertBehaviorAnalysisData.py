import os

from util.client import client

data = {
    "modelType": "",  # 操作平台类型 APP、PC、WEIXIN_PROGRAM
    "plateformType": 0,  # 页数据类型 1.商城首页 2.专区
    "timeZoneEnd": "",  # 查询时间范围结束 时间格式 2024-12-01 14:00:00
    "timeZoneStart": "",  # 查询时间范围开始 时间格式 2024-12-01 00:00:00
    "timeZoneType": 0,  # 查询时间类型 1、按月、2、按天、3、按小时
    "zoneId": 0,  # 专区id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_behaviorData_insertBehaviorAnalysisData(data=data, headers=headers):
    """
    专区页、常规页生成数据看板
    /mgmt/dataAdmin/behaviorData/insertBehaviorAnalysisData

    参数说明:
    - modelType: 操作平台类型 APP、PC、WEIXIN_PROGRAM
    - plateformType: 页数据类型 1.商城首页 2.专区
    - timeZoneEnd: 查询时间范围结束 时间格式 2024-12-01 14:00:00
    - timeZoneStart: 查询时间范围开始 时间格式 2024-12-01 00:00:00
    - timeZoneType: 查询时间类型 1、按月、2、按天、3、按小时
    - zoneId: 专区id
    """

    url = "/mgmt/dataAdmin/behaviorData/insertBehaviorAnalysisData"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
