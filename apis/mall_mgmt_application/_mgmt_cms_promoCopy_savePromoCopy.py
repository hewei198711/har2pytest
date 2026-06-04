import os

from util.client import client

data = {
    "copyText": "",  # 词条文案
    "id": 0,  # id(编辑时必填)
    "serialNoList": [],  # 商品编码列表
    "shelfConfig": 0,  # 上下架配置: 1.立即启用; 2.定时启用; 3.定时启用禁用; 4.立即禁用
    "shelfOffTime": "",  # 禁用时间
    "shelfUpTime": "",  # 启用时间
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_promoCopy_savePromoCopy(data=data, headers=headers):
    """
    促单词条新增接口
    /mgmt/cms/promoCopy/savePromoCopy

    参数说明:
    - copyText: 词条文案
    - id: id(编辑时必填)
    - serialNoList: 商品编码列表
    - shelfConfig: 上下架配置: 1.立即启用; 2.定时启用; 3.定时启用禁用; 4.立即禁用
    - shelfOffTime: 禁用时间
    - shelfUpTime: 启用时间
    """

    url = "/mgmt/cms/promoCopy/savePromoCopy"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
