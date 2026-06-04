import os

from util.client import client

data = {
    "answerDate": "",  # 答题日期开始
    "answerDateEnd": "",  # 答题日期结束
    "answerTimeCount": 0,  # 答题时长
    "answerTimeUnit": 0,  # 答题时长时间单位: 1.秒 2.分 3.时
    "cardNo": "",  # 用户卡号
    "deviceChannel": 0,  # 登录端:1.APP 2.小程序 3.PC
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 每页页数
    "projectKey": "",  # 问卷key
    "timeRangeSymbol": 0,  # 答题时长时间范围符号:1.大于等于 2.小于等于 3.大于 4.小于
    "userName": "",  # 用户名
    "userType": 0,  # 顾客类型:1->普通顾客；2->优惠顾客；3->云商；4->微店（云+）
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_questionnaire_questionnaireStatisticsQuery(data=data, headers=headers):
    """
    问卷回收数据查询
    /mgmt/cms/questionnaire/questionnaireStatisticsQuery

    参数说明:
    - answerDate: 答题日期开始
    - answerDateEnd: 答题日期结束
    - answerTimeCount: 答题时长
    - answerTimeUnit: 答题时长时间单位: 1.秒 2.分 3.时
    - cardNo: 用户卡号
    - deviceChannel: 登录端:1.APP 2.小程序 3.PC
    - pageNum: 页码
    - pageSize: 每页页数
    - projectKey: 问卷key
    - timeRangeSymbol: 答题时长时间范围符号:1.大于等于 2.小于等于 3.大于 4.小于
    - userName: 用户名
    - userType: 顾客类型:1->普通顾客；2->优惠顾客；3->云商；4->微店（云+）
    """

    url = "/mgmt/cms/questionnaire/questionnaireStatisticsQuery"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
