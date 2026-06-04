import os

from util.client import client

params = {
    "companyId": 0,  # companyId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_company_business_region_list(params=params, headers=headers):
    """
    获取分公司业务范围集合
    /mgmt/sys/company/business/region/list

    参数说明:
    - companyId: companyId
    """

    url = "/mgmt/sys/company/business/region/list"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
