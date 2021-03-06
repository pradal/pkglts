"""Regroup set of functions that make use of local environment
inside a package. Just a way to normalize pre defined paths.
"""
from os import path

from .templating import render


def pkg_full_name(cfg):
    """Compute name of src dir according to pkgname
    and namespace in environment

    Args:
        cfg (Config):  current package configuration

    Returns:
        (str)
    """
    namespace = cfg['base']['namespace']
    if namespace is None:
        return cfg['base']['pkgname']

    return namespace + "." + cfg['base']['pkgname']


def src_dir(cfg):
    """Compute name of src dir according to pkgname
    and namespace in environment

    Args:
        cfg (Config):  current package configuration

    Returns:
        (str)
    """
    rep = "src"
    namespace = cfg['base']['namespace']
    if namespace is not None:
        rep = rep + "/" + namespace

    pkgname = cfg['base']['pkgname']
    rep = rep + "/" + pkgname

    return rep


def init_namespace_dir(pth, cfg):
    """Populate a directory with specific __init__.py
    for namespace packages.

    Args:
        pth (str): path in which to create the files
        cfg (Config):  current package configuration

    Returns:
        None
    """
    src_pth = path.dirname(__file__) + "/resource/namespace__init__.py.tpl"
    tgt_pth = pth + "/__init__.py"
    render(cfg, src_pth, tgt_pth)
