import os

from util.client import client

params = {
    "companyCode": "",  # companyCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_listCompanyBaseByCode(params=params, headers=headers):
    """
    根据分公司编码模糊查询公司基础信息集合
    /mgmt/sys/listCompanyBaseByCode

    参数说明:
    - companyCode: companyCode
    """

    url = "/mgmt/sys/listCompanyBaseByCode"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
