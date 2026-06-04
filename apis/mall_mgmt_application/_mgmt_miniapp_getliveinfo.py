import os

from util.client import client

data = {
    "end_time": "",  # 直播计划结束时间
    "from": 0,  # TODO: 添加参数说明
    "live_status": 0,  # 直播间状态。101：直播中，102：未开始，103已结束，104禁播，105：暂停，106：异常，107：已过期
    "name": "",  # 直播标题
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "start_time": "",  # 直播计划开始时间
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_miniapp_getliveinfo(data=data, headers=headers):
    """
    获取直播间数据列表
    /mgmt/miniapp/getliveinfo

    参数说明:
    - end_time: 直播计划结束时间
    - live_status: 直播间状态。101：直播中，102：未开始，103已结束，104禁播，105：暂停，106：异常，107：已过期
    - name: 直播标题
    - pageNum: 页数
    - pageSize: 每页显示数
    - start_time: 直播计划开始时间
    """

    url = "/mgmt/miniapp/getliveinfo"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
