import os

from util.client import client

params = {
    "downloader": "",  # 用户名
    "endTime": "",  # 结束时间
    "manualName": "",  # 形象手册名称
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "startTime": "",  # 开始时间
    "storeCode": "",  # 服务中心编码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_image_record_page(params=params, headers=headers):
    """
    查询形象手册列表下载记录
    /mgmt/sys/image/record/page

    参数说明:
    - downloader: 用户名
    - endTime: 结束时间
    - manualName: 形象手册名称
    - pageNum: 页数
    - pageSize: 页大小
    - startTime: 开始时间
    - storeCode: 服务中心编码
    """

    url = "/mgmt/sys/image/record/page"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
