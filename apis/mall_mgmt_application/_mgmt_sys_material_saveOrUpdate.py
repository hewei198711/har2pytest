import os

from util.client import client

data = {
    "fileFormat": "",  # 文件格式
    "fileName": "",  # 文件名称
    "filePath": "",  # 文件路径
    "id": 0,  # 主键ID
    "materialName": "",  # 物料名称
    "status": 0,  # 状态(0:禁用 1:启用)
    "storeList": [],  # 指定店铺列表(当storeType=3时必填)
    "storeType": 0,  # 店铺类型(0:服务中心+微店 1:服务中心 2:微店 3:指定店铺)
    "useObjectType": 0,  # 使用对象类型(1:自定义类型 2:自定义导入)
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_material_saveOrUpdate(data=data, headers=headers):
    """
    新增/更新形象物料，更新需送id
    /mgmt/sys/material/saveOrUpdate

    参数说明:
    - fileFormat: 文件格式
    - fileName: 文件名称
    - filePath: 文件路径
    - id: 主键ID
    - materialName: 物料名称
    - status: 状态(0:禁用 1:启用)
    - storeList: 指定店铺列表(当storeType=3时必填)
    - storeType: 店铺类型(0:服务中心+微店 1:服务中心 2:微店 3:指定店铺)
    - useObjectType: 使用对象类型(1:自定义类型 2:自定义导入)
    """

    url = "/mgmt/sys/material/saveOrUpdate"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
