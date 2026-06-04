import os

from util.client import client

data = {
    "switchOperate": 0,  # 商城自提方式隐藏开关操作: 0.隐藏，1.显示
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_pickUpSwitch_pickUpSwitchChange(data=data, headers=headers):
    """
    变更商城自提方式隐藏开关状态
    /mgmt/cms/pickUpSwitch/pickUpSwitchChange

    参数说明:
    - switchOperate: 商城自提方式隐藏开关操作: 0.隐藏，1.显示
    """

    url = "/mgmt/cms/pickUpSwitch/pickUpSwitchChange"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
