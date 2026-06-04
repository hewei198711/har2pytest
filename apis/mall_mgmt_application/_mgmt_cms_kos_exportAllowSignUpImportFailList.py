import os

from util.client import client

params = {
    "importResultKey": "",  # 导入结果key
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_kos_exportAllowSignUpImportFailList(params=params, headers=headers):
    """
    导出可报名人员导入失败原因列表
    /mgmt/cms/kos/exportAllowSignUpImportFailList

    参数说明:
    - importResultKey: 导入结果key
    """

    url = "/mgmt/cms/kos/exportAllowSignUpImportFailList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
