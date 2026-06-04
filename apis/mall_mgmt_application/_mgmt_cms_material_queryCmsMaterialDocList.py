import os

from util.client import client

data = {
    "endTime": 0,  # 结束时间时间戳
    "materialNo": "",  # 编号
    "name": "",  # 自定义名称
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 每页页数
    "startTime": 0,  # 开始时间时间戳
    "status": 0,  # 状态 1：启用（默认）0：禁用
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_material_queryCmsMaterialDocList(data=data, headers=headers):
    """
    文档列表查询
    /mgmt/cms/material/queryCmsMaterialDocList

    参数说明:
    - endTime: 结束时间时间戳
    - materialNo: 编号
    - name: 自定义名称
    - pageNum: 页码
    - pageSize: 每页页数
    - startTime: 开始时间时间戳
    - status: 状态 1：启用（默认）0：禁用
    """

    url = "/mgmt/cms/material/queryCmsMaterialDocList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
