import os
from urllib.parse import urlencode

from util.client import client

data = {
    "docNo": "",  # 合同编号，多个用英文逗号分隔
    "pass": 0,  # 是否通过，1、通过、2：驳回
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_store_batchAuditOfflineContracts(data=data, headers=headers):
    """
    线下合同批量审核
    /mgmt/store/batchAuditOfflineContracts

    参数说明:
    - docNo: 合同编号，多个用英文逗号分隔
    - pass: 是否通过，1、通过、2：驳回
    """

    url = "/mgmt/store/batchAuditOfflineContracts"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
