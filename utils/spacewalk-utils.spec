%define rhnroot %{_prefix}/share/rhn

Name:		spacewalk-utils
Version:	1.7.14
Release:	1%{?dist}
Summary:	Utilities that may be run against a Spacewalk server.

Group:		Applications/Internet
License:	GPLv2
URL:		https://fedorahosted.org/spacewalk
Source0:	https://fedorahosted.org/releases/s/p/spacewalk/%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  /usr/bin/docbook2man
BuildRequires:  docbook-utils
BuildRequires:  python
%if 0%{?fedora} > 15 || 0%{?rhel} > 5 || 0%{?suse_version} > 1100
# pylint check
BuildRequires:  spacewalk-pylint
BuildRequires:  yum
BuildRequires:  spacewalk-backend >= 1.7.24
BuildRequires:  spacewalk-backend-libs >= 1.7.24
BuildRequires:  spacewalk-backend-tools >= 1.7.24
%endif

Requires:       bash
Requires:       cobbler
Requires:       coreutils
%if ! 0%{?suse_version}
Requires:       initscripts
%endif
Requires:       iproute
Requires:       net-tools
Requires:       /usr/bin/spacewalk-sql
Requires:       perl-Satcon
%if 0%{?suse_version}
Requires:     perl = %{perl_version}
%else
Requires:     perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
%endif
Requires:       python, rpm-python
Requires:       rhnlib >= 2.5.20
Requires:       rpm
%if ! 0%{?suse_version}
Requires:       setup
%endif
Requires:       spacewalk-admin
Requires:       spacewalk-certs-tools
Requires:       spacewalk-config
Requires:       spacewalk-setup
Requires:       spacewalk-backend
Requires:       spacewalk-backend-libs
Requires:       spacewalk-backend-tools
Requires:       yum-utils

%description
Generic utilities that may be run against a Spacewalk server.


%prep
%setup -q


%build
make all

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/%{rhnroot}
make install PREFIX=$RPM_BUILD_ROOT ROOT=%{rhnroot} \
    MANDIR=%{_mandir}


%clean
rm -rf $RPM_BUILD_ROOT

%check
%if 0%{?fedora} > 15 || 0%{?rhel} > 5 || 0%{?suse_version} > 1100
# check coding style
spacewalk-pylint $RPM_BUILD_ROOT%{rhnroot}
%endif

