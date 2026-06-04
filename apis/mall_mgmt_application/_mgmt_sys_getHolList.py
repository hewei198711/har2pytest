import os

from util.client import client

params = {
    "desc": "",  # 是否按时间逆序
    "month": "",  # 月
    "pageNum": "",  # 当前页码,默认为1
    "pageSize": "",  # 当前显示的条数,默认为10
    "year": "",  # 年
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_getHolList(params=params, headers=headers):
    """
    展示节假日页面
    /mgmt/sys/getHolList

    参数说明:
    - desc: 是否按时间逆序
    - month: 月
    - pageNum: 当前页码,默认为1
    - pageSize: 当前显示的条数,默认为10
    - year: 年
    """

    url = "/mgmt/sys/getHolList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
