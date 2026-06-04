import os

from util.client import client

params = {
    "answerDate": "",  # 答题日期开始
    "answerDateEnd": "",  # 答题日期结束
    "answerTimeCount": "",  # 答题时长
    "answerTimeUnit": "",  # 答题时长时间单位: 1.秒 2.分 3.时
    "cardNo": "",  # 用户卡号
    "deviceChannel": "",  # 登录端:1.APP 2.小程序 3.PC
    "projectKey": "",  # 问卷key
    "timeRangeSymbol": "",  # 答题时长时间范围符号:1.大于等于 2.小于等于 3.大于 4.小于
    "userName": "",  # 用户名
    "userType": "",  # 顾客类型:1->会员；2->VIP会员；3->云商；4->微店（云+）
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_questionnaire_exportQuestionnaireStatistics(params=params, headers=headers):
    """
    问卷回收数据导出
    /mgmt/cms/questionnaire/exportQuestionnaireStatistics

    参数说明:
    - answerDate: 答题日期开始
    - answerDateEnd: 答题日期结束
    - answerTimeCount: 答题时长
    - answerTimeUnit: 答题时长时间单位: 1.秒 2.分 3.时
    - cardNo: 用户卡号
    - deviceChannel: 登录端:1.APP 2.小程序 3.PC
    - projectKey: 问卷key
    - timeRangeSymbol: 答题时长时间范围符号:1.大于等于 2.小于等于 3.大于 4.小于
    - userName: 用户名
    - userType: 顾客类型:1->会员；2->VIP会员；3->云商；4->微店（云+）
    """

    url = "/mgmt/cms/questionnaire/exportQuestionnaireStatistics"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
