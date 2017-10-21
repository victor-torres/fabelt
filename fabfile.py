from fabric.api import env, task

from fabelt import *


env.project = 'my-project'
env.project_home = '/var/sites/{project}'.format(project=env.project)
env.virtualenv = '/usr/local/pythonenv/{project}'.format(project=env.project)


@task
def setup():
    """Example setup task"""
    pip.setup()
    virtualenv.install()
    virtualenv.create(env.virtualenv)
    with cd(env.project_home):
        with virtualenv.activate(env.virtualenv):
            pip.install_requirements()
            django.migrate()
            django.create_super_user()
            django.collect_static()
