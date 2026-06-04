import os

from util.client import client

data = {
    "bizType": 0,  # 操作行为类型 1-下载  2-浏览， 3-点赞
    "downloadAtEnd": 0,  # 下载结束时间(毫秒时间戳)
    "downloadAtEndAsLocalDateTime": "",  # TODO: 添加参数说明
    "downloadAtStart": 0,  # 下载开始时间(毫秒时间戳)
    "downloadAtStartAsLocalDateTime": "",  # TODO: 添加参数说明
    "downloadType": 0,  # 下载类型1、形象手册管理 2、油葱微店运营与管理手册 3、服务中心运营与管理手册 4、优秀案例库
    "manualSectionTitle": "",  # 小节名称
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
    "storeCode": "",  # 服务中心编号
    "userName": "",  # 用户名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_manual_listDownloadRecord(data=data, headers=headers):
    """
    分页查询下载记录
    /mgmt/sys/manual/listDownloadRecord

    参数说明:
    - bizType: 操作行为类型 1-下载  2-浏览， 3-点赞
    - downloadAtEnd: 下载结束时间(毫秒时间戳)
    - downloadAtStart: 下载开始时间(毫秒时间戳)
    - downloadType: 下载类型1、形象手册管理 2、油葱微店运营与管理手册 3、服务中心运营与管理手册 4、优秀案例库
    - manualSectionTitle: 小节名称
    - storeCode: 服务中心编号
    - userName: 用户名称
    """

    url = "/mgmt/sys/manual/listDownloadRecord"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
