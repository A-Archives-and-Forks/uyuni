package NOCpulse::Notif::AlertDB;

use strict;

use Class::MethodMaker
  new_hash_init => 'new',
  get_set       => 'dbh',
  hash          => 'statements';

use Data::Dumper;    # for debugging
use DBI;
use NOCpulse::Config;
use RHN::DBI;

use NOCpulse::Log::Logger;
my $Log = NOCpulse::Log::Logger->new(__PACKAGE__);

#############
sub connect {
#############
  my ($self, %paramHash) = @_;

  # Usage:
  # my $adb = new NOCpulse::Notif::AlertDB;
  # $adb->connect ( 'PrintError'=>0, 'RaiseError'=>0, 'AutoCommit'=>0 );

  my $cfg = new NOCpulse::Config;

  my $PrintError = $paramHash{PrintError} || 0;
  my $RaiseError = $paramHash{RaiseError} || 0;
  my $AutoCommit = $paramHash{AutoCommit} || 0;

  # Disconnect prior session, if exists
  if ($self->dbh) {
    $self->disconnect;
  }

  # Open a connection to the DB
  my $dbh = RHN::DBI->connect;

  if ($dbh) {

    # Remember dbh
    $self->dbh($dbh);
    $self->init_statements;
    return (0, "SUCCESS");
  } else {
    return (1, $DBI::errstr);
  }
} ## end sub connect

################
sub disconnect {
################
  my $self = shift;

  # Close the connection to the DB
  if ($self->connected()) {
    my @statements = $self->statements_values;
    foreach (@statements) {
      $_->finish();
    }
  }
  $self->dbh->disconnect if $self->dbh;
} ## end sub disconnect

############
sub commit {
############
  my $self = shift;

  # Commit changes to the database
  if ($self->connected()) {
    $self->dbh->commit || return (1, $self->dbh->errstr);
  } else {
    return (1, "database not connected");
  }
  return (0);
} ## end sub commit

##############
sub rollback {
##############
  my $self = shift;

  # Roll back changes to the database
  if ($self->connected()) {
    $self->dbh->rollback;
  } else {
    return (1, "database not connected");
  }
  return (0);
} ## end sub rollback

###############
sub dbprepare {
###############
  my ($self, $name, $sql_statement) = @_;

  my $errcode   = 0;
  my $errstring = "SUCCESS";
  my $dataref   = [];

  # Make sure we have an open DB handle
  $self->connect() unless ($self->connected());

  # Prepare the statement handle
  my $statement_handle;
  $statement_handle = $self->dbh->prepare($sql_statement);
  if ($statement_handle) {
    $self->statements($name, $statement_handle);
  } else {
    $errcode   = 1;
    $errstring = $DBI::errstr;
    $@         = $errstring;
    $errstring .= ".  Unable to prepare statement handle.";
  }
  return ($errcode, $errstring);
} ## end sub dbprepare

###############
sub dbexecute {
###############

  my ($self, $statement_name, @bindvars) = @_;
  my $errcode   = 0;
  my $errstring = "SUCCESS";
  my $dataref   = [];

  # Make sure we have an open DB handle
  $self->connect() unless ($self->connected());

  # Prepare the statement handle
  my $statement_handle = $self->statements($statement_name);
  if (!$statement_handle) {
    $errcode   = 1;
    $errstring = $DBI::errstr;
    $@         = $errstring;
    $errstring .= ".  Unable to prepare the query named $statement_name.";
    return ($errcode, $errstring);
  }

  # Execute the query
  my $rc;
  $rc = $statement_handle->execute(@bindvars);
  if (!$rc) {
    $errcode   = 1;
    $errstring = $DBI::errstr;
    $@         = $errstring;
    $errstring .= ".  Unable to execute the query named $statement_name, with ";
    $errstring .= join(',', @bindvars);
    print STDERR "$errstring\n";
    return ($errcode, $errstring);
  }

  # Fetch the data, if any

  if ($statement_handle->{NUM_OF_FIELDS}) {
    $dataref = $statement_handle->fetchall_arrayref;
    if ($statement_handle->err) {
      $dataref   = [];
      $errcode   = 1;
      $errstring = $DBI::errstr;
      $@         = $errstring;
      $errstring .= ".  Unable to fetch the data for $statement_name.";
      return ($errcode, $errstring);
    }
  } ## end if ($statement_handle->...

  return ($errcode, $dataref);
} ## end sub dbexecute

