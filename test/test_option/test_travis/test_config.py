import pytest
from pkglts.config_management import Config
from pkglts.option.travis.option import OptionTravis


@pytest.fixture()
def opt():
    return OptionTravis('travis')


def test_root_dir_is_defined(opt):
    assert opt.root_dir() is not None


def test_require_option(opt):
    assert len(tuple(opt.require_option())) == 3


def test_require(opt):
    cfg = Config()
    opt.update_parameters(cfg)

    assert len(tuple(opt.require(cfg))) == 0
