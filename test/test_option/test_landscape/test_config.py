import pytest
from pkglts.config_management import Config
from pkglts.option.landscape.option import OptionLandscape


@pytest.fixture()
def opt():
    return OptionLandscape('landscape')


def test_root_dir_is_defined(opt):
    assert opt.root_dir() is not None


def test_require(opt):
    cfg = Config(dict(landscape={}))

    assert len(opt.require('option', cfg)) == 4
    assert len(opt.require('setup', cfg)) == 0
    assert len(opt.require('install', cfg)) == 0
    assert len(opt.require('dvlpt', cfg)) == 0
