import os

from util.client import client

data = {
    "endTime": "",  # 截止时间
    "materialName": "",  # 形象物料名称
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
    "serviceCenterCode": "",  # 服务中心编码
    "startTime": "",  # 开始时间
    "userName": "",  # 用户名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_material_downloadRecord_page(data=data, headers=headers):
    """
    后台管理-分页查询下载记录列表
    /mgmt/sys/material/downloadRecord/page

    参数说明:
    - endTime: 截止时间
    - materialName: 形象物料名称
    - serviceCenterCode: 服务中心编码
    - startTime: 开始时间
    - userName: 用户名称
    """

    url = "/mgmt/sys/material/downloadRecord/page"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
