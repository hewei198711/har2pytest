import os

from util.client import client

params = {
    "companyCode": "",  # 公司编码
    "pageNum": "",  # 当前页码,默认为1
    "pageSize": "",  # 当前显示的条数,默认为10
    "principal": "",  # 负责人
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_getComByCodeOrPri(params=params, headers=headers):
    """
    公司资料查询展示
    /mgmt/sys/getComByCodeOrPri

    参数说明:
    - companyCode: 公司编码
    - pageNum: 当前页码,默认为1
    - pageSize: 当前显示的条数,默认为10
    - principal: 负责人
    """

    url = "/mgmt/sys/getComByCodeOrPri"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
