import os

from util.client import client

data = {
    "childList": [{"linkName": "", "linkUrl": ""}],  # 子链接
    "id": 0,  # id
    "name": "",  # 父链接名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_friendship_saveMultiFriendLink(data=data, headers=headers):
    """
    保存编辑多个友情链接
    /mgmt/cms/friendship/saveMultiFriendLink

    参数说明:
    - childList: 子链接
    - childList.linkName: 友情链接名称
    - childList.linkUrl: 友情链接地址
    - id: id
    - name: 父链接名称
    """

    url = "/mgmt/cms/friendship/saveMultiFriendLink"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
