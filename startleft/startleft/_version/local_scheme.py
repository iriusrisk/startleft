def choose_strategy_by_branch(branch: str) -> callable:
    if branch == 'main' or 'release/' in branch:
        return _no_local_version_strategy
    else:
        return _node_strategy


def guess_startleft_semver_suffix(version) -> str:
    return choose_strategy_by_branch(version.branch)(version)


def _node_strategy(version) -> str:
    if version.exact or version.node is None:
        return ''
    else:
        return f'+{version.node}'


def _no_local_version_strategy(version) -> str:
    return ''
