import os

from util.client import client

data = {
    "appendix": "",  # 附件地址(逗号拼接)
    "opinion": "",  # 审核意见
    "ruleId": 0,  # 规则id
    "state": "",  # 状态:0禁用,1审核通过,3审核不通过
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_warningRule_check(data=data, headers=headers):
    """
    数据中心管理后台-预警规则管理-审核预警规则
    /mgmt/dataAdmin/warningRule/check

    参数说明:
    - appendix: 附件地址(逗号拼接)
    - opinion: 审核意见
    - ruleId: 规则id
    - state: 状态:0禁用,1审核通过,3审核不通过
    """

    url = "/mgmt/dataAdmin/warningRule/check"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
