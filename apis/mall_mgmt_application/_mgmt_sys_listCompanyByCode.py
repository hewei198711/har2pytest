import os

from util.client import client

params = {
    "companyCode": "",  # 公司编码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_listCompanyByCode(params=params, headers=headers):
    """
    根据分公司编码模糊查询公司信息集合
    /mgmt/sys/listCompanyByCode

    参数说明:
    - companyCode: 公司编码
    """

    url = "/mgmt/sys/listCompanyByCode"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
