import os

from util.client import client

data = {
    "holidayFlag": 0,  # 是否是节假日：1.是;0.否
    "id": 0,  # id
    "remarks": "",  # 备注
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_updateHoliday(data=data, headers=headers):
    """
    编辑假期
    /mgmt/sys/updateHoliday

    参数说明:
    - holidayFlag: 是否是节假日：1.是;0.否
    - id: id
    - remarks: 备注
    """

    url = "/mgmt/sys/updateHoliday"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
