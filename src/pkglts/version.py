"""
Maintain version for this package.
"""
# {# pkglts, version
#  -*- coding: utf-8 -*-

major = 2
"""(int) Version major component."""

minor = 3
"""(int) Version minor component."""

post = 4
"""(int) Version post or bugfix component."""

__version__ = ".".join([str(s) for s in (major, minor, post)])
# #}
