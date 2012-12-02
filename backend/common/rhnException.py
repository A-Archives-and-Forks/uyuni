#
# Copyright (c) 2008--2012 Red Hat, Inc.
#
# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.
#
# Red Hat trademarks are not licensed under GPLv2. No permission is
# granted to use or replicate Red Hat trademarks that are incorporated
# in this software or its documentation.
#

import sys
import xmlrpclib


from cStringIO import StringIO


# What other rhn modules we need
from rhnTranslate import _
import rhnFlags


# default template values for error messages
templateValues = {
    'hostname': 'example.com',
    }


# This array translates exception codes into meaningful messages
# for the eye of the beholder
# DOMAINS:
#   0-999:     RHN client/client-like interaction errors
#   1000-1999: RHN Proxy specific interaction errors
#   2000-2999: RHN Satellite specific interation errors

FaultArray = {
     10000: _("Outage mode"),
     # 0-999: RHN client/client-like interaction errors:
     1: _("This does not appear to be a valid username."),
     2: _("Invalid username and password combination."),
     3: _("This login is already taken, or the password is incorrect."),
     4: _("Permission denied."),
     5: _("Can not create new entry."),
     6: _("Object not found."),
     7: _("Account limits exceeded."),
     8: _("Invalid System Digital ID."),
     9: _("Invalid System Credentials."),
     10: _("Could not retrieve user data from database."),
     11: _("Valid username required."),
     12: _("Valid password required."),
     13: _("Minimum username length violation."),
     14: _("Minimum password length violation."),
     15: _("The username contains invalid characters."),
     16: _("Invalid product registration code."),
     17: _("File not found."),
     18: _("Invalid Architecture and OS release combination."),
     19: _("Architecture and OS version combination is not supported."),
     20: _("Could not retrieve system data from database."),
     21: _("Invalid arguments passed to function."),
     22: _("Unable to retrieve requested entry."),
     23: _("Could not update database entry."),
     24: _("Unsupported server architecture."),
     25: _("LDAP operation failed."),
     26: _("Backend RPM database failure: can not retrieve \
requested information."),
     27: _("Server Entry is busy."),
     28: _("""
     The anonymous server functionality is no longer available.

     Please re-register this system by running mgr_register as root.
     Please visit https://%(hostname)s/rhn/systems/SystemEntitlements.do
     or login at https://%(hostname)s, and from the "Overview" tab, select
     "Subscription Management" to enable SUSE Manager service for this system.
     """),
     29: _("Record not available in the database."),
     30: _("Invalid value for entry."),
     31: _("""
     This system does not have a valid entitlement for SUSE Manager.
     Please visit https://%(hostname)s/rhn/systems/SystemEntitlements.do
     or login at https://%(hostname)s, and from the "Overview" tab, select
     "Subscription Management" to enable SUSE Manager service for this system.
     """),
     32: _("Channel error"),
     33: _("Client session token is invalid."),
     34: _("Client session token has expired."),
     35: _("You are not authorized to retrieve the requested object."),
     36: _("Invalid action"),
     37: _("You are not allowed to perform administrative tasks \
on this system."),
     38: _("The system is already subscribed to the specified channel."),
     39: _("The system is not currently subscribed to the specified channel."),
     40: _("The specified channel does not exist."),
     41: _("Invalid channel version."),
     42: _("Invalid ORG_ID requested"),
     43: _("""
     User group membership limits exceeded.

     The current settings for your account do not allow you to add another
     user account. Please check with the organization administrator for your
     account whether the maximum number of users allowed to subscribe to
     SUSE Manager needs to be changed.
     """),
     44: _("""
     System group membership limits exceeded.

     The current settings for your account do not allow you to add another
     system profile. Please check with the organization administrator for your
     account for modifying the maximum number of system profiles that can be
     subscribed to your SUSE Manager account.
     """),
     45: _("""
     Invalid architecture.

     The architecture of the package is not supported by SUSE Manager
     """),
     46: _("""
     Incompatible architectures.

     The architecture of the package you are trying to upload is not
     compatible with the channel architecture.
     """),
     47: _("""Invalid RPM header"""),
     48: _("""
     Invalid channel.

     The channel you have specified does not exist.
     """),
     # originally "Too many connections to RHN from this system and account"
     49: _("""
     rhnFault 49. This should not happen with SUSE Manager.
     """),
     # For the uploading tools
     50: _("Invalid information uploaded to the server"),
     # originally "RHN Demo service disabled"
     51: _("""
     rhnFault 51: This should not happen with SUSE Manager
     """),
     # originally "Access to RHN limited to subscribed customers"
     52: _("""
     rhnFault 52. This should not happen with SUSE Manager.
     """),
     53: _("Error uploading network interfaces configuration."),
     54: _("""
     Package Upload Failed due to uniqueness constraint violation.
     Make sure the package does not have any duplicate dependencies or
     does not already exists on the server
     """),
     55: _("""
     The --force rhnpush option is disabled on this server. 
     Please contact your SUSE Manager administrator for more help.
     """),

     # 60-70: token errors
     60: _("""
     The activation token specified could not be found on the server.
     Please retry with a valid key.
     """),
     61: _("Too many systems registered using this registration token"),
     62: _("Token contains invalid, obsoleted or insufficient settings"),
     63: _("Conflicting activation tokens"),

     # 70-80: channel subscription errors
     70: _("""
     All available subscriptions for the requested channel have been exhausted.
     Please contact a SUSE sales representative.
     """),
     71: _("""
     You do not have subscription permission to the designated channel.
     Please refer to your organization's channel or organization
     administrators for further details.
     """),
     72: _("""You can not unsubscribe from base channel."""),
     73: _("""Satellite or Proxy channel can not be subscribed."""),

     # 80-90: server group errors
     80: _("There was an error while trying to join the system to its groups"),

     # 90-100: entitlement errors
     90: _("Unable to entitle system"),
     91: _("Registration token unable to entitle system: \
maximum membership exceeded"),

     # 100-109: e-mail and uuid related faults
     100: _("Maximum e-mail length violation."),
     101: _("Changing e-mail address is not supported."),
     105: _("This system has been previously registered."),
     106: _("Invalid username"),

     # 110-129: disabled org errors
     110: _("Service for your account has been disabled."),
     111: _("Email address not validated; service disabled"),
     112: _("Survey not filled out; service disabled"),

     # 130-140: bugzilla errata import errors
     130: _("Bugzilla import error"),

     # 140-159 applet errors
     140: _("Unable to look up server"),

     # 160-179: OSAD errors
     160: _("Required argument is missing"),

     # 500-599: Package Uploader errors
     500: _("Missing HTTP header information"),
     501: _("The package's checksum signature does not match the header one"),
     502: _("Header information does not match package metainformation"),
     503: _("Package with a different signature already uploaded"),
     504: _("Not an RPM package"),
     505: _("Unsigned RPM package"),
     506: _("Incompatible package and channel architectures"),
     507: _("Incompatible checksum type"),

     # 600-699: RHEL5+ EN errors
     600: _("Invalid Entitlement Number"),
     601: _("No entitlement information tied to hardware"),
     602: _("Installation number is not entitling"),

     # 700-799: Additional user input verification errors.
     700: _("Maximum username length violation"),
     701: _("Maximum password length violation"),

     800: _("System Name cannot be less than 3 characters"),

     # 1000-1999: RHN Proxy specific errors:
     # issued by an RHN Proxy to the client
     1000: _("SUSE Manager Proxy error."),
     1001: _("SUSE Manager Proxy unable to login."),
     # issued by an RHN Server/Satellite to the proxy
     1002: _("""
     SUSE Manager Proxy system ID does not match any SUSE Manager Proxy
     Server in the database.
     """),
     1003: _("SUSE Manager Proxy session token is invalid."),
     1004: _("SUSE Manager Proxy session token has expired."),


     # 2000-2999: RHN Satellite specific errors:
     2001: _("""
     SUSE Manager user creation is not allowed via mgr_register.
     Please contact your sysadmin to have your account created.
     """),
     # originally "Satellite system ID not found in RHN database"
     2002: _("""
     rhnFault 2002. This should not happen with SUSE Manager.
     """),
     2003: _("""
     This SUSE Manager server is not allowed to access the specified channel
     """),
     2004: _("""
     This SUSE Manager server is not allowed to use Inter Server Sync on this server
     """),
     2005: _("""
     Inter Server Sync is disabled on this SUSE Manager.
     """),

     # Kickstart errors
     2100: _("Access denied to autoinstallation tree"),
     2101: _("Could not find autoinstallation file"),
     2102: _("""
     Autoinstallation tree would not lint, there are packages
     missing in the channel
     """),

     # 3000-3999: XML dumper errors:
     3000: _("Invalid datatype passed"),
     3001: _("Unable to retrieve channel"),
     3002: _("Invalid package name"),
     3003: _("Unable to retrieve package"),
     3004: _("Invalid patch name"),
     3005: _("Unable to retrieve patch"),
     3006: _("Invalid SUSE Manager certificate"),
     3007: _("File is missing"),
     3008: _("Function retrieval error"),
     3009: _("Function execution error"),
     3010: _("Missing version string"),
     3011: _("Invalid version string"),
     3012: _("Mismatching versions"),
     3013: _("Invalid channel version"),
     3014: _("Missing snapshot for channels"),
     3015: _("No comps file for channel"),
     3016: _("Unable to retrieve comps file"),

     # 4000 - 4999: config management errors
     4002: _("Configuration action missing"),
     4003: _("File too large"),
     4004: _("File contains binary data"),
     4005: _("Configuration channel is not empty"),
     4006: _("Permission error"),
     4007: _("Content missing for configuration file"),
     4008: _("Template delimiters not specified"),
     4009: _("Configuration channel does not exist"),
     4010: _("Configuration channel already exists"),
     4011: _("File missing from configuration channel"),
     4012: _("Different revision of this file is uploaded"),
     4013: _("File already uploaded to configuration channel"),
     4014: _("File size exceeds remaining quota space"),
     4015: _("Full path of file must be specified"),
     4016: _("Invalid revision number"),
     4017: _("Cannot compare files of different file type"),

     # 5000 - 5099: entitlement mapper errors
     5000: _("The speicified item is not present in the input"),
     5001: _("Invalid item code"),
     5002: _("Invalid user role"),
     5003: _("Invalid server group"),
     5004: _("Invalid channel family"),
    }


