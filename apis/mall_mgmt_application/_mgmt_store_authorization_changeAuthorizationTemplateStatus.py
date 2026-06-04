import os
from urllib.parse import urlencode

from util.client import client

data = {
    "id": 0,  # 主键ID
    "status": 0,  # 状态，0：已失效，1：生效中
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_store_authorization_changeAuthorizationTemplateStatus(data=data, headers=headers):
    """
    生效/失效授权书模板
    /mgmt/store/authorization/changeAuthorizationTemplateStatus

    参数说明:
    - id: 主键ID
    - status: 状态，0：已失效，1：生效中
    """

    url = "/mgmt/store/authorization/changeAuthorizationTemplateStatus"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
