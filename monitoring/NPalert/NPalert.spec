%define install_prefix     %{_var}/lib/notification
%define log_dir            %{_var}/log/notification
%if 0%{?suse_version}
%define httpd_prefix       /srv/www
%define apache_user        wwwrun
%else
%define httpd_prefix       %{_datadir}/nocpulse
%define apache_user        apache
%endif
%define notif_user         nocpulse
%define log_rotate_prefix  %{_sysconfdir}/logrotate.d/

# Package specific stuff
Name:         NPalert
Summary:      NOCpulse notification system
URL:          https://fedorahosted.org/spacewalk
Source0:      https://fedorahosted.org/releases/s/p/spacewalk/%{name}-%{version}.tar.gz
Version:      1.126.26
Release:      1%{?dist}
BuildArch:    noarch
%if 0%{?suse_version}
Requires:     perl = %{perl_version}
Requires:     perl-Error
Requires:     perl-Crypt-GeneratePassword
%else
Requires:     perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
%endif
Group:        Applications/Communications
License:      GPLv2
Requires:     nocpulse-common
%if 0%{?suse_version}
Requires:     smtp_daemon
%else
Requires:     smtpdaemon
%endif
Requires:     SatConfig-general
Buildroot:    %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%if 0%{?suse_version}
BuildRequires: nocpulse-common
%endif

%description
NOCpulse provides application, network, systems and transaction monitoring,
coupled with a comprehensive reporting system including availability,
historical and trending reports in an easy-to-use browser interface.

This package provides NOCpulse notification system.

%prep
%setup -q

%build
#nothing to do here

%install
rm -rf $RPM_BUILD_ROOT

# Create directories
mkdir -p --mode=755 $RPM_BUILD_ROOT%{_sysconfdir}/notification/archive
mkdir -p --mode=755 $RPM_BUILD_ROOT%{_sysconfdir}/notification/generated
mkdir -p --mode=755 $RPM_BUILD_ROOT%{_sysconfdir}/notification/static
mkdir -p --mode=755 $RPM_BUILD_ROOT%{_sysconfdir}/notification/stage/config
mkdir -p --mode=755 $RPM_BUILD_ROOT%{_sysconfdir}/notification
mkdir -p --mode=755 $RPM_BUILD_ROOT%{_sysconfdir}/smrsh
mkdir -p --mode=775 $RPM_BUILD_ROOT%install_prefix/queue/ack_queue
mkdir -p --mode=775 $RPM_BUILD_ROOT%install_prefix/queue/ack_queue/.new
mkdir -p --mode=775 $RPM_BUILD_ROOT%install_prefix/queue/alert_queue
mkdir -p --mode=775 $RPM_BUILD_ROOT%install_prefix/queue/alert_queue/.new
mkdir -p --mode=755 $RPM_BUILD_ROOT%{_bindir}
mkdir -p --mode=755 $RPM_BUILD_ROOT%log_dir
mkdir -p --mode=755 $RPM_BUILD_ROOT%log_dir/archive
mkdir -p --mode=755 $RPM_BUILD_ROOT%log_dir/ticketlog

# Create symlinks
ln -s ../../static                  $RPM_BUILD_ROOT%{_sysconfdir}/notification/stage/config/static
ln -s /usr/bin/ack_enqueuer.pl      $RPM_BUILD_ROOT%{_sysconfdir}/smrsh/ack_enqueuer.pl

# Install the perl modules
mkdir -p $RPM_BUILD_ROOT%{perl_vendorlib}/NOCpulse/Notif
#mkdir -p --mode 755 $RPM_BUILD_ROOT%{perl_vendorlib}/NOCpulse/Notif/test
install -p -m 644 *.pm $RPM_BUILD_ROOT%{perl_vendorlib}/NOCpulse/Notif
#install -m 644 test/*.pm $RPM_BUILD_ROOT%{perl_vendorlib}/NOCpulse/Notif/test

