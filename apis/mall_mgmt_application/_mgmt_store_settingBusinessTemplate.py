import os

from util.client import client

data = {
    "contractType": 0,  # 合同类型，1/经营合同（默认），2/协议
    "templateNo": "",  # 合同模板编码，多个用逗号分隔
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_settingBusinessTemplate(data=data, headers=headers):
    """
    设置经营合同模板
    /mgmt/store/settingBusinessTemplate

    参数说明:
    - contractType: 合同类型，1/经营合同（默认），2/协议
    - templateNo: 合同模板编码，多个用逗号分隔
    """

    url = "/mgmt/store/settingBusinessTemplate"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
