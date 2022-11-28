import re

MINOR_VERSION_POSITION = 1
PATCH_VERSION_POSITION = 2


def choose_strategy_by_branch(branch_name: str) -> callable:
    """
    This function chooses the right strategy for calculating the version of the application based on the given branch name.
    :param branch_name: The name of the branch for which the version is being calculated
    :return: The callable for the version strategy calculation
    """
    if branch_name == 'main' or 'release/' in branch_name:
        return _tag_version_strategy
    elif 'hotfix/' in branch_name:
        return _patch_version_dev_commit_strategy
    elif 'bugfix' in branch_name:
        return _tag_version_dev_commit_strategy
    else:
        return _minor_version_dev_commit_strategy


def guess_startleft_semver(scm_version) -> str:
    """
    Custom function to retrieve the StartLeft version from git tags. It is intended to be used by the setuptools_scm
    by injecting it through use_scm_version.version_scheme property. It is based on a strategy pattern with a
    specific behaviour depending on the branch over what the version is being calculated.
    :param scm_version: An object from the setuptools_scm lib that contains all the git describe command output info.
    :return: The formatted version of StartLeft (without the commit suffix, calculated by the local_scheme). I.e.:
    1.5.0.dev5
    """
    return choose_strategy_by_branch(scm_version.branch)(scm_version)


def _tag_version_strategy(scm_version) -> str:
    """
    Strategy that returns as version the last tag found by the git describe command. For example, if the last tag is
    1.5.0, it will return 1.5.0.
    :param scm_version: An object from the setuptools_scm lib that contains all the git describe command output info.
    :return: The formatted str for the version.
    """
    return str(scm_version.tag)


def _patch_version_dev_commit_strategy(scm_version) -> str:
    """
    Strategy that takes the last tag found by the git describe command and increases it by one in its patch part. For
    example, if the last tag is 1.5.0, it will return 1.5.1.devN (N is the distance from the tag to the current commit).
    :param scm_version: An object from the setuptools_scm lib that contains all the git describe command output info.
    :return: The formatted str for the version.
    """
    return __build_dev_version(
        semver=__increment_version(str(scm_version.tag), PATCH_VERSION_POSITION),
        distance=scm_version.distance
    )


def _tag_version_dev_commit_strategy(scm_version) -> str:
    """
    Strategy that takes the last tag found by the git describe command and returns it without increasing any part,
    but adding the dev section. For example, if the last tag is 1.6.0rc1, it will return 1.6.0rc1.devN (N is the
    distance from the tag to the current commit).
    :param scm_version: An object from the setuptools_scm lib that contains all the git describe command output info.
    :return: The formatted str for the version.
    """
    return __build_dev_version(
        semver=str(scm_version.tag),
        distance=scm_version.distance
    )


def _minor_version_dev_commit_strategy(scm_version) -> str:
    """
    Strategy that takes the last tag found by the git describe command and increases it by one in its minor part. For
    example, if the last tag is 1.5.0, it will return 1.6.0.devN (N is the distance from the tag to the current commit).
    :param scm_version: An object from the setuptools_scm lib that contains all the git describe command output info.
    :return: The formatted str for the version.
    """
    semver = re.sub(r'rc[0-9]+', '', str(str(scm_version.tag)))

    return __build_dev_version(
        semver=__increment_version(semver, MINOR_VERSION_POSITION),
        distance=scm_version.distance
    )


def __build_dev_version(semver: str, distance: int):
    return f'{semver}.dev{distance}'


def __increment_version(semver: str, position: int):
    version_parts = semver.split('.')
    version_parts[position] = str(int(version_parts[position]) + 1)
    return '.'.join(version_parts)
