import os

import allure
from allure_commons.types import Severity

from apis.mall_mgmt_application import (
    _mgmt_prmt_state_waitExamineCount,
)


@allure.severity(Severity.NORMAL)
@allure.feature("mall_mgmt_application")
@allure.story("/mgmt/prmt/state/waitExamineCount")
@allure.title("待审核状态数量")
def test_mgmt_prmt_state_waitExamineCount():

    headers = {
        "channel": "pc",
        "client": "op",
        "authorization": f"bearer {os.environ['access_token']}",
    }
    with _mgmt_prmt_state_waitExamineCount(headers=headers) as r:
        assert r.status_code == 200
        assert r.json()["code"] == 200

