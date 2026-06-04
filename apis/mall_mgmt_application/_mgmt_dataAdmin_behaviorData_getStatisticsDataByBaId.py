import os

from util.client import client

data = {
    "baId": 0,  # 行为数据分析总表id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_behaviorData_getStatisticsDataByBaId(data=data, headers=headers):
    """
    查询概览页数据
    /mgmt/dataAdmin/behaviorData/getStatisticsDataByBaId

    参数说明:
    - baId: 行为数据分析总表id
    """

    url = "/mgmt/dataAdmin/behaviorData/getStatisticsDataByBaId"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
