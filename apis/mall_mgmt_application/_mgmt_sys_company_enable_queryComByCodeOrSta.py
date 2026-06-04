import os

from util.client import client

data = {
    "companyCode": "",  # 公司编码
    "enableStatus": 0,  # 状态 1：启用 0：禁用
    "pageNum": 0,  # 页 默认1
    "pageSize": 0,  # 每页数量 默认10
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_company_enable_queryComByCodeOrSta(data=data, headers=headers):
    """
    上门取件公司列表查询
    /mgmt/sys/company/enable/queryComByCodeOrSta

    参数说明:
    - companyCode: 公司编码
    - enableStatus: 状态 1：启用 0：禁用
    - pageNum: 页 默认1
    - pageSize: 每页数量 默认10
    """

    url = "/mgmt/sys/company/enable/queryComByCodeOrSta"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
