import os

from util.client import client

params = {
    "downloadType": "",  # 下载途径，1：运营后台，2：门店系统
    "endOperateTime": "",  # 下载结束时间
    "operateSourceChannel": 0,  # 操作来源渠道，1：后台，2：店铺
    "pageNum": 0,  # pageNum
    "pageSize": 0,  # pageSize
    "startOperateTime": "",  # 下载开始时间
    "storeCode": "",  # 服务中心编号
    "templateName": "",  # 授权书模板名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_authorization_getDownLoadLogList(params=params, headers=headers):
    """
    获取授权书下载日志列表
    /mgmt/store/authorization/getDownLoadLogList

    参数说明:
    - downloadType: 下载途径，1：运营后台，2：门店系统
    - endOperateTime: 下载结束时间
    - operateSourceChannel: 操作来源渠道，1：后台，2：店铺
    - pageNum: pageNum
    - pageSize: pageSize
    - startOperateTime: 下载开始时间
    - storeCode: 服务中心编号
    - templateName: 授权书模板名称
    """

    url = "/mgmt/store/authorization/getDownLoadLogList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
