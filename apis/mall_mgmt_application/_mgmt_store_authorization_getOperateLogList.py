import os

from util.client import client

params = {
    "endOperateTime": "",  # 操作结束时间
    "operateSourceChannel": 0,  # 操作来源渠道，1：后台，2：店铺
    "pageNum": 0,  # pageNum
    "pageSize": 0,  # pageSize
    "startOperateTime": "",  # 操作开始时间
    "storeCode": "",  # 服务中心编号（店铺端必传）
    "type": 0,  # 类型，1：授权书操作记录，2：授权书下载记录，3：授权书模板操作记录
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_authorization_getOperateLogList(params=params, headers=headers):
    """
    获取授权书操作日志列表
    /mgmt/store/authorization/getOperateLogList

    参数说明:
    - endOperateTime: 操作结束时间
    - operateSourceChannel: 操作来源渠道，1：后台，2：店铺
    - pageNum: pageNum
    - pageSize: pageSize
    - startOperateTime: 操作开始时间
    - storeCode: 服务中心编号（店铺端必传）
    - type: 类型，1：授权书操作记录，2：授权书下载记录，3：授权书模板操作记录
    """

    url = "/mgmt/store/authorization/getOperateLogList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
