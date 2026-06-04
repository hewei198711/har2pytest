import os

from util.client import client

data = {
    "advancedLearningJumpChannel": 0,  # 进阶学习跳转的小程序: 1.油葱学堂 2.油葱健康 3.荟有趣
    "advancedLearningJumpPath": "",  # 进阶学习跳转页面路径
    "beginnerLearningJumpChannel": 0,  # 初阶学习跳转的小程序: 1.油葱学堂 2.油葱健康 3.荟有趣
    "beginnerLearningJumpPath": "",  # 初阶学习跳转页面路径
    "bottomText": "",  # 底部文案
    "describe": "",  # 说明
    "linkEduCourseId": 0,  # 关联学堂课程的id
    "postUrl": "",  # 海报链接
    "topText": "",  # 顶部文案
    "updateType": 0,  # 修改类型: 1.修改海报链接 2.修改文案 3.修改关联内容
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_kos_updateKosSetting(data=data, headers=headers):
    """
    保存kos报名设置
    /mgmt/cms/kos/updateKosSetting

    参数说明:
    - advancedLearningJumpChannel: 进阶学习跳转的小程序: 1.油葱学堂 2.油葱健康 3.荟有趣
    - advancedLearningJumpPath: 进阶学习跳转页面路径
    - beginnerLearningJumpChannel: 初阶学习跳转的小程序: 1.油葱学堂 2.油葱健康 3.荟有趣
    - beginnerLearningJumpPath: 初阶学习跳转页面路径
    - bottomText: 底部文案
    - describe: 说明
    - linkEduCourseId: 关联学堂课程的id
    - postUrl: 海报链接
    - topText: 顶部文案
    - updateType: 修改类型: 1.修改海报链接 2.修改文案 3.修改关联内容
    """

    url = "/mgmt/cms/kos/updateKosSetting"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
