import pytest

if __name__ == "__main__":
    # 执行测试用例
    print("\n开始执行测试用例...\n")
    exit_code = pytest.main(
        [
            "--clean-alluredir",
            "tests",  # 指定测试目录
        ]
    )
