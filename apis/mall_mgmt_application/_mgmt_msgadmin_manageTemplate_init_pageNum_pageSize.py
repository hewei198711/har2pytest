import os

from util.client import client

params = {
    "pageNum": 0,  # pageNum
    "pageSize": 0,  # pageSize
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_msgadmin_manageTemplate_init_pageNum_pageSize(params=params, headers=headers):
    """
    获取一个站内信模板内容
    /mgmt/msgadmin/manageTemplate/init/{pageNum}/{pageSize}

    参数说明:
    - pageNum: pageNum
    - pageSize: pageSize
    """

    url = f"/mgmt/msgadmin/manageTemplate/init/{params['pageNum']}/{params['pageSize']}"
    with client.get(url=url, headers=headers) as r:
        return r
