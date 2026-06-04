import os

from util.client import client

data = {
    "channel": "",  # 渠道
    "searchTime": "",  # 查询时间
    "searchType": "",  # 查询类型:1.按月查询 2.按日查询
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_ecBehaviorData_getStatisticsData(data=data, headers=headers):
    """
    查询概览页数据
    /mgmt/dataAdmin/ecBehaviorData/getStatisticsData

    参数说明:
    - channel: 渠道
    - searchTime: 查询时间
    - searchType: 查询类型:1.按月查询 2.按日查询
    """

    url = "/mgmt/dataAdmin/ecBehaviorData/getStatisticsData"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
