import os

from util.client import client

data = {
    "cardNo": "",  # 会员卡号
    "displayUserSerial": "",  # 关联序列号
    "relateType": 0,  # 关联类型:1.素材;2.问卷;3.直播间;4.码上有名头像框;
    "userMobile": "",  # 会员手机号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_questionnaire_removeQuestionnaireDisplayUser(data=data, headers=headers):
    """
    删除问卷展示用户
    /mgmt/cms/questionnaire/removeQuestionnaireDisplayUser

    参数说明:
    - cardNo: 会员卡号
    - displayUserSerial: 关联序列号
    - relateType: 关联类型:1.素材;2.问卷;3.直播间;4.码上有名头像框;
    - userMobile: 会员手机号
    """

    url = "/mgmt/cms/questionnaire/removeQuestionnaireDisplayUser"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
