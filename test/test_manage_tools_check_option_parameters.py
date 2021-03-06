from pkglts.config_management import Config, DEFAULT_CFG
from pkglts.manage_tools import check_option_parameters


def test_check_handle_option_config_not_existing():
    cfg = Config(DEFAULT_CFG)
    assert len(check_option_parameters("toto", cfg)) == 0


def test_check_handle_option_defines_no_check():
    cfg = Config(DEFAULT_CFG)
    assert len(check_option_parameters("coverage", cfg)) == 0
