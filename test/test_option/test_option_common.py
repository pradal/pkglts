from glob import glob
from os import path

import pkglts
from pkglts.config_management import Config
from pkglts.option_tools import available_options


def test_options_expose_parameters():
    # walk through all possible options defined by pkglts
    option_basedir = path.join(path.dirname(pkglts.__file__), 'option')
    for pth in glob("{}/*/".format(option_basedir)):
        option_name = path.basename(path.dirname(pth))
        if not option_name.startswith("_"):
            # check 'update_parameters' exists for each option
            try:
                opt = available_options[option_name]
                cfg = {}
                opt.update_parameters(cfg)
                assert len(cfg) == 1
            except KeyError:
                assert False


def test_require_correctly_defined():
    cfg = Config(dict(base={}, doc={'fmt': 'rst'}, sphinx={'theme': 'default'}, test={'suite_name': 'pytest'}))

    # walk through all possible options
    option_basedir = path.join(path.dirname(pkglts.__file__), 'option')
    for pth in glob("{}/*/".format(option_basedir)):
        option_name = path.basename(path.dirname(pth))
        if not option_name.startswith("_"):
            # check 'require' function exists for each option
            try:
                opt = available_options[option_name]
                assert len(tuple(opt.require_option())) >=0
                assert len(tuple(opt.require(cfg))) >= 0
            except ImportError:
                assert False
