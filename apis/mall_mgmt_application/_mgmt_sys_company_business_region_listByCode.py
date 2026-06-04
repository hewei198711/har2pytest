import os

from util.client import client

params = {
    "companyCode": "",  # companyCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_company_business_region_listByCode(params=params, headers=headers):
    """
    获取分公司业务范围集合(根据编号查询)
    /mgmt/sys/company/business/region/listByCode

    参数说明:
    - companyCode: companyCode
    """

    url = "/mgmt/sys/company/business/region/listByCode"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
