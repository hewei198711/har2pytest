import os

from util.client import client

data = {
    "moduleList": [{"decorateId": 0, "sort": 0}],  # 模块列表
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_pcHomepageArrange_savePcHomepageArrange(data=data, headers=headers):
    """
    保存pc端首页排序
    /mgmt/cms/pcHomepageArrange/savePcHomepageArrange

    参数说明:
    - moduleList: 模块列表
    - moduleList.decorateId: 装饰id
    - moduleList.sort: 排序
    """

    url = "/mgmt/cms/pcHomepageArrange/savePcHomepageArrange"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