#####################
sub init_statements {
#####################
  my $self = shift;

  $self->dbprepare(
    'select_next_redirect_recid',
    "select sequence_nextval('rhn_redirects_recid_seq')
                                 from DUAL"
                  );
  $self->dbprepare(
    'create_redirect',
    "insert into rhn_redirects (
                                   RECID, CUSTOMER_ID, CONTACT_ID, REDIRECT_TYPE,
                                   DESCRIPTION, REASON,
                                   START_DATE,
                                   EXPIRATION,
                                   LAST_UPDATE_USER, LAST_UPDATE_DATE )
                                 values ( ?, ?, ?, ?,
                                   ?, ?,
                                   TO_TIMESTAMP(?, 'MM-DD-YYYY HH24:MI:SS'),
                                   TO_TIMESTAMP(?, 'MM-DD-YYYY HH24:MI:SS'),
                                   ?, current_timestamp)"
                  );
  $self->dbprepare(
    'create_redirect_criterion',
    "insert into rhn_redirect_criteria (
                                   RECID, REDIRECT_ID, MATCH_PARAM, MATCH_VALUE)
                                 select
                                 sequence_nextval('rhn_redirect_crit_recid_seq'),
                                 ?, ?, ?
                                 from DUAL"
                  );
  $self->dbprepare(
    'create_redirect_email_target',
    "insert into rhn_redirect_email_targets (
                                   REDIRECT_ID, EMAIL_ADDRESS)
                                 values ( ?, ?)"
                  );
  $self->dbprepare(
    'delete_redirect',
    "delete from REDIRECTS
                                 where RECID = ?"
                  );
  $self->dbprepare(
    'delete_redirect_criteria',
    "delete from REDIRECT_CRITERIA
                                 where REDIRECT_ID = ?"
                  );
  $self->dbprepare(
    'delete_redirect_email_targets',
    "delete from REDIRECT_EMAIL_TARGETS
                                 where REDIRECT_ID = ?"
                  );
  $self->dbprepare(
    'select_probe_by_recid',
    "select RECID, PROBE_TYPE, DESCRIPTION, CUSTOMER_ID,
               COMMAND_ID, CONTACT_GROUP_ID, NOTIFY_CRITICAL, NOTIFY_WARNING,
               NOTIFY_UNKNOWN, NOTIFY_RECOVERY, NOTIFICATION_INTERVAL_MINUTES,
               CHECK_INTERVAL_MINUTES, RETRY_INTERVAL_MINUTES, MAX_ATTEMPTS,
               LAST_UPDATE_USER, LAST_UPDATE_DATE 
           from probe where recid  = ?"
                  );
  $self->dbprepare(
    'select_command_by_probe_id',
    "select c.recid, c.name, c.description, c.group_name 
      from rhn_command c,
        rhn_probe p
      where p.command_id = c.recid
        and p.recid = ?"
                  );
  $self->dbprepare(
    'select_redirect_type_by_name',
    "select NAME, DESCRIPTION, LONG_NAME
                                 from redirect_types
                                 where NAME = ?"
                  );
  $self->dbprepare(
    'same_host_probes_from_probeid',
"select probe_id from rhn_check_probe where host_id in (select host_id from rhn_check_probe where probe_id = ?)"
  );
  $self->dbprepare('dual', 'select * from dual');
} ## end sub init_statements

###############
sub connected {
###############
  my $self = shift;
  return undef unless $self->dbh;
  my $result = $self->dbh->ping;
  unless ($result) {
    $Log->log(1, "ping error pid $$ not connected to database\n");
  }
  return $result;
} ## end sub connected

1;

__END__

=head1 NAME

NOCpulse::Notif::AlertDB - An interface to the database for the notification system.

=head1 SYNOPSIS

#Create a new AlertDB object
$adb=NOCpulse::Notif::AlertDB->new();

#Connect to the database
$adb->connect();

#Check whether the connection to the database is still good
$boolean=$adb->connected();

#Create a new sql statement and store it by name for future use
$adb->prepare($name,$sql);

#Execute a prepared statement by name
$arrayref=$adb->execute($sql,@bindvars);

#Commit the transaction to the database
$adb->commit();

#Rollback the current transaction on the database
$adb->rollback();

=head1 DESCRIPTION

The C<AlertDB> object provides an interface to the cdfb for retrieving and updating information.  It was
initial designed and created specifically for current alerts data.

=head1 CLASS METHODS

=over 4

=item new ( [%args] )

Create a new object with the supplied arguments, if any.

=back

=head1 METHODS

=over 4

=item commit ( )

Commits the current transaction to the database.

=item connect ( )

Connect to the database using the parameters specified in the /etc/NOCpulse.ini file.

=item connected ( )

Returns a true value if the database connection is up and valid, otherwise returns a false value.o

=item dbexecute ( $name, @bindvars )

Executes a preprepared sql statement by name with a set of values.

=item dbh ( $dbh )

Get or set the DBI database handle.

=item dbprepare ( $name, $sql )

Prepares a sql statement and stores it by name for future use.

=item disconnect ( )

Disconnect the connection from the database.

=item init_statements ( )

Prepare a set of predefined frequently used sql statements.  These are noted below with required bindvars.

- create_redirect ( recid, customer_id, contact_id, redirect_type, description, reason, start_date, expiration, last_update_user )

Create a new redirect record with the specified bindvars.

- create_redirect_criterion ( redirect_id, match_param, match_value )

Create a new redirect criterion record with the specified bindvars.

- create_redirect_email_target ( redirect_id, email_address )

Create a new email address destination for a redirect.

Create an snmp type alert with the specified bindvars.

- delete_redirect (RECID)

Delete the redirect with the specified redirect id.

- delete_redirect_criteria (REDIRECT_ID)

Delete the redirect criteria for the specified redirect id.

- delete_redirect_email_targets (REDIRECT_ID)

Delete the redirect email targets for the specified redirect id.

- dual

blah blah 

- select_next_redirect_recid ( )

Return the next recid in sequence for use in the redirect table.

- select_probe_by_recid ( RECID )

blah blah


=item rollback ( )

Rollback the current transaction in the database.

=back

=head1 BUGS

No known bugs.

=head1 AUTHOR

Karen Jacqmin-Adams <kja@redhat.com>

Last update: $Date: 2005-05-27 20:18:01 $

=head1 SEE ALSO

B<NOCpulse::Notif::Alert>
B<NOCpulse::Notif::Escalator>
B<NOCpulse::Config>
B<DBI>

=cut
