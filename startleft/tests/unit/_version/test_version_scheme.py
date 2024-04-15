import random

from pytest import mark, param

from startleft.startleft._version.version_scheme import choose_strategy_by_branch, guess_startleft_semver, \
    DEFAULT_VERSION
from .version_mocks import *


def rand_bool() -> bool:
    return bool(random.getrandbits(1))


class TestVersionScheme:
    # To simplify the methods naming, we use the following acronyms:
    # - RTP (or rtp) stands for Release Testing Period.
    # - RP (or rtp) stands for Release Period.

    @mark.parametrize('branch,expected_strategy', [
        ('main', '_tag_version_strategy'),
        ('hotfix/XXX-000', '_patch_version_dev_commit_strategy'),
        ('release/1.5.0', '_tag_version_strategy'),
        ('bugfix/XXX-000', '_tag_version_dev_commit_strategy'),
        ('support/1.19', '_tag_version_strategy'),
        ('supfix/XXX-000', '_patch_version_dev_commit_strategy'),
        ('dev', '_minor_version_dev_commit_strategy'),
        ('feature/XXX-000', '_minor_version_dev_commit_strategy'),
        ('UNKNOWN_BRANCH_PATTERN', '_minor_version_dev_commit_strategy'),
    ])
    def test_strategy_by_branch(self, branch, expected_strategy):
        # GIVEN some branch
        # WHEN choose_strategy_by_branch is called
        strategy_fn = choose_strategy_by_branch(branch, rand_bool())

        # THEN the right strategy is chosen
        assert strategy_fn.__name__ == expected_strategy

    @mark.parametrize('exact,expected_strategy', [
        param(True, '_tag_version_strategy', id='exact version'),
        param(False, '_minor_version_dev_commit_strategy', id='non exact version')])
    def test_detached_head(self, exact: bool, expected_strategy):
        # GIVEN a detached head
        branch = 'HEAD'

        # AND a parametrized exact flag

        # WHEN choose_strategy_by_branch is called
        strategy_fn = choose_strategy_by_branch(branch, exact)

        # THEN the right strategy is chosen
        assert strategy_fn.__name__ == expected_strategy


    @mark.parametrize('scm_version,expected_version', [
        # MAIN
        param(MAIN_NO_HOTFIX_VERSION, '1.5.0', id='test_main_no_hotfix_version'),
        param(MAIN_HOTFIX_VERSION, '1.5.1', id='test_main_hotfix_version'),
        # HOTFIX
        param(HOTFIX_VERSION, '1.5.1.dev18', id='test_hotfix_version'),
        # RELEASE
        param(RELEASE_VERSION_NO_BUGFIX, '1.6.0rc1', id='test_release_version_no_bugfix'),
        param(RELEASE_VERSION_BUGFIX, '1.6.0rc1', id='test_release_version_bugfix'),
        # BUGFIX
        param(BUGFIX_VERSION, '1.6.0rc1.dev1', id='test_bugfix_version'),
        # SUPPORT
        param(SUPPORT_VERSION_NO_SUPFIX, '1.19.0', id='test_support_version_no_supfix'),
        param(SUPPORT_VERSION_SUPFIX, '1.19.1', id='test_support_version_supfix'),
        # SUPFIX
        param(SUPFIX_VERSION, '1.19.1.dev1', id='test_supfix_version'),
        # DEV
        param(DEV_RTP_VERSION, '1.7.0.dev19', id='test_dev_rtp_version'),
        param(DEV_RTP_NO_DISTANCE_VERSION, '1.7.0', id='test_dev_rtp_no_distance_version'),
        param(DEV_RP_VERSION, '1.7.0.dev3', id='test_dev_rp_version'),
        param(DEV_RP_HOTFIX_VERSION, '1.7.0.dev3', id='test_dev_rp_hotfix_version'),
        # FEATURE
        param(FEATURE_RTP_VERSION, '1.7.0.dev3', id='test_feature_rtp_version'),
        param(FEATURE_RP_VERSION, '1.7.0.dev4', id='test_feature_rp_version'),
        param(FEATURE_RP_HOTFIX_VERSION, '1.7.0.dev14', id='test_feature_rp_hotfix_version'),
        # FREE BRANCH
        param(FREE_BRANCH_RTP_VERSION, '1.7.0.dev7', id='test_free_branch_rtp_version'),
        param(FREE_BRANCH_RP_VERSION, '1.7.0.dev2', id='test_free_branch_rp_version'),
        param(FREE_BRANCH_RP_HOTFIX_VERSION, '1.7.0.dev1', id='test_free_branch_rp_hotfix_version'),
    ])
    def test_main(self, scm_version, expected_version):
        # GIVEN a ScmVersion mock
        # WHEN guess_startleft_semver is called
        version = guess_startleft_semver(scm_version)

        # THEN the expected version is returned
        assert version == expected_version

    def test_error_calculating_version(self):
        # GIVEN some invalid version
        version = Mock(branch='dev', tag='invalid_version')

        # WHEN guess_startleft_semver_suffix is called
        version = guess_startleft_semver(version)

        # THEN no local part is returned
        assert version == DEFAULT_VERSION
