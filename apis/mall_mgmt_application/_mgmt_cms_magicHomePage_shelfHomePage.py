import os

from util.client import client

data = {
    "displayTarget": "",  # 发布展示对象: 1:会员; 2:VIP会员; 3:云商; 4:微店; 7:游客(多选使用逗号分隔)
    "id": 0,  # id
    "shelfConfig": 0,  # 上下架配置: 1:立即发布; 2:定时发布; 3:定时上下架
    "shelfOffTime": "",  # 定时下架时间
    "shelfOperate": 0,  # 上下架操作: 1:上架(发布); 2:下架;
    "shelfUpTime": "",  # 定时发布时间
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_magicHomePage_shelfHomePage(data=data, headers=headers):
    """
    发布/下架魔法首页
    /mgmt/cms/magicHomePage/shelfHomePage

    参数说明:
    - displayTarget: 发布展示对象: 1:会员; 2:VIP会员; 3:云商; 4:微店; 7:游客(多选使用逗号分隔)
    - id: id
    - shelfConfig: 上下架配置: 1:立即发布; 2:定时发布; 3:定时上下架
    - shelfOffTime: 定时下架时间
    - shelfOperate: 上下架操作: 1:上架(发布); 2:下架;
    - shelfUpTime: 定时发布时间
    """

    url = "/mgmt/cms/magicHomePage/shelfHomePage"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
