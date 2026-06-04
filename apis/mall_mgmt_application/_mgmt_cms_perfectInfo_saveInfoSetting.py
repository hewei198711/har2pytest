import os

from util.client import client

data = {
    "enableStatus": 0,  # 启用状态: 0.禁用 1.启用
    "imgUrl": "",  # 资讯图片链接
    "infoName": "",  # 资讯名称
    "linkUrl": "",  # 关联链接
    "sort": 0,  # 排序
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_perfectInfo_saveInfoSetting(data=data, headers=headers):
    """
    保存完美资讯信息
    /mgmt/cms/perfectInfo/saveInfoSetting

    参数说明:
    - enableStatus: 启用状态: 0.禁用 1.启用
    - imgUrl: 资讯图片链接
    - infoName: 资讯名称
    - linkUrl: 关联链接
    - sort: 排序
    """

    url = "/mgmt/cms/perfectInfo/saveInfoSetting"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
