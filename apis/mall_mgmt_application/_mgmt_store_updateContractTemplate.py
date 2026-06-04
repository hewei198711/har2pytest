import os
from urllib.parse import urlencode

from util.client import client

data = {
    "id": "",  # 主键id(必填)
    "type": "",  # 操作类型：1,停用；2,启用
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_store_updateContractTemplate(data=data, headers=headers):
    """
    启用/停用合同模板
    /mgmt/store/updateContractTemplate

    参数说明:
    - id: 主键id(必填)
    - type: 操作类型：1,停用；2,启用
    """

    url = "/mgmt/store/updateContractTemplate"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
