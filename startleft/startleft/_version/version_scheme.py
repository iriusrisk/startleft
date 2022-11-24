import re

from setuptools_scm import ScmVersion

MINOR_VERSION_POSITION = 1
PATCH_VERSION_POSITION = 2


def choose_strategy_by_branch(branch: str) -> callable:
    if branch == 'main' or 'release/' in branch:
        return _tag_version_strategy
    elif 'hotfix/' in branch:
        return _patch_version_dev_commit_strategy
    elif 'bugfix' in branch:
        return _tag_version_dev_commit_strategy
    else:
        return _minor_version_dev_commit_strategy


def guess_startleft_semver(version: ScmVersion) -> str:
    return choose_strategy_by_branch(version.branch)(version)


# Version generation strategies
def _tag_version_strategy(version: ScmVersion) -> str:
    return str(version.tag)


def _patch_version_dev_commit_strategy(version: ScmVersion) -> str:
    return __build_dev_version(
        semver=__increment_version(str(version.tag), PATCH_VERSION_POSITION),
        distance=version.distance
    )


def _tag_version_dev_commit_strategy(version: ScmVersion) -> str:
    return __build_dev_version(
        semver=str(version.tag),
        distance=version.distance
    )


def _minor_version_dev_commit_strategy(version: ScmVersion) -> str:
    semver = re.sub(r'rc[0-9]+', '', str(str(version.tag)))

    return __build_dev_version(
        semver=__increment_version(semver, MINOR_VERSION_POSITION),
        distance=version.distance
    )


def __build_dev_version(semver: str, distance: int):
    return f'{semver}.dev{distance}'


def __increment_version(semver: str, position: int):
    version_parts = semver.split('.')
    version_parts[position] = str(int(version_parts[position]) + 1)
    return '.'.join(version_parts)


