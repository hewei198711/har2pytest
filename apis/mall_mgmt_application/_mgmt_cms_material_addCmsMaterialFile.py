import os

from util.client import client

data = {
    "allowNoLogin": 0,  # 未登录顾客查看权限 1.是 0.否
    "author": "",  # 作者名称
    "cmsClassificationLabelIds": "",  # 分类标签ID,多个ID以逗号隔开,例：1,2,3
    "cmsMaterialFileBaseReqVOS": [{"fileName": "", "fileSize": "", "fileUrl": ""}],  # 文件集合
    "cmsTypeLabelId": 0,  # 类型标签ID
    "commentArticle": "",  # 朋友圈评论文案
    "content": "",  # 图文内容
    "coverUrl": [{"url": ""}],  # 封面图地址
    "coverUrlType": 0,  # 封面图类型: 1.上文下图(单图) 2.上文下图(三图) 3.左文右图(单图) 4.视频
    "displayObjects": "",  # 按顾客身份查看 1:会员; 2:vip会员; 3:云商; 4:微店;(多选使用逗号分隔)
    "displayType": 0,  # 素材查看类型 1:按顾客身份查看; 2:按用户展示名单
    "displayUserSerial": "",  # 素材展示用户关联序列号
    "fileType": 0,  # 素材文件类型:1.上传文件; 2.关联链接; 3.图文;
    "linkUrl": "",  # 关联链接
    "materialNo": "",  # 编号
    "name": "",  # 自定义名称
    "productId": 0,  # 商品id
    "productList": [{"serialNo": "", "sort": 0}],  # 关联产品编码列表
    "remarks": "",  # 说明
    "secondaryClassificationId": 0,  # 二级分类id
    "shareArticle": "",  # 分享文案
    "shelfConfig": 0,  # 上下架配置,1:立即启用; 2:定时启用;3:定时启用禁用; 4:立即禁用
    "shelfOffTime": "",  # 素材禁用时间
    "shelfUpTime": "",  # 素材启用时间
    "sort": 0,  # 排序
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_material_addCmsMaterialFile(data=data, headers=headers):
    """
    添加素材-文件
    /mgmt/cms/material/addCmsMaterialFile

    参数说明:
    - allowNoLogin: 未登录顾客查看权限 1.是 0.否
    - author: 作者名称
    - cmsClassificationLabelIds: 分类标签ID,多个ID以逗号隔开,例：1,2,3
    - cmsMaterialFileBaseReqVOS: 文件集合
    - cmsMaterialFileBaseReqVOS.fileName: 文件名称
    - cmsMaterialFileBaseReqVOS.fileSize: 文件大小 例：200kb
    - cmsMaterialFileBaseReqVOS.fileUrl: 文件地址
    - cmsTypeLabelId: 类型标签ID
    - commentArticle: 朋友圈评论文案
    - content: 图文内容
    - coverUrl: 封面图地址
    - coverUrl.url: 封面图地址
    - coverUrlType: 封面图类型: 1.上文下图(单图) 2.上文下图(三图) 3.左文右图(单图) 4.视频
    - displayObjects: 按顾客身份查看 1:会员; 2:vip会员; 3:云商; 4:微店;(多选使用逗号分隔)
    - displayType: 素材查看类型 1:按顾客身份查看; 2:按用户展示名单
    - displayUserSerial: 素材展示用户关联序列号
    - fileType: 素材文件类型:1.上传文件; 2.关联链接; 3.图文;
    - linkUrl: 关联链接
    - materialNo: 编号
    - name: 自定义名称
    - productId: 商品id
    - productList: 关联产品编码列表
    - productList.serialNo: 产品编码
    - productList.sort: sort
    - remarks: 说明
    - secondaryClassificationId: 二级分类id
    - shareArticle: 分享文案
    - shelfConfig: 上下架配置,1:立即启用; 2:定时启用;3:定时启用禁用; 4:立即禁用
    - shelfOffTime: 素材禁用时间
    - shelfUpTime: 素材启用时间
    - sort: 排序
    """

    url = "/mgmt/cms/material/addCmsMaterialFile"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
