import os

from util.client import client

params = {
    "popUpId": 0,  # popUpId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_editPopUpSetting_popUpId(params=params, headers=headers):
    """
    更新指定id的弹窗配置信息
    /mgmt/cms/editPopUpSetting/{popUpId}

    参数说明:
    - popUpId: popUpId
    - disableTime: 定时禁用时间
    - enableConfig: 上下架配置: 1.立即启用; 2.定时禁用启用
    - enableTime: 定时启用时间
    - location: 显示位置(可多选): 1.APP; 2.小程序;(多选使用逗号分隔)
    - popUpContent: 弹窗内容
    - popUpTitle: 弹窗标题
    - popUpType: 弹窗类型: 1:系统升级提醒
    - sort: 排序
    """

    url = f"/mgmt/cms/editPopUpSetting/{params['popUpId']}"
    with client.get(url=url, headers=headers) as r:
        return r
