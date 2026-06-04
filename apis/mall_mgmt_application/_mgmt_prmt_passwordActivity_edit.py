import os

from util.client import client

data = {
    "answer": False,  # 是否开启正确答案 false-否 true-是
    "answerContentList": [],  # 答案集合
    "bgPicUrl": "",  # 背景图片
    "endTime": "",  # 活动结束时间 (null不限)
    "id": 0,  # 主键
    "inputFrontColor": "",  # 输入框字体颜色
    "inputFrontSize": "",  # 输入框字体大小
    "menuTip": "",  # 按钮文案
    "position": {
        "answerInputX": "",
        "answerInputY": "",
        "submitButtonX": "",
        "submitButtonY": "",
    },  # 答案框/提交按钮位置
    "promotionCode": "",  # 活动编号
    "promotionName": "",  # 活动名称
    "promotionState": 0,  # 活动状态:活动状态:1-待审核,2-待开始,3-进行中,4-已结束,5-已驳回(待修改),6-草稿,7-已失效
    "rule": "",  # 活动规则
    "startTime": "",  # 活动开始时间
    "wechatGuide": False,  # 是否开启企微相关引导 false-否 true-是
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_passwordActivity_edit(data=data, headers=headers):
    """
    编辑口令活动
    /mgmt/prmt/passwordActivity/edit

    参数说明:
    - answer: 是否开启正确答案 false-否 true-是
    - answerContentList: 答案集合
    - bgPicUrl: 背景图片
    - endTime: 活动结束时间 (null不限)
    - id: 主键
    - inputFrontColor: 输入框字体颜色
    - inputFrontSize: 输入框字体大小
    - menuTip: 按钮文案
    - position: 答案框/提交按钮位置
    - position.answerInputX: 答案输入框X轴位置
    - position.answerInputY: 答案输入框Y轴位置
    - position.submitButtonX: 提交按钮X轴位置
    - position.submitButtonY: 提交按钮Y轴位置
    - promotionCode: 活动编号
    - promotionName: 活动名称
    - promotionState: 活动状态:活动状态:1-待审核,2-待开始,3-进行中,4-已结束,5-已驳回(待修改),6-草稿,7-已失效
    - rule: 活动规则
    - startTime: 活动开始时间
    - wechatGuide: 是否开启企微相关引导 false-否 true-是
    """

    url = "/mgmt/prmt/passwordActivity/edit"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
