%if 0%{?suse_version}
%define apache_user wwwrun
%define apache_group www
%define misc_path /srv/
%else
%define apache_user apache
%define apache_group apache
%define misc_path %{_var}
%endif

Name:           spacewalk-setup
Version:        1.6.3
Release:        1%{?dist}
Summary:        Initial setup tools for Red Hat Spacewalk

Group:          Applications/System
License:        GPLv2
URL:            http://spacewalk.redhat.com
Source0:        %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker)
## non-core
#BuildRequires:  perl(Getopt::Long), perl(Pod::Usage)
#BuildRequires:  perl(Test::Pod::Coverage), perl(Test::Pod)

BuildArch:      noarch
Requires:       perl
Requires:       perl-Params-Validate
Requires:       spacewalk-schema
%if 0%{?suse_version}
Requires:       curl
Requires:       policycoreutils
Requires:       perl-Mail-RFC822-Address
Requires:       perl-XML-LibXML perl-XML-SAX perl-DateTime
Requires:       perl-Frontier-RPC
Requires:       perl-libwww-perl
Requires:       perl-Net-LibIDN
Requires:       patch
BuildRequires:       perl-libwww-perl
%else
Requires:       /sbin/restorecon
%endif
Requires:       spacewalk-admin
Requires:       spacewalk-certs-tools
Requires:       perl-Satcon
Requires:       spacewalk-backend-tools
Requires:       cobbler >= 2.0.0
Requires:       PyYAML
Requires:       /usr/bin/gpg
Requires:       spacewalk-setup-jabberd

%description
A collection of post-installation scripts for managing Spacewalk's initial
setup tasks, re-installation, and upgrades.

