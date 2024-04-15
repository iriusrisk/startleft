from pytest import mark, param


from startleft.startleft._version.local_scheme import choose_strategy_by_branch, guess_startleft_semver_suffix, DEFAULT_LOCAL_PART
from .version_mocks import *


class TestLocalScheme:
    # To simplify the methods naming, we use the following acronyms:
    # - RTP (or rtp) stands for Release Testing Period.
    # - RP (or rtp) stands for Release Period.

    @mark.parametrize('branch,expected_strategy', [
        ('main', '_no_local_version_strategy'),
        ('hotfix/XXX-000', '_node_strategy'),
        ('release/1.5.0', '_no_local_version_strategy'),
        ('bugfix/XXX-000', '_node_strategy'),
        ('support/1.19', '_no_local_version_strategy'),
        ('supfix/XXX-000', '_node_strategy'),
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

    @mark.parametrize('scm_version,expected_version', [
        # MAIN
        param(MAIN_NO_HOTFIX_VERSION, '', id='test_main_no_hotfix_version'),
        param(MAIN_HOTFIX_VERSION, '', id='test_main_hotfix_version'),
        # HOTFIX
        param(HOTFIX_VERSION, '+g550c1c9', id='test_hotfix_version'),
        # RELEASE
        param(RELEASE_VERSION_NO_BUGFIX, '', id='test_release_version_no_bugfix'),
        param(RELEASE_VERSION_BUGFIX, '', id='test_release_version_bugfix'),
        # BUGFIX
        param(BUGFIX_VERSION, '+g6cda015', id='test_bugfix_version'),
        # SUPFIX
        param(SUPFIX_VERSION, '+g6cda015', id='test_supfix_version'),
        # DEV
        param(DEV_RTP_VERSION, '+g17d9f68', id='test_dev_rtp_version'),
        param(DEV_RP_VERSION, '+g3e49113', id='test_dev_rp_version'),
        # FEATURE
        param(FEATURE_RTP_VERSION, '+ga1d748e', id='test_feature_rtp_version'),
        param(FEATURE_RP_VERSION, '+g76d029f', id='test_feature_rp_version'),
        # FREE BRANCH
        param(FREE_BRANCH_RTP_VERSION, '+g52d796a', id='test_free_branch_rtp_version'),
        param(FREE_BRANCH_RP_VERSION, '+g31a54fa', id='test_free_branch_rp_version'),
    ])
    def test_main(self, scm_version, expected_version):
        # GIVEN a ScmVersion mock
        # WHEN guess_startleft_semver_suffix is called
        version = guess_startleft_semver_suffix(scm_version)

        # THEN the expected version is returned
        assert version == expected_version

    def test_error_calculating_local_part(self):
        # GIVEN some invalid version
        version = Mock(branch= 'dev', tag='invalid_version')

        # WHEN guess_startleft_semver_suffix is called
        version = guess_startleft_semver_suffix(version)

        # THEN no local part is returned
        assert version == DEFAULT_LOCAL_PART
