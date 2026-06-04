import os

from util.client import client

data = {
    "ruleId": 0,  # TODO: 添加参数说明
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_warningRule_disable(data=data, headers=headers):
    """
    数据中心管理后台-预警规则管理-禁用预警规则
    /mgmt/dataAdmin/warningRule/disable
    """

    url = "/mgmt/dataAdmin/warningRule/disable"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
