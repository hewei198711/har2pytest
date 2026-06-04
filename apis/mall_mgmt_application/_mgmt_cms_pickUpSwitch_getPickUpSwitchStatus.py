import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_pickUpSwitch_getPickUpSwitchStatus(headers=headers):
    """
    获取商城自提方式隐藏开关状态
    /mgmt/cms/pickUpSwitch/getPickUpSwitchStatus
    """

    url = "/mgmt/cms/pickUpSwitch/getPickUpSwitchStatus"
    with client.get(url=url, headers=headers) as r:
        return r
