import os

from util.client import client

data = {
    "createTimeMin": "2026-05-19 00:00:00",  # 创建时间始 yyyy-MM-dd HH:mm:ss
    "createTimeMax": "2026-05-19 23:59:59",  # 创建时间末 yyyy-MM-dd HH:mm:ss
    "pictureCode": None,  # 图片编码
    "pictureName": None,  # 图片名称
    "pageNum": 1,  # 当前页
    "pageSize": 10,  # 每页数量
}

headers = {
    "channel": "pc",
    "client": "op",
    "content-type": "application/json;charset=UTF-8",
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_prmt_luckyActivity_luckyBoxPicturePage(data=data, headers=headers):
    """
    条件分页查询盲盒海报图片列表
    /mgmt/prmt/luckyActivity/luckyBoxPicturePage

    参数说明:
    - createTimeMax: 创建时间末 yyyy-MM-dd HH:mm:ss
    - createTimeMin: 创建时间始 yyyy-MM-dd HH:mm:ss
    - pageNum: 当前页
    - pageSize: 每页数量
    - pictureCode: 图片编码
    - pictureName: 图片名称
    """

    url = "/mgmt/prmt/luckyActivity/luckyBoxPicturePage"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
