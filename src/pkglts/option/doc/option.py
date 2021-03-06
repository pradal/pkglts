from os.path import dirname
from pkglts.dependency import Dependency
from pkglts.option_object import Option
from pkglts.option_tools import available_options
from pkglts.version import __version__

from . import history


class OptionDoc(Option):
    def version(self):
        return __version__

    def root_dir(self):
        return dirname(__file__)

    def update_parameters(self, cfg):
        sec = dict(
            description="belle petite description",
            fmt="rst",
            keywords=[]
        )
        cfg['doc'] = sec

    def check(self, cfg):
        invalids = []
        description = cfg['doc']['description']
        fmt = cfg['doc']['fmt']
        # keywords = env.globals['doc'].keywords

        if not description:
            invalids.append("doc.description")

        if fmt not in ('rst', 'md'):
            invalids.append("doc.fmt")

        return invalids

    def require_option(self):
        return ['base']

    def require(self, cfg):
        if cfg['doc']['fmt'] == 'md':
            yield Dependency('mkdocs', intent='doc')

    def environment_extensions(self, cfg):
        badges = []
        for name in cfg.installed_options():
            if name != 'doc':
                opt = available_options[name]
                ext = opt.environment_extensions(cfg)
                if 'badge' in ext:
                    badges.append(ext['badge'])
                if 'badges' in ext:
                    badges.extend(ext['badges'])

        return {"badges": badges}

    def tools(self, cfg):
        del cfg
        yield history.parser_history
