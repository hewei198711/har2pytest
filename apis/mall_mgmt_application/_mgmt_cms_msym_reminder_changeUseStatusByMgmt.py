import os

from util.client import client

data = {
    "enable": 0,  # 是否启用, 0:禁用; 1:启用
    "id": 0,  # id
    "remark": "",  # 备注
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_msym_reminder_changeUseStatusByMgmt(data=data, headers=headers):
    """
    运营后台启用禁用店铺温馨语
    /mgmt/cms/msym/reminder/changeUseStatusByMgmt

    参数说明:
    - enable: 是否启用, 0:禁用; 1:启用
    - id: id
    - remark: 备注
    """

    url = "/mgmt/cms/msym/reminder/changeUseStatusByMgmt"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
