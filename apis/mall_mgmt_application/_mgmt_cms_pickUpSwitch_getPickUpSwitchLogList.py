import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_pickUpSwitch_getPickUpSwitchLogList(headers=headers):
    """
    获取商城自提方式隐藏开关状态变更日志列表
    /mgmt/cms/pickUpSwitch/getPickUpSwitchLogList
    """

    url = "/mgmt/cms/pickUpSwitch/getPickUpSwitchLogList"
    with client.get(url=url, headers=headers) as r:
        return r
