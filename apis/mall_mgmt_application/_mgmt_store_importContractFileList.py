import os
from urllib.parse import urlencode

from util.client import client

data = {
    "contractType": 0,  # 合同类型，1/经营合同，2/协议
    "params": "",  # 文件名称与URL键值对字符串
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_store_importContractFileList(data=data, headers=headers):
    """
    批量导入双方签署合同(文件版)
    /mgmt/store/importContractFileList

    参数说明:
    - contractType: 合同类型，1/经营合同，2/协议
    - params: 文件名称与URL键值对字符串
    """

    url = "/mgmt/store/importContractFileList"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
