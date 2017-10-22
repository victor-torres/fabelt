import os

from fabric.api import env, put, run, task

from fabelt import apt, templates


__all__ = [
    'install',
    'config',
    'enable_app',
    'disable_app',
    'remove_app',
]


def get_module():
    args = dict(project=env.project)
    return '{project}.wsgi:application'.format(**args)


def get_socket():
    args = dict(project=env.project)
    return '/run/uwsgi/{project}.sock'.format(**args)


def get_logger(suffix=None):
    args = dict(project=env.project, suffix=suffix)
    logger = '/var/log/uwsgi/app/{project}'
    if suffix:
        logger += '-{suffix}'

    logger = logger.format(**args)
    return logger


def get_pid_file():
    args = dict(project=env.project)
    return '/run/uwsgi/{project}.pid'.format(**args)


def get_file_path(status='available'):
    args = dict(project=env.project, status=status)
    return '/etc/uwsgi/apps-{status}/{project}.ini'.format(**args)


@task
def install():
    # TODO: support multiple systems
    apt.install('uwsgi')


@task
def config(**kwargs):
    config = {
        'virtualenv': env.virtualenv,
        'module': get_module(),
        'master': 'true',
        'processes': 4,
        'socket': get_socket(),
        'chmod_socket': 666,
        'vacuum': 'true',
        'logger': get_logger('error'),
        'req_logger': get_logger('access'),
        'pidfile': get_pid_file(),
        'uid': 'www-data',
        'gid': 'www-data'
    }
    config.update(kwargs)
    config = templates.render('uwsgi.ini', config)
    tmp_file_path = '/tmp/uwsgi.ini.tmp'
    with open(tmp_file_path, 'w') as f:
        f.write(config)

    file_path = get_file_path()
    put(tmp_file_path, file_path)


@task
def enable_app():
    available_file_path = get_file_path(status='available')
    enabled_file_path = get_file_path(status='enabled')
    run('ln -sf {0} {1}'.format(available_file_path, enabled_file_path))


@task
def disable_app():
    enabled_file_path = get_file_path(status='enabled')
    run('rm {0}'.format(enabled_file_path))


@task
def remove_app():
    available_file_path = get_file_path(status='available')
    run('rm {0}'.format(available_file_path))
