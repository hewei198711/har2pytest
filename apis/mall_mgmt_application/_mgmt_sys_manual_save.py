import os

from util.client import client

data = {
    "chapters": [
        {
            "id": 0,
            "manualId": 0,
            "sections": [
                {"chapterId": 0, "fileUrl": "", "fileUrlName": "", "iconUrl": "", "id": 0, "sortOrder": 0, "title": ""}
            ],
            "sortOrder": 0,
            "title": "",
        }
    ],  # 章节列表
    "coverUrl": "",  # 封面地址
    "id": 0,  # 主键ID
    "isDownload": False,  # 下载按钮展示(优秀案例库时需传) 0 -不展示  1-展示
    "isLike": False,  # 点赞按钮显示(优秀案例库时需传) 0 - 不显示， 1-显示
    "isPublish": False,  # 是否立即上架，0=否，1=是
    "targetServiceCenter": False,  # 使用对象-服务中心：0-未选中，1-选中
    "targetStore": False,  # 使用对象-微店：0-未选中，1-选中
    "title": "",  # 形象手册标题
    "type": 0,  # 1、形象手册管理 2、油葱微店运营与管理手册 3、服务中心运营与管理手册 4、优秀案例库
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_manual_save(data=data, headers=headers):
    """
    保存形象手册信息
    /mgmt/sys/manual/save

    参数说明:
    - chapters: 章节列表
    - chapters.id: 主键ID
    - chapters.manualId: 形象手册ID
    - chapters.sections: 小节列表
    - chapters.sections.chapterId: 所属章节ID
    - chapters.sections.fileUrl: 小节文件URL，仅支持pdf
    - chapters.sections.fileUrlName: 小节文件名称
    - chapters.sections.iconUrl: 小节icon地址
    - chapters.sections.id: 主键ID
    - chapters.sections.sortOrder: 排序
    - chapters.sections.title: 小节名称
    - chapters.sortOrder: 排序
    - chapters.title: 章节名称
    - coverUrl: 封面地址
    - id: 主键ID
    - isDownload: 下载按钮展示(优秀案例库时需传) 0 -不展示  1-展示
    - isLike: 点赞按钮显示(优秀案例库时需传) 0 - 不显示， 1-显示
    - isPublish: 是否立即上架，0=否，1=是
    - targetServiceCenter: 使用对象-服务中心：0-未选中，1-选中
    - targetStore: 使用对象-微店：0-未选中，1-选中
    - title: 形象手册标题
    - type: 1、形象手册管理 2、油葱微店运营与管理手册 3、服务中心运营与管理手册 4、优秀案例库
    """

    url = "/mgmt/sys/manual/save"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
