#
# Copyright (c) 2008--2011 Red Hat, Inc.
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

package RHN::SatInstall;

use strict;

use File::Spec;
use Frontier::Client;

use English;
use POSIX qw/dup2 setsid O_WRONLY O_CREAT/;
use ModPerl::Util qw/exit/;
use DateTime;
use IPC::Open3;

use RHN::DB;
use Params::Validate;
Params::Validate::validation_options(strip_leading => "-");

use RHN::Exception qw/throw/;

use RHN::DB::SatInstall;

use RHN::SatelliteCert;

our @ISA = qw/RHN::DB::SatInstall/;

use constant DEFAULT_RHN_CERT_LOCATION =>
  '/etc/sysconfig/rhn/rhn-entitlement-cert.xml';

use constant DEFAULT_RHN_CONF_LOCATION =>
  '/etc/rhn/rhn.conf';

use constant DEFAULT_RHN_ETC_DIR =>
  '/etc/sysconfig/rhn';

use constant DEFAULT_DB_POP_LOG_FILE =>
  '/var/log/rhn/populate_db.log';

use constant DEFAULT_CA_CERT_NAME =>
  'RHN-ORG-TRUSTED-SSL-CERT';

use constant DB_POP_LOG_SIZE => 154000;

# Some utility functions to do the configuration steps needed for the
# satellite install.

sub write_config {
  my $class = shift;
  my $options = shift;
  my $target = shift || DEFAULT_RHN_CONF_LOCATION;

  my @opt_strings = map { "--option=${_}=" . $options->{$_} } keys %{$options};

  my $ret = system("/usr/bin/sudo", "/usr/bin/rhn-config-satellite.pl",
		   "--target=$target", @opt_strings);

  if ($ret) {
    throw 'There was a problem updating your configuration.  '
      . 'See the webserver error log for details.';
  }

  return;
}

my %server_cert_opts = (
   dir => 1,
   password => 1,
   'set-country' => 1,
   'set-state' => 1,
   'set-city' => 1,
   'set-org' => 1,
   'set-org-unit' => 1,
   'cert-expiration' => 1,
   'set-email' => 1,
   'set-hostname' => 1,
);

sub generate_server_cert {
  my $class = shift;
  my %params = validate(@_, {
   %server_cert_opts,
			    });

  $params{'cert-expiration'} *= 365;

  my @opts = "--gen-server";

  foreach my $name (keys %params) {
    next unless ($params{$name}
		 and exists $server_cert_opts{$name});

    push @opts, qq(--$name=$params{$name});
  }

  my @command = ('/usr/bin/rhn-sudo-ssl-tool',  @opts, '-q');

  my $pid = open3(undef, ">&STDERR", ">&STDERR", @command);
  waitpid( $pid, 0 );
  my $ret = $?;

  return $ret;
}

1;
