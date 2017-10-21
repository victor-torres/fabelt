from fabric.api import env, puts, run, task

from fabelt import templates


__all__ = [
    'install',
    'config'
]


def get_module():
    args = dict(project=env.project)
    return '{project}.wsgi:application'.format(**args)


def get_socket():
    args = dict(project=env.project)
    return '/run/uwsgi/{project}.sock'.format(**args)


def get_logger(suffix=None):
    args = dict(project=env.project)
    logger = '/var/log/uwsgi/app/{project}'
    if suffix:
        logger += suffix

    return logger


def get_pid_file():
    args = dict(project=env.project)
    return '/run/uwsgi/{project}.pid'.format(**args)


def get_filename():
    args = dict(project=env.project)
    return '/etc/uwsgi/apps-available/{project}.ini'.format(**args)


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
        'chmod-socket': 666,
        'vacuum': 'true',
        'logger': get_logger('error'),
        'req-logger': get_logger('access'),
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
    puts(tmp_file_path, file_path)
