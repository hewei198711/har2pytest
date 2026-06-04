import os

from util.client import client

params = {
    "endMonth": "",  # 结束月份
    "startMonth": "",  # 开始月份
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_monthly_return_list(params=params, headers=headers):
    """
    查询退货月结列表
    /mgmt/sys/monthly/return/list

    参数说明:
    - endMonth: 结束月份
    - startMonth: 开始月份
    """

    url = "/mgmt/sys/monthly/return/list"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
