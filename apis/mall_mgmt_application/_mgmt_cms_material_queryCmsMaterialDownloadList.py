import os

from util.client import client

data = {
    "channel": 0,  # 渠道 1：H5 2：app 3：小程序 4 pc
    "cmsMaterialId": 0,  # 素材id
    "download": "",  # 下载人
    "endTime": 0,  # 结束时间时间戳
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 每页页数
    "startTime": 0,  # 开始时间时间戳
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_material_queryCmsMaterialDownloadList(data=data, headers=headers):
    """
    查询下载列表
    /mgmt/cms/material/queryCmsMaterialDownloadList

    参数说明:
    - channel: 渠道 1：H5 2：app 3：小程序 4 pc
    - cmsMaterialId: 素材id
    - download: 下载人
    - endTime: 结束时间时间戳
    - pageNum: 页码
    - pageSize: 每页页数
    - startTime: 开始时间时间戳
    """

    url = "/mgmt/cms/material/queryCmsMaterialDownloadList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
