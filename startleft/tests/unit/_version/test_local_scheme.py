import pytest

from startleft.startleft._version.local_scheme import choose_strategy_by_branch, guess_startleft_semver_suffix
from .version_mocks import *


class TestLocalScheme:
    # To simplify the methods naming, we use the following acronyms:
    # - RTP (or rtp) stands for Release Testing Period.
    # - RP (or rtp) stands for Release Period.

    @pytest.mark.parametrize('branch,expected_strategy', [
        ('main', '_no_local_version_strategy'),
        ('hotfix/XXX-000', '_node_strategy'),
        ('release/1.5.0', '_no_local_version_strategy'),
        ('bugfix/XXX-000', '_node_strategy'),
        ('dev', '_node_strategy'),
        ('feature/XXX-000', '_node_strategy'),
        ('UNKNOWN_BRANCH_PATTERN', '_node_strategy'),
    ])
    def test_strategy_by_branch(self, branch, expected_strategy):
        # GIVEN some branch
        # WHEN choose_strategy_by_branch is called
        strategy_fn = choose_strategy_by_branch(branch)

        # THEN the right strategy is chosen
        assert strategy_fn.__name__ == expected_strategy

    @pytest.mark.parametrize('scm_version,expected_version', [
        # MAIN
        (MAIN_NO_HOTFIX_VERSION, ''),
        (MAIN_HOTFIX_VERSION, ''),
        # HOTFIX
        (HOTFIX_VERSION, '+ge7812ca'),
        # RELEASE
        (RELEASE_VERSION_NO_BUGFIX, ''),
        (RELEASE_VERSION_BUGFIX, ''),
        # BUGFIX
        (BUGFIX_VERSION, '+g6cda015'),
        # DEV
        (DEV_RTP_VERSION, '+g17d9f68'),
        (DEV_RP_VERSION, '+g24d9a41'),
        # FEATURE
        (FEATURE_RTP_VERSION, '+ga1d748e'),
        (FEATURE_RP_VERSION, '+ga1a547d'),
        # FREE BRANCH
        (FREE_BRANCH_RTP_VERSION, '+g52d796a'),
        (FREE_BRANCH_RP_VERSION, '+g31a54fa'),
    ], ids=['test_main_no_hotfix_version',
            'test_main_hotfix_version',
            'test_hotfix_version',
            'test_release_version_no_bugfix',
            'test_release_version_bugfix',
            'test_bugfix_version',
            'test_dev_rtp_version',
            'test_dev_rp_version',
            'test_feature_rtp_version',
            'test_feature_rp_version',
            'test_free_branch_rtp_version',
            'test_free_branch_rp_version'])
    def test_main(self, scm_version, expected_version):
        # GIVEN a ScmVersion mock
        # WHEN guess_startleft_semver_suffix is called
        # THEN the expected version is returned
        assert guess_startleft_semver_suffix(scm_version) == expected_version
