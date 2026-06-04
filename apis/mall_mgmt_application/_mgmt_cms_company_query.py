import os

from util.client import client

data = {
    "companyCode": "",  # 分公司编号
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 每页页数
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_company_query(data=data, headers=headers):
    """
    分页查询分公司信息
    /mgmt/cms/company/query

    参数说明:
    - companyCode: 分公司编号
    - pageNum: 页码
    - pageSize: 每页页数
    """

    url = "/mgmt/cms/company/query"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
