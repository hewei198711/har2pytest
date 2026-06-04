import os

from util.client import client

data = {
    "fileFormat": "",  # 文件格式
    "materialName": "",  # 物料名称
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
    "status": 0,  # 状态(0:禁用 1:启用)
    "storeType": 0,  # 使用对象类型(0-服务中心+微店，1-服务中心，2-微店，3-指定店铺(自定义导入))
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_material_admin_page(data=data, headers=headers):
    """
    后台管理-分页查询形象物料列表
    /mgmt/sys/material/admin/page

    参数说明:
    - fileFormat: 文件格式
    - materialName: 物料名称
    - status: 状态(0:禁用 1:启用)
    - storeType: 使用对象类型(0-服务中心+微店，1-服务中心，2-微店，3-指定店铺(自定义导入))
    """

    url = "/mgmt/sys/material/admin/page"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
