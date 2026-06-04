import os

from util.client import client

params = {
    "configTime": "",  # 配置时间
    "effectiveDate": "",  # 生效日期
    "id": "",  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_updateOrderConfigTime(params=params, headers=headers):
    """
    更新退货或订货的截至时间
    /mgmt/sys/updateOrderConfigTime

    参数说明:
    - configTime: 配置时间
    - effectiveDate: 生效日期
    - id: id
    """

    url = "/mgmt/sys/updateOrderConfigTime"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
