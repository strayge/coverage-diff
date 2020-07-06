from invoke import run, task

name = 'coverage-diff'
src = 'coverage_diff'

@task
def isort(c):
    run(f'isort {src} -rc')


@task
def lint(c):
    run(f'flake8 {src} --ignore E501')


@task
def build(c):
    run('python setup.py sdist bdist_wheel')


@task
def clean(c):
    run('rm -rf ./build ./dist ./*.egg-info')


@task
def upload_test(c):
    run('python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*')


@task
def upload_release(c):
    run('python -m twine upload dist/*')


@task
def install_test(c):
    run(f'python -m pip install --index-url https://test.pypi.org/simple/ --no-deps {name}')


@task
def install_release(c):
    run(f'python -m pip install {name}')

@task
def uninstall(c):
    run(f'python -m pip uninstall {name}')
