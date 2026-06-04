import os

from util.client import client

params = {
    "honorType": "",  # 荣誉类型:1.用户荣誉  2.用户等级隐藏
    "importType": "",  # 导入类型:1.导入新增  2.导入删除
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_honor_exportUserHonorImportFailList(params=params, headers=headers):
    """
    导出用户荣誉导入失败原因列表
    /mgmt/cms/honor/exportUserHonorImportFailList

    参数说明:
    - honorType: 荣誉类型:1.用户荣誉  2.用户等级隐藏
    - importType: 导入类型:1.导入新增  2.导入删除
    """

    url = "/mgmt/cms/honor/exportUserHonorImportFailList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