%prep
%setup -q

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w %{buildroot}/*
install -d -m 755 %{buildroot}/%{_datadir}/spacewalk/setup/
install -m 0755 share/embedded_diskspace_check.py %{buildroot}/%{_datadir}/spacewalk/setup/
install -m 0644 share/sudoers.base %{buildroot}/%{_datadir}/spacewalk/setup/
install -m 0644 share/sudoers.clear %{buildroot}/%{_datadir}/spacewalk/setup/
install -m 0644 share/sudoers.1 %{buildroot}/%{_datadir}/spacewalk/setup/
install -m 0644 share/sudoers.2 %{buildroot}/%{_datadir}/spacewalk/setup/
install -m 0644 share/sudoers.3 %{buildroot}/%{_datadir}/spacewalk/setup/
install -m 0644 share/ssl.conf.1 %{buildroot}/%{_datadir}/spacewalk/setup/
install -m 0644 share/ssl.conf.2 %{buildroot}/%{_datadir}/spacewalk/setup/
install -m 0644 share/ssl.conf.3 %{buildroot}/%{_datadir}/spacewalk/setup/
install -m 0644 share/ssl.conf.4 %{buildroot}/%{_datadir}/spacewalk/setup/
install -m 0644 share/ssl.conf.5 %{buildroot}/%{_datadir}/spacewalk/setup/
install -m 0644 share/ssl.conf.6 %{buildroot}/%{_datadir}/spacewalk/setup/
install -m 0644 share/ssl.conf.7 %{buildroot}/%{_datadir}/spacewalk/setup/
install -m 0644 share/ssl.conf.8 %{buildroot}/%{_datadir}/spacewalk/setup/
install -m 0644 share/tomcatX.conf.1 %{buildroot}/%{_datadir}/spacewalk/setup/
install -m 0644 share/tomcatX.conf.2 %{buildroot}/%{_datadir}/spacewalk/setup/
install -m 0644 share/tomcatX.conf.3 %{buildroot}/%{_datadir}/spacewalk/setup/
install -m 0644 share/server.xml.xsl %{buildroot}/%{_datadir}/spacewalk/setup/
install -m 0644 share/context.xml.xsl %{buildroot}/%{_datadir}/spacewalk/setup/
install -m 0644 share/web.xml.patch %{buildroot}/%{_datadir}/spacewalk/setup/
install -m 0644 share/old-jvm-list %{buildroot}/%{_datadir}/spacewalk/setup/
install -d -m 755 %{buildroot}/%{_datadir}/spacewalk/setup/defaults.d/
install -d -m 755 %{buildroot}/%{_datadir}/spacewalk/setup/upgrade
install -m 0755 share/upgrade/* %{buildroot}/%{_datadir}/spacewalk/setup/upgrade
install -m 0644 share/defaults.d/defaults.conf %{buildroot}/%{_datadir}/spacewalk/setup/defaults.d/

# Oracle specific stuff, possible candidate for sub-package down the road:
install -d -m 755 %{buildroot}/%{_datadir}/spacewalk/setup/oracle/
install -m 0755 share/oracle/install-db.sh %{buildroot}/%{_datadir}/spacewalk/setup/oracle
install -m 0755 share/oracle/remove-db.sh %{buildroot}/%{_datadir}/spacewalk/setup/oracle
install -m 0755 share/oracle/upgrade-db.sh %{buildroot}/%{_datadir}/spacewalk/setup/oracle

# create a directory for misc. Spacewalk things
install -d -m 755 %{buildroot}/%{misc_path}/spacewalk

mkdir -p $RPM_BUILD_ROOT%{_mandir}/man8
/usr/bin/pod2man --section=8 $RPM_BUILD_ROOT/%{_bindir}/spacewalk-make-mount-points | gzip > $RPM_BUILD_ROOT%{_mandir}/man8/spacewalk-make-mount-points.8.gz

%check
make test


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc Changes README answers.txt
%{perl_vendorlib}/*
%{_bindir}/spacewalk-setup
%{_bindir}/spacewalk-make-mount-points
%{_bindir}/cobbler-setup
%{_mandir}/man[13]/*.[13]*
%dir %{_datadir}/spacewalk
%{_datadir}/spacewalk/*
%attr(755, %{apache_user}, root) %{misc_path}/spacewalk
%{_mandir}/man8/spacewalk-make-mount-points*

%changelog
* Thu Dec 08 2011 Miroslav Suchý 1.6.3-1
- code cleanup - rhn-load-ssl-cert and rhn-sudo-load-ssl-cert are not needed
  anymore

* Fri Nov 04 2011 Milan Zazrivec <mzazrivec@redhat.com> 1.6.2-1
- 679335 - remove osa-dispatcher login credentials from rhn.conf

* Fri Oct 07 2011 Milan Zazrivec <mzazrivec@redhat.com> 1.6.1-1
- 715271 - define AJP connector on [::1]:8009

* Tue Jul 19 2011 Jan Pazdziora 1.5.11-1
- Updating the copyright years.

* Tue Jul 19 2011 Jan Pazdziora 1.5.10-1
- We kinda need the use Spacewalk::Setup if we plan to call functions from it.

* Mon Jul 18 2011 Jan Pazdziora 1.5.9-1
- Fireworks for the spinning pattern.
- add man page for spacewalk-make-mount-points (msuchy@redhat.com)
- remove macro from changelog (msuchy@redhat.com)

* Mon Jul 11 2011 Jan Pazdziora 1.5.8-1
- Check for cases when loading of the DBD driver fails (so there is no DBI
  error itself).

* Fri May 27 2011 Jan Pazdziora 1.5.7-1
- 708357 - If the mountpoint is on NFS, set cobbler_use_nfs.

* Mon May 16 2011 Jan Pazdziora 1.5.6-1
- We only want to source the setenv.sh if it exists.

* Wed May 11 2011 Jan Pazdziora 1.5.5-1
- Actually package the new tomcatX.conf.3 (for the tomcat6 setenv.sh issue) in
  the rpm.

* Wed May 04 2011 Jan Pazdziora 1.5.4-1
- On RHEL 6, tomcat6 no longer sources the setenv.sh so we need to source it
  ourselves.

* Wed Apr 27 2011 Simon Lukasik <slukasik@redhat.com> 1.5.3-1
- Drop the schema only if exists (slukasik@redhat.com)

* Fri Apr 15 2011 Jan Pazdziora 1.5.2-1
- redirect upgrade log to correct file (mzazrivec@redhat.com)
- move the m4 template at the end of cmd line parameters (mzazrivec@redhat.com)

* Tue Apr 12 2011 Miroslav Suchý 1.5.1-1
- fix rhnConfig namespace
- suppress warning
- Bumping package versions for 1.5

* Tue Apr 05 2011 Michael Mraka <michael.mraka@redhat.com> 1.4.8-1
- fixed typo in answer file option name

* Fri Apr 01 2011 Jan Pazdziora 1.4.7-1
- 683200 - fixing broken commit 695e8f7a792996b7e51f9fd2b11789d26e625753.

* Fri Apr 01 2011 Jan Pazdziora 1.4.6-1
- 683200 - fix more syntax errors.

* Thu Mar 31 2011 Miroslav Suchý 1.4.5-1
- 683200 - fix syntax error

* Wed Mar 30 2011 Michael Mraka <michael.mraka@redhat.com> 1.4.4-1
- fixed missing output redirection
- oracle_sqlplus_t is not able to write to logs

* Wed Mar 30 2011 Miroslav Suchý <msuchy@redhat.com> 1.4.3-1
- 683200 - convert db-host from IDN to ascii

* Mon Mar 07 2011 Jan Pazdziora 1.4.2-1
- Removing rhn-enable-push.pl as it is not referenced from anywhere.
- Removing rhn-load-config.pl as it is not referenced from anywhere.

* Fri Feb 18 2011 Jan Pazdziora 1.4.1-1
- Localize globs used for filehandles; use three-parameter opens.

* Wed Jan 26 2011 Jan Pazdziora 1.3.10-1
- PostgreSQL start/stop is no longer handled by spacewalk-service, neither is
  Oracle XE.
- Make all system_debug invocations multiparameter.

* Tue Jan 25 2011 Michael Mraka <michael.mraka@redhat.com> 1.3.9-1
- 636458 - reuse db version check via dbms_utility.db_version()
- updating Copyright years for year 2011

* Wed Jan 19 2011 Jan Pazdziora 1.3.8-1
- Call spacewalk-sql instead of rhn-populate-database.pl.

* Tue Jan 18 2011 Jan Pazdziora 1.3.7-1
- The db-sid is long gone, using db-name now.
- As db-protocol is no longer processed (supported), removing.
- Refactored oracle_get_database_answers.
- Creating empty file is not that useful, dropping.

* Tue Jan 11 2011 Tomas Lestach <tlestach@redhat.com> 1.3.6-1
- replace any LD_LIBRARY_PATH by given content (tlestach@redhat.com)
- Removing Oracle-ism from postgresql_populate_db. (jpazdziora@redhat.com)
- The installation on PostgreSQL is now supported. (jpazdziora@redhat.com)
- Removing code which was commented out since 2009. (jpazdziora@redhat.com)
- All three invocations of write_config in spacewalk-setup specify the target,
  no need to have the default. (jpazdziora@redhat.com)

* Fri Jan 07 2011 Jan Pazdziora 1.3.5-1
- Setup InstantClient 11 path for tomcat.

* Sun Dec 26 2010 Jan Pazdziora 1.3.4-1
- 665693: convert sysdate to current_timestamp (colin.coe@gmail.com)

* Thu Dec 23 2010 Jan Pazdziora 1.3.3-1
- The rhn_package package (schema in PostgreSQL) is now gone.

* Thu Dec 16 2010 Jan Pazdziora 1.3.2-1
- 636458 - check that the Oracle database instance is version 10 or 11.

* Mon Dec 13 2010 Jan Pazdziora 1.3.1-1
- 640971 - when waiting for tomcat, try to connect directly to 8009.
- We need to check the return value of GetOptions and die if the parameters
  were not correct.

* Fri Nov 05 2010 Miroslav Suchý <msuchy@redhat.com> 1.2.16-1
- 491331 - move /etc/sysconfig/rhn-satellite-prep to /var/lib/rhn/rhn-
  satellite-prep (msuchy@redhat.com)

* Tue Nov 02 2010 Jan Pazdziora 1.2.15-1
- Update copyright years in the rest of the repo.

* Fri Oct 29 2010 Miroslav Suchý <msuchy@redhat.com> 1.2.14-1
- change ascii art animation to bow, arrow and target

* Tue Oct 26 2010 Jan Pazdziora 1.2.13-1
- When run with the --db-only option, stop after populating the database.

* Fri Oct 22 2010 Miroslav Suchý <msuchy@redhat.com> 1.2.12-1
- 612581 - use new spacewalk namespace for spacewalk-setup

* Fri Oct 15 2010 Jan Pazdziora 1.2.11-1
- Revert "avoid people install packages for different os"
- Revert "valid require format is name = version"

* Thu Oct 14 2010 Michael Mraka <michael.mraka@redhat.com> 1.2.10-1
- avoid people install packages for different os

* Tue Oct 12 2010 Jan Pazdziora 1.2.9-1
- Move the cobbler requirement to version 2.0.0.

* Mon Oct 11 2010 Jan Pazdziora 1.2.8-1
- Do not require perl-DBD-Pg in spacewalk-setup, save it for spacewalk-
  postgresql.

* Mon Sep 27 2010 Miroslav Suchý <msuchy@redhat.com> 1.2.7-1
- do not restart whole satellite when enabling monitoring
  (mzazrivec@redhat.com)
- use bind variables (mzazrivec@redhat.com)
- don't use RHN::Utils in spacewalk-setup (mzazrivec@redhat.com)
- need_oracle_9i_10g_upgrade is no longer needed (mzazrivec@redhat.com)
- unify embedded database upgrades (mzazrivec@redhat.com)
- use standard perl dbi in update_monitoring_scout (mzazrivec@redhat.com)

* Tue Sep 14 2010 Milan Zazrivec <mzazrivec@redhat.com> 1.2.6-1
- re-link /etc/smrsh/ack_enqueuer.pl during upgrade
- update monitoring scout setup directly by spacewalk-setup
- added --external-db option to installer

* Wed Sep 01 2010 Jan Pazdziora 1.2.5-1
- 594513 - only listen on localhost (connectors at 8080 and 8009).
- 531719 - fixing cobbler setup to set pxe_just_once (jsherril@redhat.com)

* Thu Aug 26 2010 Justin Sherrill <jsherril@redhat.com> 1.2.4-1
- small fix for broken perl code (jsherril@redhat.com)

* Thu Aug 26 2010 Justin Sherrill <jsherril@redhat.com> 1.2.3-1
- making patch command silent (jsherril@redhat.com)
- 533527 - having spacewalk-setup patch the web.xml for tomcat to turn off
  development mode (jsherril@redhat.com)

* Thu Aug 26 2010 Justin Sherrill <jsherril@redhat.com> 1.2.2-1
- 533527 - having spacewalk-setup patch the web.xml for tomcat to turn off
  development mode (jsherril@redhat.com)

* Thu Aug 26 2010 Jan Pazdziora 1.2.1-1
- As we never fork now, the --nofork is obsolete, removing.

* Thu Jul 29 2010 Justin Sherrill <jsherril@redhat.com> 1.1.14-1
- 531719 - making pxe_just_once set to 1 by default on a spacewalk install
  (jsherril@redhat.com)

* Fri Jul 23 2010 Milan Zazrivec <mzazrivec@redhat.com> 1.1.13-1
- db-sid is now db-name

* Fri Jul 23 2010 Michael Mraka <michael.mraka@redhat.com> 1.1.12-1
- renamed db_sid to SID db_name to be consistent with PostgreSQL

* Fri Jul 23 2010 Michael Mraka <michael.mraka@redhat.com> 1.1.11-1
- renamed db_sid to SID db_name to be consistent with PostgreSQL

* Fri Jul 23 2010 Michael Mraka <michael.mraka@redhat.com> 1.1.10-1
- unified database connection information

* Mon Jul 19 2010 Michael Mraka <michael.mraka@redhat.com> 1.1.9-1
- fixed tomcat5.conf pattern

* Wed Jul 14 2010 Michael Mraka <michael.mraka@redhat.com> 1.1.8-1
- let jdbc use network service name

* Wed Jul 14 2010 Michael Mraka <michael.mraka@redhat.com> 1.1.7-1
- tomcat config files should be modified not replaced

* Fri Jul 09 2010 Miroslav Suchý <msuchy@redhat.com> 1.1.6-1
- add example of answers.txt file (msuchy@redhat.com)

* Thu Jul 01 2010 Miroslav Suchý <msuchy@redhat.com> 1.1.5-1
- For local database, we shall use the syntax without slashes. Even if the jdbc
  driver goes via TCP anyway. (jpazdziora@redhat.com)

* Mon Jun 28 2010 Jan Pazdziora 1.1.4-1
- The default_db has username and password in Oracle case, let's make it the
  same for PostgreSQL.
- Some values (db-sid) can be undef, do not pass them to rhn-config-
  satellite.pl.
- Some values (db-sid) can be undef, leading to warnings, there does not need
  to be a host a port, and the default_db is different for PostgreSQL.
- Let's do a slightly better formatting of our terminal output.
- Fix postgresql_clear_db to clear the content of the PostgreSQL database.

* Mon Jun 21 2010 Jan Pazdziora 1.1.3-1
- Minor fixes for PostgreSQL code paths.
- Unused code cleanup.

* Thu Jun 17 2010 Miroslav Suchý <msuchy@redhat.com> 1.1.2-1
- fun aside, swimmer meet shark (msuchy@redhat.com)

* Mon Apr 19 2010 Michael Mraka <michael.mraka@redhat.com> 1.1.1-1
- bumping spec files to 1.1 packages
- Move systemlogs directory out of /var/satellite
- Remove audit review cruft from spacewalk-setup

* Wed Mar 24 2010 Michael Mraka <michael.mraka@redhat.com> 0.9.3-1
- modified spacewalk-setup to use spacewalk-service

* Tue Mar 23 2010 Michael Mraka <michael.mraka@redhat.com> 0.9.2-1
- fixed packaging conflicts

* Fri Mar 19 2010 Michael Mraka <michael.mraka@redhat.com> 0.9.1-1
- let's smile in Spacewalk 0.9
- 566124 - spacewalk-setup-jabberd splited from spacewalk-setup

* Mon Dec  7 2009 Miroslav Suchy <msuchy@redhat.com> 0.8.1-1
- change spinning patter to bowling

* Thu Nov 19 2009 Michael Mraka <michael.mraka@redhat.com> 0.7.7-1
- make installer look more consistent

* Mon Oct 12 2009 Michael Mraka <michael.mraka@redhat.com> 0.7.6-1
- added Oracle 11gR2 to allowed versions
- fixed length of db population progress bar

* Thu Oct 01 2009 Milan Zazrivec <mzazrivec@redhat.com> 0.7.5-1
- 476851 - removal of tables: rhn_db_environment, rhn_environment (msuchy@redhat.com)
- fixed check_users_exist, check_groups_exist - only first user/group was
  checked (michael.mraka@redhat.com)
- spacewalk-setup-jabberd man page fixes (mzazrivec@redhat.com)

* Wed Sep 02 2009 Michael Mraka <michael.mraka@redhat.com> 0.7.4-1
- db-backend is set in idefaults
- 520441 - don't apply ExtUtils::MY->fixin(shift) to perl executables

* Tue Sep 01 2009 Milan Zazrivec <mzazrivec@redhat.com> 0.7.3-1
- spacewalk-setup-jabberd code cleanup
- manual page for spacewalk-setup-jabberd

* Fri Aug 28 2009 Milan Zazrivec <mzazrivec@redhat.com> 0.7.2-1
- add spacewalk-setup-jabberd script (mzazrivec@redhat.com)
- bumping Version to 0.7.0 (jmatthew@redhat.com)
- As /usr/bin/spacewalk-setup calls /usr/bin/gpg, we should Require it.
  (jpazdziora@redhat.com)
- fix missing column name (mzazrivec@redhat.com)

* Thu Aug 06 2009 Milan Zazrivec <mzazrivec@redhat.com> 0.6.20-1
- update spacewalk / satellite monitoring scout ip address

* Wed Aug 05 2009 John Matthews <jmatthew@redhat.com> 0.6.19-1
- 509474 - integration of Joshua's audit feature. (joshua.roys@gtri.gatech.edu)

* Tue Aug 04 2009 Jan Pazdziora 0.6.18-1
- 490668 - add man pages for spacewalk-setup and cobbler-setup

* Mon Aug 03 2009 Jan Pazdziora 0.6.17-1
- No --log option, print_progress does logging for us, sqlplus should print to
  STDOUT/STDERR

* Thu Jul 30 2009 Devan Goodwin <dgoodwin@redhat.com> 0.6.16-1
- Fix spacewalk-setup sudoers setup SHARED_DIR problem.
  (dgoodwin@redhat.com)

* Tue Jul 28 2009 Devan Goodwin <dgoodwin@redhat.com> 0.6.14-1
- Fix rhn.conf population of Hibernate dialect/driver/url settings.
  (dgoodwin@redhat.com)
- Fix spacewalk-setup pgsql changes lost during merges. (dgoodwin@redhat.com)

* Mon Jul 27 2009 Devan Goodwin <dgoodwin@redhat.com> 0.6.12-1
- Fix PostgreSQL clearing of the DB during setup. (dgoodwin@redhat.com)
- Populate Hibernate settings in rhn.conf for both Oracle and PostgreSQL.
  (dgoodwin@redhat.com)
- Prep perl stack for PostgreSQL connections. (dgoodwin@redhat.com)
- Fully qualify spacewalk-setup calls to satcon_deploy. (dgoodwin@redhat.com)
- Fix spacewalk-setup query to work with Oracle + PostgreSQL.
  (dgoodwin@redhat.com)
- Stop printing charset during setup. (dgoodwin@redhat.com)
- Fix Oracle rhn-populate-db.pl issue. (dgoodwin@redhat.com)
- Support setup --clear-db option for PostgreSQL. (dgoodwin@redhat.com)
- Check if schema already exists during setup. (dgoodwin@redhat.com)
- Update spacewalk-setup to deploy new PostgreSQL schema layout.
  (dgoodwin@redhat.com)

* Mon Jul 27 2009 John Matthews <jmatthew@redhat.com> 0.6.11-1
- 508187 - Fix jabberd configs on x86_64. (dgoodwin@redhat.com)

* Tue Jul 21 2009 John Matthews <jmatthew@redhat.com> 0.6.10-1
- rhn-load-config.pl - remove accidental 's' (bbuckingham@redhat.com)
- 511100 - Fixed upgrade scripts to include cobbler.host (paji@redhat.com)
- 511052 - script to fix rhn_sat_node, rhn_sat_cluster (mzazrivec@redhat.com)

* Thu Jun 25 2009 Milan Zazrivec <mzazrivec@redhat.com> 0.6.9-1
- no in-place editing of /etc/oratab under oracle user (mzazrivec@redhat.com)
- remove extraneous backslash characters (mzazrivec@redhat.com)
- update records in /etc/oratab in db upgrade scripts (mzazrivec@redhat.com)
- 507338 - Fixed a spacewalk setup glitch where we not checkking for a null
  value.. (paji@redhat.com)
- support for db upgrade with custom user set (mzazrivec@redhat.com)
- set new embedded db oratab entry only if it does not exist
  (mzazrivec@redhat.com)
- restart the satellite using shell script (mzazrivec@redhat.com)
- Do not start embedded db during upgrade (mzazrivec@redhat.com)
- 506405 - fixed cobbler-setup for non-interactive installs (paji@redhat.com)
- 499889 - Modified cobbler-setup to turn on tftp and xinetd (paji@redhat.com)

* Fri Jun 05 2009 jesus m. rodriguez <jesusr@redhat.com> 0.6.8-1
- no need to enable Monitoring + MonitoringScout explicitly (mzazrivec@redhat.com)
- Fixes to support mod_jk >= 2.2.26. (dgoodwin@redhat.com)
- distinguish minor and major version embedded db upgrades (mzazrivec@redhat.com)
- include new embedded db upgrade script into spec file (mzazrivec@redhat.com)
- add 10g 10.2.0.3 -> 10.2.0.4 embedded db setup upgrade script (mzazrivec@redhat.com)
- pass custom sid to upgrade-db.sh for embedded db upgrade (mzazrivec@redhat.com)
- update copyright information (mzazrivec@redhat.com)
- support embedded db upgrade with custom sid (mzazrivec@redhat.com)
- 502475 - remove initialization of scout from perl (msuchy@redhat.com)
- 502475 - add ip address to SatCluster and SatNode (msuchy@redhat.com)
- restart satellite using shell script (mzazrivec@redhat.com)
- 464189 - embedded db upgrade fixes from Goldmember (mmraka@redhat.com)
- set compatible flag to 10.2 during embedded db upgrade (mzazrivec@redhat.com)

* Wed May 27 2009 Jan Pazdziora 0.6.7-1
- spacewalk-setup: move creation of mount points to
  /usr/bin/spacewalk-make-mount-points

* Tue May 26 2009 Devan Goodwin <dgoodwin@redhat.com> 0.6.6-1
- 500688 - Clarify --run-updater help info in spacewalk-setup.
  (dgoodwin@redhat.com)

* Thu May 21 2009 jesus m. rodriguez <jesusr@redhat.com> 0.6.5-1
- 499901 - made cobbler sync run along with cobbler setup (paji@redhat.com)
- Make SELinux documentation in Spacewalk::Setup more up-to-date. (jpazdziora@redhat.com)
- Bump up version in Spacewalk/Setup.pm. (jpazdziora@redhat.com)

* Wed May 06 2009 jesus m. rodriguez <jesusr@redhat.com> 0.6.4-1
- no need to enable notification anymore (mzazrivec@redhat.com)

* Fri Apr 17 2009 Devan Goodwin <dgoodwin@redhat.com> 0.6.3-1
- 493466 - perl scripts from rhn-upgrade moved to spacewalk-setup
  (mzazrivec@redhat.com)
- 493466 - add scripts from rhn-upgrade to spacewalk-setup
  (mzazrivec@redhat.com)
- 466577 - add bouncycastle* to the list of obsoleted java packages
  (mzazrivec@redhat.com)
- 466577 - list of jvms from older Satellites (mzazrivec@redhat.com)
- 466577 - support for removing old jvms during upgrade (mzazrivec@redhat.com)

* Wed Apr 15 2009 Devan Goodwin <dgoodwin@redhat.com> 0.6.2-1
- Added syntax check to the setup to add cobbler.host to rhn.conf if it's
  not present (paji@redhat.com)
- 208440 - call install-db.sh with custom creation parameters
  (mzazrivec@redhat.com)
- 208440 - install-db.sh: support for creating embedded db with custom
  parameters (mzazrivec@redhat.com)
- Removing the last bastions of conditional cobbler 1.4 code 
  (paji@redhat.com)

 * Mon Apr  6 2009 Partha Aji <paji@redhat.com> 0.6.1-1
 - moved the cobbler requirement to 1.6.3 or greater as required by sat. 

* Mon Apr 06 2009 Miroslav Suchý <msuchy@redhat.com> 0.6.1-1
- replace snail with worm (msuchy@redhat.com)
- 391771 - removing usermod from install-db.sh, we should do it in %%pre of some
  rpm. (jpazdziora@redhat.com)
- bump Versions to 0.6.0 (jesusr@redhat.com)
- 469413 - included build number to the installation log file
  (tlestach@redhat.com)

* Fri Mar 27 2009 Jan Pazdziora 0.5.27-1
- 492194 - address spacewalk-setup hanging while Restarting services.

* Thu Mar 26 2009 Milan Zazrivec <mzazrivec@redhat.com> 0.5.26-1
- update message at the end of upgrade setup

* Wed Mar 25 2009 Milan Zazrivec <mzazrivec@redhat.com> 0.5.25-1
- 491091 - don't match lines in ssl.conf that are commented out

* Tue Mar 24 2009 Dennis Gilmore <dennis@ausil.us> 0.5.24-1
- write jabberd server.pem to /etc/pki/spacewalk/jabberd

* Wed Mar 18 2009 Mike McCune <mmccune@gmail.com> 0.5.23-1
- 486186 - Update spacewalk spec files to require cobbler >= 1.4.3

* Fri Mar 13 2009 jesus m. rodriguez <jesusr@redhat.com> 0.5.22-1
- run setup_monitoring even for upgrades

* Thu Mar 12 2009 jesus m. rodriguez <jesusr@redhat.com> 0.5.21-1
- rebuild

* Thu Mar 12 2009 Partha Aji <paji@redhat.com>
- None - cobbler-setup now requires PyYAML. So adding it..

* Thu Mar 12 2009 Miroslav Suchy <msuchy@redhat.com> 0.5.20-1
- 489350 - if scout already exist, dont create it again if db was not wiped

* Tue Mar 10 2009 Milan Zazrivec <mzazrivec@redhat.com> 0.5.19-1
- 488092 - moved some routines to Setup.pm so they can be used from outside
- call satcon_deploy with full path to Spacewalk::Setup

* Wed Mar  4 2009 Milan Zazrivec <mzazrivec@redhat.com> 0.5.17-1
- ssl virtual host setup modifies existing ssl.conf

* Fri Feb 27 2009 jesus m. rodriguez <jesusr@redhat.com> 0.5.16-1
- 486054 - add configuration variable to list of overrides.

* Thu Feb 26 2009 jesus m. rodriguez <jesusr@redhat.com> 0.5.15-1
- 486560 -  Installer is unable to restart database during 500 -> 530 upgrade

* Wed Feb 18 2009 Dave Parker <dparker@redhat.com> 0.5.14-1
- 486186 - Update spacewalk spec files to require cobbler >= 1.4.2

* Tue Feb 17 2009 Jan Pazdziora 0.5.13-1
- 472914 - restructure the setup_sudoers function,
  split sudoers.rhn to three definition files, add sudoers.clear,
  merge INSTALL_RHN and CONFIG_RHN in sudoers; the INSTALL_RHN section
  is no longer needed
- 484718 - remove /usr/sbin/rhnreg_ks from sudoers
- 484717 - remove /usr/bin/rhn-ssl-dbstore from sudoers
- 484709 - remove /usr/bin/satellite-sync from sudoers
- 484705 - remove /usr/bin/satcon-deploy-tree.pl from sudoers
- 484703 - remove /usr/bin/satcon-build-dictionary.pl from sudoers
- 484702 - remove /usr/bin/rhn-generate-pem.pl from sudoers
- 484701 - remove /usr/bin/rhn-deploy-ca-cert.pl from sudoers
- 484685 - remove /usr/bin/rhn-install-ssl-cert.pl from sudoers
- 484681 - remove /usr/bin/rhn-config-schema.pl from sudoers
- 484699 - remove /usr/bin/rhn-populate-database.pl from sudoers
- 484680 - remove /usr/bin/rhn-config-tnsnames.pl from sudoers

* Mon Feb 16 2009 Dave Parker <dparker@redhat.com> 0.5.12-1
-  Bug 483102 - Need answer file setting for installer question "Should setup configure apache's default ssl server for you"

* Thu Feb 12 2009 Miroslav Suchý <msuchy@redhat.com> 0.5.11-1
- 484713, 484720 - fix sudoers

* Thu Feb 12 2009 Jan Pazdziora 0.5.10-1
- 484675 - /usr/bin/spacewalk-setup: run restorecon silently

* Tue Feb 10 2009 Jan Pazdziora 0.5.9-1
- spacewalk-setup: use DEFAULT_SATCON_DICT
- spacewalk-setup: use the local write_config function

* Thu Feb 05 2009 Devan Goodwin <dgoodwin@redhat.com> 0.5.8-1
- Add support for overlay of default_mail_from setting in rhn.conf.

* Wed Feb  4 2009 Jan Pazdziora 0.5.7-1
- only run restorecon and setsebool on RHEL 5+ and with SELinux enabled
- run create-db.sh with --run-restorecon on RHEL 5+ and with SELinux enabled
- replace "!#/usr/bin/env python" with "!#/usr/bin/python" (Miroslav S.)

* Fri Jan 30 2009 Jan Pazdziora 0.5.6-1
- run restorecon on populate_db.log

* Thu Jan 29 2009 Jan Pazdziora 0.5.5-1
- numerous changes to support clean embedded database installation
- avoid fully qualifying objects with Spacewalk::Setup::
- Spacewalk::Setup: avoid using literal for INSTALL_LOG_FILE.

* Fri Jan 23 2009 Milan Zazrivec 0.5.4-1
- re-enable satellite upgrades

* Wed Jan 21 2009 Michael Mraka <michael.mraka@redhat.com> 0.5.3-1
- fixed branding stuff

* Mon Jan 19 2009 Jan Pazdziora 0.5.2-1
- fix path in Makefile

* Mon Jan 19 2009 Jan Pazdziora 0.5.1-1
- rebuilt for 0.5, after repository reorg

* Thu Jan 15 2009 Milan Zazrivec 0.4.23-1
- upgrade setup fixes

* Wed Jan 14 2009 Jan Pazdziora 0.4.22-1
- 479971 - require jabberd so that the jabberd user exists.

* Tue Jan 13 2009 Devan Goodwin <dgoodwin@redhat.com> 0.4.21-1
- 477492 - Remove "assuming Oracle" message from spacewalk-setup.

* Thu Jan  8 2009 Jan Pazdziora 0.4.20-1
- support symlinked and NFS-mounted /var/satellite during setup
- run chkconfig for "stock" httpd

* Thu Jan  8 2009 Milan Zazrivec 0.4.19-1
- Build for Spacewalk 0.4

* Mon Dec 22 2008 Mike McCune <mmccune@gmail.com> 0.4.18-1
- Adding cobbler requirement

* Mon Dec 22 2008 Michael Mraka <michael.mraka@redhat.com> 0.4.17-1
- changed defaults.conf to default.d/*
- moved spacewalk-public.cert to spacewalk-branding
- resolved #477490, #477493

* Fri Dec 19 2008 Dave Parker <dparker@redhat.com> 0.4.10-1
- added apache default ssl server config generation to spacewalk-setup

* Thu Dec 18 2008 Jan Pazdziora 0.4.11-1
- fixing duplicated $sth variable

* Wed Dec 17 2008 Miroslav Suchý <msuchy@redhat.com> 0.4.10-1
- 226915 - db_name can be different from db instance name

* Tue Dec 16 2008 Partha Aji <paji@redhat.com> 0.4.10-1
- added the cobbler setup module to build the spacewalk rpm.

* Thu Dec 11 2008 Michael Mraka <michael.mraka@redhat.com> 0.4.9-1
- resolved #471225 - moved /sbin stuff to /usr/sbin

* Wed Dec  3 2008 Milan Zazrivec 0.4.7-1
- updated fix for bz #473438

* Fri Nov 28 2008 Miroslav Suchý <msuchy@redhat.com> 0.4.6-1
- 473438 - inititate db alias

* Thu Nov 27 2008 Michael Mraka <michael.mraka@redhat.com> 0.4.5-1
- resolved #473082 - fixed sql query 
- resolved #472378 - set autostart flag on rhnsat entry

* Thu Nov 20 2008 Jan Pazdziora 0.4.3-1
- use full path to usermod
- check if we are on Red Hat Enterprise Linux before using its key
- run restorecon on Spacewalk::Setup::INSTALL_LOG_FILE

* Tue Nov 18 2008 Miroslav Suchý <msuchy@redhat.com> 0.4.2-1
- enable Monitoring services (#471220)

* Thu Oct 30 2008 Michael Mraka <michael.mraka@redhat.com> 0.4.1-1
- resolved #455421

* Tue Oct 21 2008 Michael Mraka <michael.mraka@redhat.com> 0.3.6-1
- resolves #467877 - use runuser instead of su

* Tue Oct 21 2008 Devan Goodwin <dgoodwin@redhat.com> 0.3.5-1
- Remove dependency on spacewalk-dobby. (only needed for embedded Oracle installations)

* Tue Oct 21 2008 Michael Mraka <michael.mraka@redhat.com> 0.3.4-1
- resolves #467717 - fixed sysvinit scripts

* Mon Sep 22 2008 Devan Goodwin <dgoodwin@redhat.com> 0.3.3-1
- Remove explicit chmod/chown on /var/log/rhn/.

* Thu Sep 18 2008 Devan Goodwin <dgoodwin@redhat.com> 0.3.2-1
- Fix bug with /var/log/rhn/ permissions.

* Wed Sep  3 2008 Milan Zazrivec <mzazrivec@redhat.com> 0.2.4-1
- include correct namespace when invoking system_debug()
- build-require perl(ExtUtils::MakeMaker) rather than package name

* Fri Aug 22 2008 Mike McCune <mmccune@redhat.com 0.2.2-2
- adding BuildRequires perl-ExtUtils-MakeMaker

* Wed Aug 20 2008 Devan Goodwin <dgoodwin@redhat.com> 0.2.2-1
- Updating build for spacewalk 0.2.

* Wed Jun  4 2008 Devan Goodwin <dgoodwin@redhat.com> 0.01-1
- Initial packaging.

