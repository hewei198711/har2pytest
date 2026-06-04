import os

from util.client import client

data = {
    "author": "",  # 作者名称
    "cmsClassificationLabelIds": "",  # 分类标签ID,多个ID以逗号隔开,例：1,2,3
    "cmsMaterialDocBaseReqVOS": [{"context": "", "directoryName": ""}],  # 内容集合
    "cmsTypeLabelId": 0,  # 类型标签ID
    "coverUrl": [{"url": ""}],  # 封面图地址
    "coverUrlType": 0,  # 封面图类型: 1.上文下图(单图) 2.上文下图(三图) 3.左文右图(单图) 4.视频
    "id": 0,  # 主键ID
    "materialNo": "",  # 编号
    "name": "",  # 自定义名称
    "productId": 0,  # 商品id
    "remarks": "",  # 说明
    "shelfConfig": 0,  # 上下架配置,1:立即启用; 2:定时启用;3:定时启用禁用; 4:立即禁用
    "shelfOffTime": "",  # 素材禁用时间
    "shelfUpTime": "",  # 素材启用时间
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_material_updateCmsMaterialDoc(data=data, headers=headers):
    """
    修改素材-文档
    /mgmt/cms/material/updateCmsMaterialDoc

    参数说明:
    - author: 作者名称
    - cmsClassificationLabelIds: 分类标签ID,多个ID以逗号隔开,例：1,2,3
    - cmsMaterialDocBaseReqVOS: 内容集合
    - cmsMaterialDocBaseReqVOS.context: 文档内容
    - cmsMaterialDocBaseReqVOS.directoryName: 目录名称
    - cmsTypeLabelId: 类型标签ID
    - coverUrl: 封面图地址
    - coverUrl.url: 封面图地址
    - coverUrlType: 封面图类型: 1.上文下图(单图) 2.上文下图(三图) 3.左文右图(单图) 4.视频
    - id: 主键ID
    - materialNo: 编号
    - name: 自定义名称
    - productId: 商品id
    - remarks: 说明
    - shelfConfig: 上下架配置,1:立即启用; 2:定时启用;3:定时启用禁用; 4:立即禁用
    - shelfOffTime: 素材禁用时间
    - shelfUpTime: 素材启用时间
    """

    url = "/mgmt/cms/material/updateCmsMaterialDoc"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
