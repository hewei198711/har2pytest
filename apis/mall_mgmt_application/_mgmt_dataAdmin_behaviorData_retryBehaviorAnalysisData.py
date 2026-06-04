import os
from urllib.parse import urlencode

from util.client import client

data = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_dataAdmin_behaviorData_retryBehaviorAnalysisData(data=data, headers=headers):
    """
    专区页、常规数据重试
    /mgmt/dataAdmin/behaviorData/retryBehaviorAnalysisData

    参数说明:
    - id: id
    """

    url = "/mgmt/dataAdmin/behaviorData/retryBehaviorAnalysisData"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
