import pytest
from pkglts.config_management import Config
from pkglts.option.gitlab.option import OptionGitlab


@pytest.fixture()
def opt():
    return OptionGitlab('gitlab')


def test_root_dir_is_defined(opt):
    assert opt.root_dir() is not None


def test_update_parameters(opt):
    cfg = {}
    opt.update_parameters(cfg)
    assert len(cfg['gitlab']) == 4


def test_config_check_project_exists(opt):
    cfg = Config(dict(gitlab={'owner': "", 'project': "", 'server': "", "url": ""}))
    assert 'gitlab.project' in opt.check(cfg)


def test_require_option(opt):
    assert len(tuple(opt.require_option())) == 1


def test_require(opt):
    cfg = Config()
    opt.update_parameters(cfg)

    assert len(tuple(opt.require(cfg))) == 0
