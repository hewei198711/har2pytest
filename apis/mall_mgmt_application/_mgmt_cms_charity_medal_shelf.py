import os

from util.client import client

data = {
    "id": 0,  # id
    "shelfOperate": 0,  # 上下架操作: 1:上架(发布); 2:下架;
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_charity_medal_shelf(data=data, headers=headers):
    """
    上架/下架公益购勋章
    /mgmt/cms/charity/medal/shelf

    参数说明:
    - id: id
    - shelfOperate: 上下架操作: 1:上架(发布); 2:下架;
    """

    url = "/mgmt/cms/charity/medal/shelf"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
