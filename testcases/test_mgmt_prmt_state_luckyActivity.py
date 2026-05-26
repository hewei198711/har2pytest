import os

import allure
from allure_commons.types import Severity

from apis.mall_mgmt_application import (
    _mgmt_prmt_state_luckyActivity,
)


@allure.severity(Severity.NORMAL)
@allure.feature("mall_mgmt_application")
@allure.story("/mgmt/prmt/state/luckyActivity")
@allure.title("抽奖活动管理各状态数量")
def test_mgmt_prmt_state_luckyActivity():

    params = {
        "activityCode": "052202",
        "pageNum": "1",
        "pageSize": "10",
    }
    headers = {
        "channel": "pc",
        "client": "op",
        "authorization": f"bearer {os.environ['access_token']}",
    }
    with _mgmt_prmt_state_luckyActivity(params=params, headers=headers) as r:
        assert r.status_code == 200
        assert r.json()["code"] == 200


