import os

from util.client import client

data = {
    "companyId": 0,  # 公司id
    "provinceCodes": [],  # 省份编码集
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_getChoiceDistricts(data=data, headers=headers):
    """
    此省份已被其他公司选择的地区
    /mgmt/sys/getChoiceDistricts

    参数说明:
    - companyId: 公司id
    - provinceCodes: 省份编码集
    """

    url = "/mgmt/sys/getChoiceDistricts"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
