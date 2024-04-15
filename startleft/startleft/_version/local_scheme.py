DEFAULT_LOCAL_PART = ''


def choose_strategy_by_branch(branch_name: str) -> callable:
    """
    This function chooses the right strategy for calculating the version of the application based on the given branch name.
    :param branch_name: The name of the branch for which the version is being calculated
    :return: The callable for the version strategy calculation
    """
    if branch_name == 'main' or 'release/' in branch_name or 'support/' in branch_name:
        return _no_local_version_strategy
    else:
        return _node_strategy


def guess_startleft_semver_suffix(scm_version) -> str:
    """
    Custom function to retrieve the local part of the StartLeft version from git tags. It is intended to be used by the
    setuptools_scm by injecting it through use_scm_version.local_scheme property. It is based on a strategy pattern
    with a specific behaviour depending on the branch over what the version is being calculated.
    :param scm_version: An object from the setuptools_scm lib that contains all the git describe command output info.
    :return: The formatted local part of the version of StartLeft. I.e.: +g52d796a.
    """
    try:
        return choose_strategy_by_branch(scm_version.branch)(scm_version)
    except Exception:
        return DEFAULT_LOCAL_PART


def _node_strategy(scm_version) -> str:
    """
    Strategy that returns the last short hash of the last commit where the branch is located.
    :param scm_version: An object from the setuptools_scm lib that contains all the git describe command output info.
    :return: The formatted str for the version local part.
    """
    if scm_version.exact or scm_version.node is None:
        return ''
    else:
        return f'+{scm_version.node}'


def _no_local_version_strategy(scm_version) -> str:
    """
    Strategy that return an empty str as local part for the StartLeft version.
    :return: An empty str.
    """
    return ''
