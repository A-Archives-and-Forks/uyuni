# Client code for Update Agent
# Copyright (c) 2011 Red Hat, Inc.  Distributed under GPL.
#
# Author: Simon Lukasik
#

# substituted to the prefered platfrom by Makefile
_platform='@PLATFORM@'
def getPlatform():
    if _platform != '@PLAT' + 'FORM@':
        return _platform
    else:
        return 'rpm'

