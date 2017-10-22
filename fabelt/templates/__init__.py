import os

import jinja2


__all__ = ['render']


def render(filename, args=None):
    if not args:
        args = dict()

    path = os.path.dirname(__file__)
    loader = jinja2.FileSystemLoader(path)
    env = jinja2.Environment(loader=loader)
    tmpl = env.get_template(filename)
    return tmpl.render(args)
