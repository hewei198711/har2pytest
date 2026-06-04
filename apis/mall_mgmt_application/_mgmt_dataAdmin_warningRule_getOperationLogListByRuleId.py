import os

from util.client import client

params = {
    "ruleId": 0,  # ruleId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_warningRule_getOperationLogListByRuleId(params=params, headers=headers):
    """
    数据中心管理后台-预警规则管理-根据ruleId获取操作日志
    /mgmt/dataAdmin/warningRule/getOperationLogListByRuleId

    参数说明:
    - ruleId: ruleId
    """

    url = "/mgmt/dataAdmin/warningRule/getOperationLogListByRuleId"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