class rhnException(Exception):
    """
    This is the generic exception class we raise in the code when we want to
    abort program execution and send a "500 Internal Server Error" message back
    to the client.
    """

    def __init__(self, *args):
        Exception.__init__(self, *args)
        self.args = args

    def __repr__(self):
        """
        String representation of this object.
        """
        s = StringIO()
        s.write("\nInternal SUSE Manager code error. Information available:\n")
        for a in self.args:
            s.write("  %s\n" % (a, ))

        return s.getvalue()


class redirectException(Exception):
    """
    pkilambi:This is the exception class we raise when we decide to
    issue a redirect functions in apacheRequest will catch it and
    transform it into a redirect path string
    """

    def __init__(self, redirectpath = ""):
        Exception.__init__(self)
        self.path = redirectpath

    def __str__(self):
        """
        Object in string format.
        """
        return repr(self.path)


Explain = _("""
     An error has occurred while processing your request. If this problem
     persists please enter a bug report at bugzilla.novell.com.
     If you choose to submit the bug report, please be sure to include
     details of what you were trying to do when this error occurred and
     details on how to reproduce this problem.
""")


class rhnFault(Exception):
    """
    This is a data exception class that is raised when we detect bad data.
    The higher level functions in apacheServer will catch it and transform it
    into an XMLRPC fault message that gets passed back to the client without
    aborting the current execution of the process (well, we abort, but we don't
    mail a traceback because this is the type of error we can handle - think
    user authentication).
    """

    def __init__(self, err_code = 0, err_text = "", explain = 1):
        self.code = err_code
        self.text = err_text
        self.explain = explain
        self.arrayText = ''
        if self.code and FaultArray.has_key(self.code):
            self.arrayText = FaultArray[self.code]
        Exception.__init__(self, self.code, self.text, self.arrayText)

    def __repr__(self):
        """
        String representation of this object.
        """
        return "<rhnFault class (code = %s, text = '%s')>" % (self.code,
                                                              self.text)

    def getxml(self):

        # see if there were any template strings loaded from the db,
        # {label:value}
        templateOverrides = rhnFlags.get('templateOverrides')

        # update the templateValues in the module
        if templateOverrides:
            for label in templateOverrides.keys():
                # only care about values we've defined defaults for...
                if templateValues.has_key(label):
                    templateValues[label] = templateOverrides[label]

        s = StringIO()
        s.write("\n")
        if self.text:
            s.write(_("Error Message:\n    %s\n") % self.text.strip())
        if self.code:
            s.write(_("Error Class Code: %s\n") % self.code)
        if self.arrayText:
            cinfo = self.arrayText % templateValues
            s.write(_("Error Class Info: %s\n") % cinfo.rstrip())
        if self.explain:
            s.write(_("Explanation: %s") % Explain)
        if not self.code:
            return xmlrpclib.Fault(1, s.getvalue())
        return xmlrpclib.Fault(-self.code, s.getvalue())

class rhnNotFound(Exception):
    """ Raised when we want return 404 Not Found """
    pass

if __name__ == "__main__":
    print "You can not run this module by itself"
    sys.exit(-1)
