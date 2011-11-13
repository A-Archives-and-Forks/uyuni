%if 0%{?suse_version}
%define cgi_bin        /srv/www/cgi-bin
%define cgi_mod_perl   /srv/www/cgi-mod-perl
%define templatedir    /srv/www/templates
%else
%define cgi_bin        %{_datadir}/nocpulse/cgi-bin
%define cgi_mod_perl   %{_datadir}/nocpulse/cgi-mod-perl
%define templatedir    %{_datadir}/nocpulse/templates
%endif
%define bin            %{_bindir}
%define vardir         /var/lib/nocpulse
Name:         SputLite
Source0:      https://fedorahosted.org/releases/s/p/spacewalk/%{name}-%{version}.tar.gz
Version:      1.6.1
Release:      1%{?dist}
Summary:      Command queue processor (Sputnik Lite)
URL:          https://fedorahosted.org/spacewalk
BuildArch:    noarch
%if 0%{?suse_version}
BuildRequires: nocpulse-common
%else
Requires:     perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
%endif

Group:        Applications/System
License:      GPLv2
Buildroot:    %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Provides command-queue capability.

%package server
Summary:  Command queue processor (Sputnik Lite)
Group:    Applications/System
Requires: nocpulse-common

%description server
Provides command-queue server capability.

%package client
Summary:  Command queue processor (Sputnik Lite)
%if ! 0%{?suse_version}
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
%endif
Requires: MessageQueue ProgAGoGo
Group:    Applications/System
Requires: nocpulse-common

%description  client
Provides command-queue client capability for Spacewalk.

%prep
%setup -q

%build
#Nothing to build

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{perl_vendorlib}/NOCpulse
install -m 644 lib/CommandQueue.pm $RPM_BUILD_ROOT%{perl_vendorlib}/NOCpulse/CommandQueue.pm

# Install server
# CGI bin and mod-perl bin
mkdir -p $RPM_BUILD_ROOT%cgi_bin
mkdir -p $RPM_BUILD_ROOT%cgi_mod_perl
install -m 755 html/cgi-mod-perl/*.cgi $RPM_BUILD_ROOT%cgi_mod_perl
install -m 755 html/cgi-bin/*.cgi $RPM_BUILD_ROOT%cgi_bin

# Server HTML templates
mkdir -p $RPM_BUILD_ROOT%templatedir
install -m 644 html/templates/*.html $RPM_BUILD_ROOT%templatedir

# Install client
# Client perl libraries
mkdir -p $RPM_BUILD_ROOT%{perl_vendorlib}/NOCpulse/CommandQueue
install -m 644 lib/CommandQueue/Command.pm $RPM_BUILD_ROOT%{perl_vendorlib}/NOCpulse/CommandQueue/Command.pm
install -m 644 lib/CommandQueue/Parser.pm  $RPM_BUILD_ROOT%{perl_vendorlib}/NOCpulse/CommandQueue/Parser.pm

# Client NOCpulse bin
mkdir -p $RPM_BUILD_ROOT%bin
install -m 755 bin/execute_commands $RPM_BUILD_ROOT%bin/execute_commands

# Client var files and directories
mkdir -p $RPM_BUILD_ROOT%vardir/commands
mkdir -p $RPM_BUILD_ROOT%vardir/queue/commands

%post client
# only needed in the update case because of a moved home
%if ! 0%{?suse_version}
if [ $1 -eq 2 ]; then
  ls /home/nocpulse/var/commands/heartbeat 2>/dev/null | xargs -I file mv file %{vardir}/commands
  ls /home/nocpulse/var/commands/last_completed 2>/dev/null | xargs -I file mv file %{vardir}/commands
  ls /home/nocpulse/var/commands/last_started 2>/dev/null | xargs -I file mv file %{vardir}/commands
fi
%endif

%files server
%defattr(-,root,root,-)
%attr(755, nocpulse, nocpulse) %dir %templatedir
%{perl_vendorlib}/NOCpulse/*
%cgi_bin/*
%dir %{cgi_mod_perl}
%cgi_mod_perl/*
%templatedir/*

%files client
%defattr(-,root,root,-)
%attr(755,nocpulse,nocpulse) %dir %{vardir}
%attr(755,nocpulse,nocpulse) %dir %{vardir}/queue
%attr(755,nocpulse,nocpulse) %dir %{vardir}/commands
%attr(755,nocpulse,nocpulse) %dir %{vardir}/queue/commands
%{_bindir}/*
%{perl_vendorlib}/NOCpulse/*

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Tue Aug 30 2011 Michael Mraka <michael.mraka@redhat.com> 1.6.1-1
- remove perl module files from the -server package

* Fri Mar 18 2011 Michael Mraka <michael.mraka@redhat.com> 1.4.2-1
- fixed db connection in fetch_nocpulseini*.cgi (PG)

* Fri Feb 18 2011 Jan Pazdziora 1.4.1-1
- Localize the filehandle globs; also use three-parameter opens.

* Sat Nov 20 2010 Miroslav Suchý <msuchy@redhat.com> 0.48.14-1
- bumping version as tag SputLite-0.48.13-1 already exists (msuchy@redhat.com)
- 474591 - move web data to /usr/share/nocpulse (msuchy@redhat.com)

* Wed Mar 31 2010 Miroslav Suchý <msuchy@redhat.com> 0.48.12-1
- do not care about sending email, transfer the worries to perl-MailTools

* Thu Jun 25 2009 John Matthews <jmatthew@redhat.com> 0.48.11-1
- Don't move execute_commands.log to /var/log/nocpulse (mzazrivec@redhat.com)

* Mon May 11 2009 Milan Zazrivec <mzazrivec@redhat.com> 0.48.10-1
- 498257 - migrate existing files into new nocpulse homedir

* Mon May 11 2009 Miroslav Suchý <msuchy@redhat.com> 0.48.9-1
- 499568 - require scout_shared_key for requesting NOCpulse.ini

* Wed Feb 11 2009 Miroslav Suchý <msuchy@redhat.com> 0.48.7-1
- remove dead code (apachereg)

* Mon Feb  9 2009 Jan Pazdziora 0.48.6-1
- look at /proc/.../stat directly, instead of running ps

* Sat Jan 10 2009 Milan Zazrivec 0.48.5-1
- move content from under /usr/share/nocpulse to /var/www

* Wed Jan 07 2009 Dave Parker <dparker@redhat.com> 0.48.4-1
- 461162 - move sputlite cgi programs to stock location in /var/www/cgi-bin

* Thu Dec  4 2008 Miroslav Suchý <msuchy@redhat.com> 0.48.3-1
- 474591 - move web data to /usr/share/nocpulse

* Mon Oct 20 2008 Miroslav Suchý <msuchy@redhat.com> 0.48.2-1
- 467441 - fix namespace

* Thu Sep 25 2008 Miroslav Suchý <msuchy@redhat.com> 0.48.1-1
- spec cleanup for Fedora

* Thu Jun 19 2008 Miroslav Suchy <msuchy@redhat.com>
- migrating nocpulse home dir (BZ 202614)

* Mon Jun 16 2008 Milan Zazrivec <mzazrivec@redhat.com> 0.48.0-4
- cvs.dist import