%files
%defattr(-,root,root)
%config %{_sysconfdir}/rhn/spacewalk-common-channels.ini
%attr(755,root,root) %{_bindir}/*
%dir %{rhnroot}/utils
%{rhnroot}/utils/__init__.py*
%{rhnroot}/utils/systemSnapshot.py*
%{rhnroot}/utils/migrateSystemProfile.py*
%{rhnroot}/utils/cloneByDate.py*
%{rhnroot}/utils/depsolver.py*
%{_mandir}/man8/*
%dir /etc/rhn
%dir %{_datadir}/rhn

%changelog
* Fri Feb 24 2012 Michael Mraka <michael.mraka@redhat.com> 1.7.14-1
- fixed pylint errors
- use spacewalk-pylint for coding style check

* Thu Feb 23 2012 Michael Mraka <michael.mraka@redhat.com> 1.7.13-1
- we are now just GPL

* Wed Feb 22 2012 Miroslav Suchý 1.7.12-1
- 788083 - IPv6 support in spacewalk-hostname-rename (mzazrivec@redhat.com)
- errata date clone - adding --skip-depsolve option, and fixing some man page
  errors (jsherril@redhat.com)
- errata date clone - fixing issue where repoclosure was not being passed all
  needed arguments (jsherril@redhat.com)
- errata date clone - fixing issue where raise was not called on an exception
  (jsherril@redhat.com)
- errata date clone - removing packages from remove list even if no errata are
  cloned (jsherril@redhat.com)
- errata date clone - better error message when repodata is missing
  (jsherril@redhat.com)
- errata date clone - man page fix, and catching if config file does not exist
  (jsherril@redhat.com)
- errata date clone - making regular expression syntax more apparent in docs
  (jsherril@redhat.com)
- errata date clone - pylint fixes (jsherril@redhat.com)
- errata date clone - do not dep solve if no packages were added
  (jsherril@redhat.com)
- errata date clone - adding ability to specify per-channel blacklists
  (jsherril@redhat.com)
- errata date clone - fixing issue where old metadata could be reused if the
  previous run did not complete (jsherril@redhat.com)
- errata date clone - improving user feedback in some cases
  (jsherril@redhat.com)
- errata date clone - adding regular expression support for package exclusion
  lists (jsherril@redhat.com)
- errata date clone - adding auth check to make sure that login is refreshed
  before session timeout (jsherril@redhat.com)
- errata date clone - changing meaning of blacklist to only remove packages
  based on delta, and adding removelist to remove packages based on full
  channel contents (jsherril@redhat.com)
- fixing some man page spelling errors (jsherril@redhat.com)

* Mon Feb 13 2012 Michael Mraka <michael.mraka@redhat.com> 1.7.11-1
- fixed spacewalk-common-channel glob matching

* Mon Feb 13 2012 Michael Mraka <michael.mraka@redhat.com> 1.7.10-1
- 591156 - fix for clone by date to use repodata dir for dep resolution

* Tue Feb 07 2012 Jan Pazdziora 1.7.9-1
- The COBBLER_SETTINGS_FILE is not used, we call cobbler-setup to do the work.
- errata date clone - fixing a few more issues with man page and adding a bit
  more user output (jsherril@redhat.com)
- errata date clone - another man page fix (jsherril@redhat.com)
- errata date clone - man page fix (jsherril@redhat.com)
- errata date clone - fixing man page formatting (jsherril@redhat.com)

* Thu Feb 02 2012 Justin Sherrill <jsherril@redhat.com> 1.7.8-1
- errata date clone - fixing imports (jsherril@redhat.com)

* Thu Feb 02 2012 Justin Sherrill <jsherril@redhat.com> 1.7.7-1
- errata date clone - fixing packaging to clone properly (jsherril@redhat.com)
- errata date clone - adding validate to man page (jsherril@redhat.com)

* Thu Feb 02 2012 Justin Sherrill <jsherril@redhat.com> 1.7.6-1
- errata date clone - fixing a few errors from pylint fixes
  (jsherril@redhat.com)

* Wed Feb 01 2012 Justin Sherrill <jsherril@redhat.com> 1.7.5-1
- pylint fixes (jsherril@redhat.com)

* Wed Feb 01 2012 Justin Sherrill <jsherril@redhat.com> 1.7.4-1
- adding initial spacewalk-clone-by-date (jsherril@redhat.com)

* Thu Jan 05 2012 Michael Mraka <michael.mraka@redhat.com> 1.7.3-1
- removed map and filter from bad-function list

* Thu Jan 05 2012 Michael Mraka <michael.mraka@redhat.com> 1.7.2-1
- pylint is required for coding style check

* Wed Jan 04 2012 Michael Mraka <michael.mraka@redhat.com> 1.7.1-1
- fixed coding style and pylint warnings
- added spacewalk-nightly-*-fedora16 definitions

* Wed Dec 21 2011 Milan Zazrivec <mzazrivec@redhat.com> 1.6.6-1
- Channel definitions for Spacewalk 1.6

* Wed Dec 21 2011 Milan Zazrivec <mzazrivec@redhat.com> 1.6.5-1
- update copyright info

* Wed Nov 23 2011 Jan Pazdziora 1.6.4-1
- Prevent Malformed UTF-8 character error upon dump.

* Fri Sep 09 2011 Michael Mraka <michael.mraka@redhat.com> 1.6.3-1
- updated spacewalk repos
- added scientific linux 6 repo
- added epel6 repos

* Thu Aug 11 2011 Miroslav Suchý 1.6.2-1
- do not mask original error by raise in execption

* Thu Jul 21 2011 Jan Pazdziora 1.6.1-1
- Adding centos6 and fedora15 repos. (jonathan.hoser@helmholtz-muenchen.de)

* Wed Jul 13 2011 Jan Pazdziora 1.5.4-1
- We get either undefined value or BLOB for the blob columns type.

* Fri May 20 2011 Michael Mraka <michael.mraka@redhat.com> 1.5.3-1
- fix broken (non-utf8) changelog entries

* Fri Apr 29 2011 Michael Mraka <michael.mraka@redhat.com> 1.5.2-1
- fixed base channel for spacewalk on F14
- added spacewalk nightly entries
- added spacewalk 1.4 entries

* Mon Apr 18 2011 Jan Pazdziora 1.5.1-1
- fix pattern bash matching (mzazrivec@redhat.com)

* Thu Mar 24 2011 Jan Pazdziora 1.4.3-1
- In spacewalk-dump-schema, use the default Oracle connect information from
  config file.

* Thu Mar 10 2011 Michael Mraka <michael.mraka@redhat.com> 1.4.2-1
- made spacewalk-hostname-rename working on postgresql


* Thu Feb 03 2011 Michael Mraka <michael.mraka@redhat.com> 1.4.1-1
- updated spacewalk-common-channel to spacewalk 1.3
- Bumping package versions for 1.4

* Tue Jan 04 2011 Michael Mraka <michael.mraka@redhat.com> 1.3.4-1
- fixed pylint errors

* Tue Dec 14 2010 Jan Pazdziora 1.3.3-1
- We need to check the return value of GetOptions and die if the parameters
  were not correct.

* Tue Nov 23 2010 Michael Mraka <michael.mraka@redhat.com> 1.3.2-1
- fixed pylint errors
- added spacewalk 1.2 channels and repos

* Fri Nov 19 2010 Michael Mraka <michael.mraka@redhat.com> 1.3.1-1
- re-added automatic external yum repo creation based on new API
- Bumping package versions for 1.3

* Fri Nov 05 2010 Miroslav Suchý <msuchy@redhat.com> 1.2.9-1
- 491331 - move /etc/sysconfig/rhn-satellite-prep to /var/lib/rhn/rhn-
  satellite-prep (msuchy@redhat.com)

* Mon Nov 01 2010 Jan Pazdziora 1.2.8-1
- As the table rhnPaidErrataTempCache is no more, we do not need to have check
  for temporary tables.

* Fri Oct 29 2010 Michael Mraka <michael.mraka@redhat.com> 1.2.7-1
- fixed spacewalk-common-channels
- updated spacewalk-common-channels to Spacewalk 1.1 and Fedora 13 and 14

* Tue Oct 26 2010 Jan Pazdziora 1.2.6-1
- Blobs (byteas) want double backslashes and octal values.

* Thu Oct 21 2010 Jan Pazdziora 1.2.5-1
- Adding spacewalk-dump-schema to the Makefile to be added to the rpm.
- Documentation (man page).
- For blobs, quote everything; for varchars, do not quote the UTF-8 characters.
- Export in UTF-8.
- To process the evr type, we need to handle the ARRAY ref.
- Skip the quartz tables, they get regenerated anyway.
- Escape characters that we need to escape.
- Use the ISO format for date.
- Dump records.
- No commit command, we run psql in autocommit.
- Fail if we try to dump lob longer than 10 MB.
- Do not dump copy commands for tables that are empty.
- For each table, print the copy command.
- Do not attempt to copy over temporary tables or we get error about
  rhnpaiderratatempcache.
- Initial table processing -- just purge for now.
- Stop on errors.
- Dump sequences.
- Process arguments and connect.
- Original stub of the schema dumper.

* Tue Oct 19 2010 Jan Pazdziora 1.2.4-1
- As Oracle XE is no longer managed by rhn-satellite, we need to change the
  logic in spacewalk-hostname-rename a bit as well.

* Tue Oct 05 2010 Tomas Lestach <tlestach@redhat.com> 1.2.3-1
- 639818 - fixing sys path (tlestach@redhat.com)

* Mon Oct 04 2010 Michael Mraka <michael.mraka@redhat.com> 1.2.2-1
- replaced local copy of compile.py with standard compileall module

* Thu Sep 09 2010 Tomas Lestach <tlestach@redhat.com> 1.2.1-1
- 599030 - check whether SSL certificate generation was successful
  (tlestach@redhat.com)
- use hostname as default value for organization unit (tlestach@redhat.com)
- enable also VPN IP (tlestach@redhat.com)
- bumping package versions for 1.2 (mzazrivec@redhat.com)

* Mon May 17 2010 Tomas Lestach <tlestach@redhat.com> 1.1.5-1
- changing package description (tlestach@redhat.com)
- do not check /etc/hosts file for actual hostname (tlestach@redhat.com)
- check for presence of bootstrap files before modifying them
  (tlestach@redhat.com)
- fixed typo (tlestach@redhat.com)
- set localhost instead of hostname to tnsnames.ora and listener.ora
  (tlestach@redhat.com)
- fixed a typo in the man page (tlestach@redhat.com)

* Tue Apr 27 2010 Tomas Lestach <tlestach@redhat.com> 1.1.4-1
- fixed Requires (tlestach@redhat.com)
- spacewalk-hostname-rename code cleanup (tlestach@redhat.com)

* Thu Apr 22 2010 Tomas Lestach <tlestach@redhat.com> 1.1.3-1
- adding requires to utils/spacewalk-utils.spec (tlestach@redhat.com)

* Wed Apr 21 2010 Tomas Lestach <tlestach@redhat.com> 1.1.2-1
- changes to spacewalk-hostname-rename script (tlestach@redhat.com)
- introducing spacewalk-hostname-rename.sh script (tlestach@redhat.com)

* Mon Apr 19 2010 Michael Mraka <michael.mraka@redhat.com> 1.1.1-1
- bumping spec files to 1.1 packages

* Thu Apr 01 2010 Miroslav Suchý <msuchy@redhat.com> 0.9.6-1
- add script delete-old-systems-interactive

* Tue Mar 16 2010 Michael Mraka <michael.mraka@redhat.com> 0.9.5-1
- added repo urls and gpg keys to spacewalk-common-channel.ini

* Mon Feb 22 2010 Michael Mraka <michael.mraka@redhat.com> 0.9.4-1
- emulate epilog in optparse on RHEL5 (python 2.4)

* Wed Feb 17 2010 Michael Mraka <michael.mraka@redhat.com> 0.9.3-1
- fixed of spacewalk-common-channels

* Mon Feb 15 2010 Michael Mraka <michael.mraka@redhat.com> 0.9.2-1
- added spacewalk-common-channels utility

* Thu Feb 04 2010 Michael Mraka <michael.mraka@redhat.com> 0.8.3-1
- updated copyrights

* Mon Feb 01 2010 Michael Mraka <michael.mraka@redhat.com> 0.8.2-1
- use rhnLockfile from rhnlib

* Tue Jan 05 2010 Michael Mraka <michael.mraka@redhat.com> 0.8.1-1
- added scr.cgi and apply_errata scripts

* Wed Nov 25 2009 Miroslav Suchý <msuchy@redhat.com> 0.7.1-1
- migration of system profile should be able to run as non root now that it can run on any client and not just satellite. (pkilambi@redhat.com)
- bumping Version to 0.7.0 (jmatthew@redhat.com)

* Wed Aug 05 2009 Jan Pazdziora 0.6.7-1
- utils: add python to BuildRequires

* Fri Jul 31 2009 Pradeep Kilambi <pkilambi@redhat.com> 0.6.6-1
- removing common module dep and adding locking to utils package.

* Wed Jul 15 2009 Miroslav Suchý <msuchy@redhat.com> 0.6.5-1
- add spacewalk-api script, which can interact with API from command line

* Mon May 11 2009 Brad Buckingham <bbuckingham@redhat.com> 0.6.4-1
- 500173 - update migrate-system-profile to import scripts from utils vs
  spacewalk_tools (bbuckingham@redhat.com)

* Sun May 03 2009 Brad Buckingham <bbuckingham@redhat.com> 0.6.3-1
- updates to include system migration scripts


* Mon Apr 27 2009 Brad Buckingham <bbuckingham@redhat.com> 0.6.2-1
- Adding migrate system profile tool to utils package

* Tue Apr 07 2009 Brad Buckingham <bbuckingham@redhat.com> 0.6.1-1
- Initial spec created to include sw-system-snapshot package
