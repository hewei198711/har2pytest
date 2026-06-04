import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_sys_importHoliday(headers=headers):
    """
    批量导入假期
    /mgmt/sys/importHoliday
    """

    url = "/mgmt/sys/importHoliday"
    with client.post(url=url, headers=headers) as r:
        return r
