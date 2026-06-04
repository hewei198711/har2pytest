import os

from util.client import client

params = {
    "infoId": 0,  # infoId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_perfectInfo_editInfoSetting_infoId(params=params, headers=headers):
    """
    修改完美资讯信息
    /mgmt/cms/perfectInfo/editInfoSetting/{infoId}

    参数说明:
    - infoId: infoId
    - enableStatus: 启用状态: 0.禁用 1.启用
    - imgUrl: 资讯图片链接
    - infoName: 资讯名称
    - linkUrl: 关联链接
    - sort: 排序
    """

    url = f"/mgmt/cms/perfectInfo/editInfoSetting/{params['infoId']}"
    with client.get(url=url, headers=headers) as r:
        return r
