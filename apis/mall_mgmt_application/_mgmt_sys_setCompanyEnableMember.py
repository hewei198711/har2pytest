import os

from util.client import client

data = {
    "id": 0,  # 主键id
    "memberTypeList": [],  # 顾客身份集合:1-会员 2-Vip会员 3-云商 4-微店
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_setCompanyEnableMember(data=data, headers=headers):
    """
    数字人名币-设置用户
    /mgmt/sys/setCompanyEnableMember

    参数说明:
    - id: 主键id
    - memberTypeList: 顾客身份集合:1-会员 2-Vip会员 3-云商 4-微店
    """

    url = "/mgmt/sys/setCompanyEnableMember"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
