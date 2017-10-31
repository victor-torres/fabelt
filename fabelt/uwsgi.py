import os

from fabric.api import env, put, run, task

from fabelt import apt, templates


__all__ = [
    'install',
    'config',
    'enable_app',
    'disable_app',
    'remove_app',
    'restart',
]


def get_file_path(status='available'):
    args = dict(project=env.project, status=status)
    return '/etc/uwsgi/apps-{status}/{project}.ini'.format(**args)


@task
def install():
    # TODO: support multiple systems
    apt.install('uwsgi uwsgi-plugin-python')


@task
def config():
    config = {
        'chdir': env.project_home,
        'virtualenv': env.virtualenv,
        'wsgi_file': env.wsgi_file
    }
    config = templates.render('uwsgi.ini', config)
    tmp_file_path = '/tmp/uwsgi.ini.tmp'
    with open(tmp_file_path, 'w') as f:
        f.write(config)

    file_path = get_file_path(status='available')
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


@task
def restart():
    # TODO: support other systems
    run('/etc/init.d/uwsgi restart')


@task
def start():
    # TODO: support other systems
    run('/etc/init.d/uwsgi start')

@task
def stop():
    # TODO: support other systems
    run('/etc/init.d/uwsgi stop')

