import os

from util.client import client

params = {
    "shareContentId": 0,  # shareContentId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_dkxp_shareContent_editContent_shareContentId(params=params, headers=headers):
    """
    编辑分享文案
    /mgmt/cms/dkxp/shareContent/editContent/{shareContentId}

    参数说明:
    - category: 内容分类，1：分享好友内容配置，2：保存图像内容配置
    - content: 内容文案
    - shareContentId: shareContentId
    """

    url = f"/mgmt/cms/dkxp/shareContent/editContent/{params['shareContentId']}"
    with client.get(url=url, headers=headers) as r:
        return r
