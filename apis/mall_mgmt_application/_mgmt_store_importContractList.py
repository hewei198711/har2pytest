import os
from urllib.parse import urlencode

from util.client import client

data = {
    "contractType": "",  # 合同类型，1/经营合同（默认），2/协议
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_store_importContractList(data=data, headers=headers):
    """
    批量导入合同
    /mgmt/store/importContractList

    参数说明:
    - contractType: 合同类型，1/经营合同（默认），2/协议
    """

    url = "/mgmt/store/importContractList"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
