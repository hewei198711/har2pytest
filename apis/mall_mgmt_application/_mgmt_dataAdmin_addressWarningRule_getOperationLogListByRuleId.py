import os

from util.client import client

params = {
    "ruleId": 0,  # ruleId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_addressWarningRule_getOperationLogListByRuleId(params=params, headers=headers):
    """
    根据ruleId获取操作日志
    /mgmt/dataAdmin/addressWarningRule/getOperationLogListByRuleId

    参数说明:
    - ruleId: ruleId
    """

    url = "/mgmt/dataAdmin/addressWarningRule/getOperationLogListByRuleId"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
