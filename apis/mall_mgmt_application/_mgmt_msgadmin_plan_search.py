import os

from util.client import client

data = {
    "endTime": "",  # 查询结束时间
    "pageNum": 0,  # 请求页码
    "pageSize": 0,  # 页的数量
    "platformId": 0,  # 接收者类型  0 未指定 1服务中心 2商城
    "sceneId": 0,  # 场景id
    "sceneTitle": "",  # 场景标题
    "startTime": "",  # 查询开始时间
    "status": "",  # 状态
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_msgadmin_plan_search(data=data, headers=headers):
    """
    页面子场景查询相关（系统消息）接口
    /mgmt/msgadmin/plan/search

    参数说明:
    - endTime: 查询结束时间
    - pageNum: 请求页码
    - pageSize: 页的数量
    - platformId: 接收者类型  0 未指定 1服务中心 2商城
    - sceneId: 场景id
    - sceneTitle: 场景标题
    - startTime: 查询开始时间
    - status: 状态
    """

    url = "/mgmt/msgadmin/plan/search"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
