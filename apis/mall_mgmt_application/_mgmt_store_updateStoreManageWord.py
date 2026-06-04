import os

from util.client import client

data = {
    "homeEndTime": "",  # 首页提示语结束时间，dd HH:mm
    "homeLongTime": 0,  # 首页提示语时间：1-长期，2-不是长期
    "homeStartTime": "",  # 首页提示语开始时间，dd HH:mm
    "homeWord": "",  # 首页提示语
    "manageEndTime": "",  # 押货保证金管理页提示语结束时间，dd HH:mm
    "manageLongTime": 0,  # 押货保证金管理页提示语时间：1-长期，2-不是长期
    "manageStartTime": "",  # 押货保证金管理页提示语开始时间，dd HH:mm
    "manageWord": "",  # 押货保证金管理页提示语
    "open": 0,  # 是否开启提示：1-开启，2-关闭
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_updateStoreManageWord(data=data, headers=headers):
    """
    更新服务中心提示语
    /mgmt/store/updateStoreManageWord

    参数说明:
    - homeEndTime: 首页提示语结束时间，dd HH:mm
    - homeLongTime: 首页提示语时间：1-长期，2-不是长期
    - homeStartTime: 首页提示语开始时间，dd HH:mm
    - homeWord: 首页提示语
    - manageEndTime: 押货保证金管理页提示语结束时间，dd HH:mm
    - manageLongTime: 押货保证金管理页提示语时间：1-长期，2-不是长期
    - manageStartTime: 押货保证金管理页提示语开始时间，dd HH:mm
    - manageWord: 押货保证金管理页提示语
    - open: 是否开启提示：1-开启，2-关闭
    """

    url = "/mgmt/store/updateStoreManageWord"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
