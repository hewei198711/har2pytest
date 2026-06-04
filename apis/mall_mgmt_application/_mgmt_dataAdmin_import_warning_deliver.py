import os
from urllib.parse import urlencode

from util.client import client

data = {
    "ruleId": 0,  # ruleId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_dataAdmin_import_warning_deliver(data=data, headers=headers):
    """
    数据中心管理后台-导入文件-重点交付预警名单
    /mgmt/dataAdmin/import/warning/deliver

    参数说明:
    - ruleId: ruleId
    """

    url = "/mgmt/dataAdmin/import/warning/deliver"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
