import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_holiday_bath_template(headers=headers):
    """
    获取批量导入假期模板
    /mgmt/sys/holiday/bath/template
    """

    url = "/mgmt/sys/holiday/bath/template"
    with client.get(url=url, headers=headers) as r:
        return r
