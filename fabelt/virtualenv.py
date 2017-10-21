import contextlib

from fabric.api import task, run, prefix

from fabelt import pip


__all__ = [
    'install',
    'create',
    'activate',
]


@task()
def install():
    pip.install('virtualenv')


@task()
def create(virtualenv):
    create_command = 'virtualenv {virtualenv}'
    create_command = create_command.format(virtualenv=virtualenv)
    run(create_command)


@contextlib.contextmanager
def activate(virtualenv):
    activate_command = 'source {virtualenv}/bin/activate'
    activate_command = activate_command.format(virtualenv=virtualenv)
    with prefix(activate_command):
        yield


