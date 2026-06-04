import os

from util.client import client

params = {
    "companyCode": "",  # companyCode
    "principal": "",  # principal
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_getCompanyList(params=params, headers=headers):
    """
    查询公司基本信息
    /mgmt/sys/getCompanyList

    参数说明:
    - companyCode: companyCode
    - principal: principal
    """

    url = "/mgmt/sys/getCompanyList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
