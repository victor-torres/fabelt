from fabric.api import task, run


@task()
def install(package):
    args = dict(package=package)
    run('apt-get -y --quiet install {package}'.format(**args))
