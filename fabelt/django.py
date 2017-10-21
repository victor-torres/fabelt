from fabric.api import task, run


@task
def manage(command):
    args = dict(command=command)
    run('python manage.py {command}'.format(**args))


@task
def migrate():
    manage('migrate')


@task
def create_super_user():
    # TODO: receive username and password as parameters
    manage('createsuperuser')


@task
def collect_static():
    manage('collectstatic')