# Install the scripts
install -p -m 755 scripts/* $RPM_BUILD_ROOT%{_bindir}

# Install the config stuff
install -p config/*.ini $RPM_BUILD_ROOT%{_sysconfdir}/notification/static


# Make sure everything is owned by the right user/group and critical dirs
# have the right permissions
chmod 755 $RPM_BUILD_ROOT%install_prefix
chmod -R 755 $RPM_BUILD_ROOT%{_bindir}

# Install the html and cgi scripts
mkdir -p --mode=755 $RPM_BUILD_ROOT%httpd_prefix/htdocs
mkdir -p --mode=755 $RPM_BUILD_ROOT%httpd_prefix/cgi-bin
mkdir -p --mode=755 $RPM_BUILD_ROOT%httpd_prefix/cgi-mod-perl
mkdir -p --mode=755 $RPM_BUILD_ROOT%httpd_prefix/templates

%if 0%{?suse_version}
ln -s %log_dir           $RPM_BUILD_ROOT%httpd_prefix/htdocs/alert_logs
%else
ln -s ../../../../%log_dir           $RPM_BUILD_ROOT%httpd_prefix/htdocs/alert_logs
%endif

install -p -m 755 httpd/cgi-bin/redirmgr.cgi $RPM_BUILD_ROOT%httpd_prefix/cgi-bin/
install -p -m 755 httpd/cgi-mod-perl/*.cgi $RPM_BUILD_ROOT%httpd_prefix/cgi-mod-perl/
install -p -m 644 httpd/html/*.html        $RPM_BUILD_ROOT%httpd_prefix/htdocs/
install -p -m 644 httpd/html/*.css         $RPM_BUILD_ROOT%httpd_prefix/htdocs/
install -p -m 644 httpd/templates/*.html   $RPM_BUILD_ROOT%httpd_prefix/templates/

# Install the cron stuff
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/cron.d/
install -p -m 644 cron/notification        $RPM_BUILD_ROOT%{_sysconfdir}/cron.d/notification

mkdir -p $RPM_BUILD_ROOT%{_mandir}/man3
/usr/bin/pod2man $RPM_BUILD_ROOT/%{_bindir}/monitor-queue | gzip > $RPM_BUILD_ROOT%{_mandir}/man3/monitor-queue.3pm.gz
/usr/bin/pod2man $RPM_BUILD_ROOT/%{_bindir}/queue_remote_check.pl | gzip > $RPM_BUILD_ROOT%{_mandir}/man3/queue_remote_check.pl.3pm.gz

%post
if [ $1 -eq 2 ]; then
  ls /opt/notification/config/generated/* 2>/dev/null | xargs -I file mv file %{_sysconfdir}/notification/generated
  ls /opt/notification/config/static/notif.ini 2>/dev/null | xargs -I file mv file %{_sysconfdir}/notification/static
  ls /opt/notification/var/GenerateNotifConfig-error.log 2>/dev/null | xargs -I file mv file %{_var}/log/nocpulse
  ls /opt/notification/var/archive/* 2>/dev/null | xargs -I file mv file %log_dir/archive
  ls /opt/notification/var/ticketlog/* 2>/dev/null | xargs -I file mv file %log_dir/ticketlog
fi

%files
%defattr(-,root,root,-)
%{_sysconfdir}/cron.d/notification
%if 0%{?suse_version}
%{httpd_prefix}/cgi-mod-perl
%{httpd_prefix}/templates
%{httpd_prefix}/htdocs/*
%{httpd_prefix}/cgi-bin/*
%else
%{httpd_prefix}
%endif
%dir %attr(-, %notif_user,%notif_user) %install_prefix
%dir %{perl_vendorlib}/NOCpulse/Notif
%{perl_vendorlib}/NOCpulse/Notif/*
%{_bindir}/*
%attr (755,%notif_user,%notif_user) %dir %{_sysconfdir}/notification
%attr (755,%notif_user,%notif_user) %dir %{_sysconfdir}/notification/archive
%attr (755,%notif_user,%notif_user) %dir %{_sysconfdir}/notification/generated
%attr (755,%notif_user,%notif_user) %dir %{_sysconfdir}/notification/static
%attr (755,%notif_user,%notif_user) %dir %{_sysconfdir}/notification/stage
%attr (755,%notif_user,%notif_user) %dir %{_sysconfdir}/notification/stage/config
%attr (755,%notif_user,%notif_user) %dir %install_prefix/queue
%attr (775,mail,       %notif_user) %dir %install_prefix/queue/ack_queue
%attr (775,mail,       %notif_user) %dir %install_prefix/queue/ack_queue/.new
%attr (775,%{apache_user},     %notif_user) %dir %install_prefix/queue/alert_queue
%attr (775,%{apache_user},     %notif_user) %dir %install_prefix/queue/alert_queue/.new
%attr (755,%notif_user,%notif_user) %dir %log_dir
%attr (755,%notif_user,%notif_user) %dir %log_dir/archive
%attr (755,%notif_user,%notif_user) %dir %log_dir/ticketlog
%attr(644,%notif_user,%notif_user) %{_sysconfdir}/notification/static/*
%{_sysconfdir}/smrsh/ack_enqueuer.pl
%{_sysconfdir}/notification/stage/config/static
%{_mandir}/man3/monitor-queue*
%{_mandir}/man3/queue_remote_check.pl*
%dir %{_sysconfdir}/smrsh

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Mon Dec 12 2011 Michael Mraka <michael.mraka@redhat.com> 1.126.26-1
- use real table name rhn_check_probe

* Mon Aug 15 2011 Michael Mraka <michael.mraka@redhat.com> 1.126.25-1
- 700385 - use standard ANSI join
- 700385 - use current_timestamps instead of sysdate
- 700385 - replaced synonym with original table_name
- 700385 - use standard ANSI join
- 700385 - created compatibility views for monitoring
- 700385 - reuse RHN::DB for db connection in NotificationDB.pm

* Thu Jul 21 2011 Miroslav Suchý 1.126.24-1
- 723899 - run that cron task only if /etc/NOCpulse.ini contains something else
  then comments

* Fri May 13 2011 Miroslav Suchý 1.126.23-1
- removing unmaintained file with dependencies

* Wed Apr 27 2011 Jan Pazdziora 1.126.22-1
- Neither functions from File::Basename nor from File::Copy seem to be used by
  ack-processor, removing the uses.

* Fri Mar 18 2011 Michael Mraka <michael.mraka@redhat.com> 1.126.21-1
- reuse RHN:DB for db connection in AlertDB.pm (PG)

* Wed Mar 02 2011 Michael Mraka <michael.mraka@redhat.com> 1.126.20-1
- 493028 - ack_enqueuer.pl must be linked from /etc/smrsh
- 493028 - select all but expired redirects 
- 493028 - empty TZ is interpreted as GMT not local timezone; it must be unset
- 493028 - dates in db are in localtime not GMT
- 493028 - fixed active redirects query condition

* Fri Feb 18 2011 Jan Pazdziora 1.126.19-1
- Localize the filehandle globs; also use three-parameter opens.

* Tue Jan 25 2011 Jan Pazdziora 1.126.18-1
- 493028 - simplified email check regexp (michael.mraka@redhat.com)

* Sat Nov 20 2010 Miroslav Suchý <msuchy@redhat.com> 1.126.17-1
- 474591 - move web data to /usr/share/nocpulse (msuchy@redhat.com)

* Mon Sep 27 2010 Miroslav Suchý <msuchy@redhat.com> 1.126.16-1
- 636211 - include man page for queue_remote_check.pl
- 636211 - include man page for monitor-queue

* Mon Jul 19 2010 Miroslav Suchý <msuchy@redhat.com> 1.126.15-1
- $self->dbh is method from MethodMaker and not attribute (msuchy@redhat.com)

* Mon Jul 12 2010 Miroslav Suchý <msuchy@redhat.com> 1.126.14-1
- remove unused module (msuchy@redhat.com)

* Mon Jul 12 2010 Miroslav Suchý <msuchy@redhat.com> 1.126.13-1
- break dependency of NPalert on perl(NOCpulse::Probe::DataSource::Oracle)
  (msuchy@redhat.com)

* Mon Jul 12 2010 Miroslav Suchý <msuchy@redhat.com> 1.126.12-1
- remove dependency on DBD::Oracle (msuchy@redhat.com)

* Fri Oct 30 2009 Michael Mraka <michael.mraka@redhat.com> 1.126.11-1
- Fix to use MethodMaker-provided accessor methods for list types.
- bailout is defined in NOCpulse::NOCpulseini

* Thu Aug 20 2009 Miroslav Suchý <msuchy@redhat.com> 1.126.10-1
- avoid deadlock when we have problem after acquiring lock

* Thu May 14 2009 Milan Zazrivec <mzazrivec@redhat.com> 1.126.9-1
- fix package upgrade %post section

* Mon May 11 2009 Milan Zazrivec <mzazrivec@redhat.com> 1.126.8-1
- 498257 - migrage existing files into new locations

* Thu Mar  5 2009 Miroslav Suchý <msuchy@redhat.com> 1.126.7-1
- remove dependecies on IO::Capture::Stderr

* Tue Mar  3 2009 Miroslav Suchý <msuchy@redhat.com> 1.126.6-1
- 300011 - properly parse content of lock file

* Wed Feb 18 2009 Miroslav Suchý <msuchy@redhat.com> 1.126.5-1
- fix enqueue-log-check

* Thu Feb 12 2009 Miroslav Suchý <msuchy@redhat.com> 1.126.4-1
- move logs from /var/tmp to /var/log/nocpulse

* Wed Feb 11 2009 Miroslav Suchý <msuchy@redhat.com> 1.126.3-1
- remove dead code (apachereg)

* Fri Jan 16 2009 Miroslav Suchý <msuchy@redhat.com> 1.126.1-1
- fix path to notif-escalator.log again

* Sat Jan 10 2009 Milan Zazrivec 1.125.26-1
- move web data from under /usr/share/nocpulse to /var/www

* Thu Dec 18 2008 Miroslav Suchý <msuchy@redhat.com> 1.125.25-1
- fix path to notif-escalator.log

* Tue Dec 16 2008 Miroslav Suchý <msuchy@redhat.com> 1.125.24-1
- 472895 - remove grouped_fields from Class::MethodMaker declaration

* Thu Dec  4 2008 Miroslav Suchý <msuchy@redhat.com> 1.125.23-1
- 474591 - move web data to /usr/share/nocpulse

* Thu Dec  4 2008 Miroslav Suchý <msuchy@redhat.com> 1.125.22-1
- fix permission of /var/lib/notification

* Mon Dec  1 2008 Miroslav Suchý <msuchy@redhat.com> 1.125.21-1
- 472910 - fix paths to nofitication configs
- rename logrotate script to NPalert

* Thu Oct 16 2008 Milan Zazrivec 1.125.20-1
- tagged for Spacewalk / Satellite build & inclusion

* Thu Oct 02 2008 Dennis Gilmore <dgilmore@redhat.com> 1.125.19-2
- install web content in %%{_datadir}/%%{name}
- set permissions to 644 on html and css files
- preserve timestamps when installing files

* Mon Sep 29 2008 Miroslav Suchý <msuchy@redhat.com> 1.125.19-1
- spec cleanup for Fedora

* Wed Sep  3 2008 Jesus Rodriguez <jesusr@redhat.com> 1.125.18-1
- rebuild for spacewalk
- move version from file to spec file

* Wed Aug 20 2008 Milan Zazrivec <mzazrivec@redhat.com>
- fix for bugzilla #253966

* Wed Jun  4 2008 Milan Zazrivec <mzazrivec@redhat.com> 1.125.17-21
- fixed files permissions

* Mon Jun 2 2008 Pradeep Kilambi <pkilambi@redhat.com> 
- new build

* Fri May 30 2008 Pradeep Kilambi <pkilambi@redhat.com> 1.125.17-20-
- new build

* Tue May 27 2008 Jan Pazdziora <jpazdziora@redhat.com> 1.125.17-19
- fixed bugzilla 438770
- rebuild in dist.cvs
