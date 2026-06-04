import os

from util.client import client

data = {
    "bizType": 0,  # 业务操作类型 1-下载  2-浏览， 3-点赞
    "downLoadType": 0,  # 下载类型1、形象手册管理 2、油葱微店运营与管理手册 3、服务中心运营与管理手册 4、优秀案例库
    "manualSectionId": 0,  # 形象手册小节ID
    "manualSectionTitle": "",  # 小节名称
    "storeCode": "",  # 服务中心编号。后台下载不需要送
    "title": "",  # 标题
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_manual_addDownloadRecord(data=data, headers=headers):
    """
    新增下载记录
    /mgmt/sys/manual/addDownloadRecord

    参数说明:
    - bizType: 业务操作类型 1-下载  2-浏览， 3-点赞
    - downLoadType: 下载类型1、形象手册管理 2、油葱微店运营与管理手册 3、服务中心运营与管理手册 4、优秀案例库
    - manualSectionId: 形象手册小节ID
    - manualSectionTitle: 小节名称
    - storeCode: 服务中心编号。后台下载不需要送
    - title: 标题
    """

    url = "/mgmt/sys/manual/addDownloadRecord"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
