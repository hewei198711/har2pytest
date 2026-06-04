import os

from util.client import client

data = {
    "cmsClassificationLabelIds": "",  # 分类标签ID,多个ID以逗号隔开,例：1,2,3
    "cmsTypeLabelId": 0,  # 类型标签ID
    "endTime": 0,  # 结束时间时间戳
    "materialNo": "",  # 编号
    "name": "",  # 自定义名称
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 每页页数
    "secondaryClassificationId": 0,  # 二级分类ID
    "startTime": 0,  # 开始时间时间戳
    "status": 0,  # 状态 1：启用（默认）0：禁用
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_material_queryCmsMaterialFileList(data=data, headers=headers):
    """
    素材列表查询（统计下载量）
    /mgmt/cms/material/queryCmsMaterialFileList

    参数说明:
    - cmsClassificationLabelIds: 分类标签ID,多个ID以逗号隔开,例：1,2,3
    - cmsTypeLabelId: 类型标签ID
    - endTime: 结束时间时间戳
    - materialNo: 编号
    - name: 自定义名称
    - pageNum: 页码
    - pageSize: 每页页数
    - secondaryClassificationId: 二级分类ID
    - startTime: 开始时间时间戳
    - status: 状态 1：启用（默认）0：禁用
    """

    url = "/mgmt/cms/material/queryCmsMaterialFileList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
