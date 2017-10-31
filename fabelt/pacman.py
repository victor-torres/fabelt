from fabric.api import task, run


@task()
def install(package):
    args = dict(package=package)
    run('pacman -S {package}'.format(**args))
