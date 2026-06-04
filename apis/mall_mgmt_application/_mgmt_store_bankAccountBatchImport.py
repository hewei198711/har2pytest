import os
from urllib.parse import urlencode

from util.client import client

data = {
    "params": "",  # 许可证名称与URL键值对字符串
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_store_bankAccountBatchImport(data=data, headers=headers):
    """
    批量导入银行账号
    /mgmt/store/bankAccountBatchImport

    参数说明:
    - params: 许可证名称与URL键值对字符串
    """

    url = "/mgmt/store/bankAccountBatchImport"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
