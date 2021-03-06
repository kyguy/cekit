import pytest
import sys

from cekit.cli import Cekit


@pytest.mark.parametrize('command', ['generate', 'build', 'test'])
def test_args_command(mocker, command):
    mocker.patch.object(sys, 'argv', ['cekit', command])

    assert Cekit().parse().args.commands == [command]


def test_args_not_valid_command(mocker):
    mocker.patch.object(sys, 'argv', ['cekit', 'explode'])

    with pytest.raises(SystemExit):
        Cekit().parse()


def test_args_build_pull(mocker):
    mocker.patch.object(sys, 'argv', ['cekit', 'build', '--build-pull'])

    assert Cekit().parse().args.build_pull


@pytest.mark.parametrize('engine', ['osbs', 'docker', 'buildah'])
def test_args_build_engine(mocker, engine):
    mocker.patch.object(sys, 'argv', ['cekit', 'build', '--build-engine', engine])

    assert Cekit().parse().args.build_engine == engine


def test_args_osbs_stage(mocker):
    mocker.patch.object(sys, 'argv', ['cekit', 'build', '--build-osbs-stage'])

    assert Cekit().parse().args.build_osbs_stage is True


def test_args_osbs_stage_false(mocker):
    mocker.patch.object(sys, 'argv', ['cekit', 'build'])

    assert Cekit().parse().args.build_osbs_stage is False


def test_args_invalid_build_engine(mocker):
    mocker.patch.object(sys, 'argv', ['cekit', 'build', '--build-engine', 'rkt'])

    with pytest.raises(SystemExit):
        Cekit().parse()


def test_args_osbs_user(mocker):
    mocker.patch.object(sys, 'argv', ['cekit',
                                      'build',
                                      '--build-engine',
                                      'osbs',
                                      '--build-osbs-user',
                                      'USER'])

    assert Cekit().parse().args.build_osbs_user == 'USER'


def test_args_config_default(mocker):
    mocker.patch.object(sys, 'argv', ['cekit',
                                      'generate'])

    assert Cekit().parse().args.config == '~/.cekit/config'


def test_args_workd_dir(mocker):
    mocker.patch.object(sys, 'argv', ['cekit',
                                      'generate',
                                      '--work-dir',
                                      'foo'])

    assert Cekit().parse().args.work_dir == 'foo'


def test_args_config(mocker):
    mocker.patch.object(sys, 'argv', ['cekit',
                                      '--config',
                                      'whatever',
                                      'generate'])

    assert Cekit().parse().args.config == 'whatever'


def test_args_target(mocker):
    mocker.patch.object(sys, 'argv', ['cekit',
                                      'build',
                                      '--target',
                                      'foo'])

    assert Cekit().parse().args.target == 'foo'


def test_args_redhat(mocker):
    mocker.patch.object(sys, 'argv', ['cekit',
                                      '--redhat',
                                      'build'])

    assert Cekit().parse().args.redhat


def test_args_redhat_default(mocker):
    mocker.patch.object(sys, 'argv', ['cekit',
                                      'build'])

    assert not Cekit().parse().args.redhat


def test_args_osbs_nowait(mocker):
    mocker.patch.object(sys, 'argv', ['cekit',
                                      'build',
                                      '--build-osbs-nowait'])

    assert Cekit().parse().args.build_osbs_nowait is True


def test_args_osbs_no_nowait(mocker):
    mocker.patch.object(sys, 'argv', ['cekit',
                                      'build'])

    assert Cekit().parse().args.build_osbs_nowait is False


def test_args_overrides(mocker):
    mocker.patch.object(sys, 'argv', ['cekit',
                                      'build',
                                      '--overrides',
                                      'foo'])

    assert Cekit().parse().args.overrides == ['foo']


def test_args_overrides_file(mocker):
    mocker.patch.object(sys, 'argv', ['cekit',
                                      'build',
                                      '--overrides-file',
                                      'foo'])

    assert Cekit().parse().args.overrides == ['foo']


def test_args_overrides_exclusiver(mocker):
    mocker.patch.object(sys, 'argv', ['cekit',
                                      'build',
                                      'overrides',
                                      'bar',
                                      '--overrides-file',
                                      'foo'])

    with pytest.raises(SystemExit):
        Cekit().parse()
