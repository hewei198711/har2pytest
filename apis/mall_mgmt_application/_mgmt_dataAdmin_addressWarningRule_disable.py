import os

from util.client import client

data = {
    "ruleId": 0,  # TODO: 添加参数说明
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_addressWarningRule_disable(data=data, headers=headers):
    """
    禁用预警规则
    /mgmt/dataAdmin/addressWarningRule/disable
    """

    url = "/mgmt/dataAdmin/addressWarningRule/disable"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
