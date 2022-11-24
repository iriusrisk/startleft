# To simplify the methods naming, we use the following acronyms:
# - RTP (or rtp) stands for Release Testing Period.
# - RP (or rtp) stands for Release Period.
from unittest.mock import Mock

########
# MAIN #
########
MAIN_NO_HOTFIX_VERSION = Mock(
    branch='main', tag='1.5.0', distance=None, exact='True', node='gd6712fe')

# TODO: Review
MAIN_HOTFIX_VERSION = Mock(
    branch='main', tag='1.5.1', distance=None, exact='True', node='gea213e7')

##########
# HOTFIX #
##########

# TODO: Review
HOTFIX_VERSION = Mock(
    branch='hotfix/XXX-000', tag='1.5.0', distance=1, exact='False', node='ge7812ca')

###########
# RELEASE #
###########

# TODO: Review
RELEASE_VERSION_NO_BUGFIX = Mock(
    branch='release/1.6.0', tag='1.6.0rc1', distance=0, exact='True', node='g27522ae'
)

RELEASE_VERSION_BUGFIX = Mock(
    branch='release/1.6.0', tag='1.6.0rc1', distance=3, exact='False', node='ga1d748e'
)


##########
# BUGFIX #
##########
BUGFIX_VERSION = Mock(
    branch='bugfix/XXX-000', tag='1.6.0rc1', distance=1, exact='False', node='g6cda015')

#######
# DEV #
#######
DEV_RTP_VERSION = Mock(
    branch='dev', tag='1.6.0rc1', distance=19, exact='False', node='g17d9f68')

# TODO: Review
DEV_RP_VERSION = Mock(
    branch='dev', tag='1.6.0', distance=5, exact='False', node='g24d9a41')

###########
# FEATURE #
###########
FEATURE_RTP_VERSION = Mock(
    branch='feature/XXX-000', tag='1.6.0rc1', distance=3, exact='False', node='ga1d748e')

# TODO: Review
FEATURE_RP_VERSION = Mock(
    branch='feature/XXX-000', tag='1.6.0', distance=5, exact='False', node='ga1a547d')

##############
# FREE BRANCH#
##############
FREE_BRANCH_RTP_VERSION = Mock(
    branch='free_branch', tag='1.6.0rc1', distance=7, exact='False', node='g52d796a')

# TODO: Review
FREE_BRANCH_RP_VERSION = Mock(
    branch='free_branch', tag='1.6.0', distance=2, exact='False', node='g31a54fa')
