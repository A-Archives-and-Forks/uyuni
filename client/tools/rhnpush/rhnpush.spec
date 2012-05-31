%define rhnroot %{_datadir}/rhn

Name:          rhnpush
Group:         Applications/System
License:       GPLv2
URL:           http://fedorahosted.org/spacewalk
Version:       5.5.42.3
Release:       1%{?dist}
Source0:       https://fedorahosted.org/releases/s/p/spacewalk/%{name}-%{version}.tar.gz
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
Requires:      rpm-python
Requires:      rhnlib >= 2.5.38
Requires:      spacewalk-backend-libs >= 1.7.17
Requires:      rhn-client-tools
%if 0%{?suse_version}
# provides rhn directories for filelist check in OBS
BuildRequires:      rhn-client-tools
%endif
BuildRequires: docbook-utils, gettext
BuildRequires: python-devel

Summary: Package uploader for the Spacewalk Server

%description
rhnpush uploads package headers to the Spacewalk servers into
specified channels and allows for several other channel management
operations relevant to controlling what packages are available per
channel.

%prep
%setup -q
%if 0%{?rhel} && 0%{?rhel} <= 4
patch -p0 < patches/rhel4-static.dif
%endif

%build
make -f Makefile.rhnpush all

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/%{rhnroot}
make -f Makefile.rhnpush install PREFIX=$RPM_BUILD_ROOT ROOT=%{rhnroot} \
    MANDIR=%{_mandir}
%if 0%{?suse_version}
ln -s rhnpush $RPM_BUILD_ROOT/%{_bindir}/mgrpush
%endif

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%dir %{rhnroot}
%dir %{_sysconfdir}/sysconfig/rhn
%dir %{rhnroot}/rhnpush
%{rhnroot}/rhnpush/*
%attr(755,root,root) %{_bindir}/rhnpush
%if 0%{?suse_version}
%{_bindir}/mgrpush
%endif
%attr(755,root,root) %{_bindir}/rpm2mpm
%attr(755,root,root) %{_bindir}/solaris2mpm
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/sysconfig/rhn/rhnpushrc
%{_mandir}/man8/rhnpush.8*
%{_mandir}/man8/solaris2mpm.8*

%changelog
* Fri Mar 02 2012 Jan Pazdziora 5.5.42-1
- Update the copyright year info.

* Mon Feb 20 2012 Michael Mraka <michael.mraka@redhat.com> 5.5.41-1
- merged list() with parent class
- merged uploadHeaders() with parent class
- the very same newest() is defined in parent class

* Wed Feb 08 2012 Michael Mraka <michael.mraka@redhat.com> 5.5.40-1
- pylint fixes

* Tue Feb 07 2012 Michael Mraka <michael.mraka@redhat.com> 5.5.39-1
- updated uploadLib to use A_Package interface
- removed legacy code for satellite < 4.0.6 support
- converted rhnpush to use A_Package interface
- InvalidPackageError is now in rhn_pkg
- removed support for satellite < 4.1.0

* Mon Feb 06 2012 Michael Mraka <michael.mraka@redhat.com> 5.5.38-1
- require new spacewalk-backend-libs

* Sat Feb 04 2012 Michael Mraka <michael.mraka@redhat.com> 5.5.37-1
- fixed pylint errors / warnings

* Wed Dec 21 2011 Milan Zazrivec <mzazrivec@redhat.com> 5.5.36-1
- update copyright info

* Tue Nov 29 2011 Michael Mraka <michael.mraka@redhat.com> 5.5.35-1
- removed dead functions

* Thu Nov 24 2011 Michael Mraka <michael.mraka@redhat.com> 5.5.34-1
- replaced external zip with zipfile module
- replaced external tar with tarfile module
- don't call os.path.join() over and over
- don't read 2GB file into memory at once
- don't hide original error message
- replaced external unzip with zipfile module

* Wed Oct 19 2011 Michael Mraka <michael.mraka@redhat.com> 5.5.33-1
- removed test for already removed object_has_attr()
- removed dead function object_has_attr()

* Thu Aug 11 2011 Miroslav Suchý 5.5.32-1
- True and False constants are defined since python 2.4
- do not mask original error by raise in execption

* Thu Jul 28 2011 Jan Pazdziora 5.5.31-1
- removing unnecessarry summary line from rhnpush.spec (lzap+git@redhat.com)

* Fri Jul 22 2011 Jan Pazdziora 5.5.30-1
- We always have rhnserver (no longer building for RHEL 4-).
- We only support version 5 and newer of RHEL, removing conditions for old
  versions.

* Fri Jul 15 2011 Miroslav Suchý 5.5.29-1
- optparse is here since python 2.3 - remove optik (msuchy@redhat.com)

* Tue Jun 21 2011 Jan Pazdziora 5.5.28-1
- 559092 - recognize both new and old patch clusters (michael.mraka@redhat.com)
- 485880 - put -N option to SYNOPSIS as well (msuchy@redhat.com)

* Thu May 05 2011 Miroslav Suchý 5.5.27-1
- do not test if rhnParent can handle session caching

* Fri Apr 15 2011 Jan Pazdziora 5.5.26-1
- build rhnpush on SUSE (mc@suse.de)

* Tue Apr 12 2011 Miroslav Suchý 5.5.25-1
- build rhnpush on SUSE (mc@suse.de)

* Fri Apr 08 2011 Miroslav Suchý 5.5.24-1
- Revert "idn_unicode_to_pune() have to return string" (msuchy@redhat.com)

* Fri Apr 08 2011 Miroslav Suchý 5.5.23-1
- update copyright years (msuchy@redhat.com)

* Tue Apr 05 2011 Michael Mraka <michael.mraka@redhat.com> 5.5.22-1
- idn_unicode_to_pune() has to return string
- no need to define built-in constants
- delete dead code

* Fri Apr 01 2011 Miroslav Suchý 5.5.21-1
- pass only one argument to idn_ascii_to_pune (msuchy@redhat.com)

* Wed Mar 30 2011 Miroslav Suchý 5.5.20-1
- 683200 - instead of encodings.idna use wrapper from rhn.connections, which
  workaround corner cases
- 683200 - rhnpush.py - convert servername from input to Pune encodings

* Wed Mar 02 2011 Michael Mraka <michael.mraka@redhat.com> 5.5.19-1
- Revertes "use size instead of archivesize"

* Thu Feb 24 2011 Michael Mraka <michael.mraka@redhat.com> 5.5.18-1
- use size instead of archivesize

* Fri Feb 18 2011 Jan Pazdziora 5.5.17-1
- Revert "Revert "get_server_capability() is defined twice in osad and rhncfg,
  merge and move to rhnlib and make it member of rpclib.Server""
  (msuchy@redhat.com)
- Revert "Revert "648403 - do not create TB even on Red Hat Enterprise Linux
  4"" (msuchy@redhat.com)

* Tue Feb 01 2011 Tomas Lestach <tlestach@redhat.com> 5.5.16-1
- Revert "648403 - do not create TB even on Red Hat Enterprise Linux 4"
  (tlestach@redhat.com)

* Tue Feb 01 2011 Tomas Lestach <tlestach@redhat.com> 5.5.15-1
- Revert "get_server_capability() is defined twice in osad and rhncfg, merge
  and move to rhnlib and make it member of rpclib.Server" (tlestach@redhat.com)

* Tue Feb 01 2011 Miroslav Suchý <msuchy@redhat.com> 5.5.14-1
- 648403 - do not require up2date on rhel5

* Fri Jan 28 2011 Miroslav Suchý <msuchy@redhat.com> 5.5.13-1
- get_server_capability() is defined twice in osad and rhncfg, merge and move
  to rhnlib and make it member of rpclib.Server
- 648403 - do not create TB even on Red Hat Enterprise Linux 4
- 648403 - workaround missing hasCapability() on RHEL4
- Updating the copyright years to include 2010.

* Thu Dec 23 2010 Miroslav Suchý <msuchy@redhat.com> 5.5.12-1
- 648403 - use server given on command line rather than rhnParent

* Mon Dec 20 2010 Miroslav Suchý <msuchy@redhat.com> 5.5.11-1
- 648403 - do not call getPackageChecksumBySession directly

* Wed Dec 08 2010 Michael Mraka <michael.mraka@redhat.com> 5.5.10-1
- import Fault, ResponseError and ProtocolError directly from xmlrpclib

* Mon Dec 06 2010 Miroslav Suchý <msuchy@redhat.com> 5.5.9-1
- 656746 - make _processFile and _processBatch method of UploadClass class
  (msuchy@redhat.com)

* Wed Nov 24 2010 Michael Mraka <michael.mraka@redhat.com> 5.5.8-1
- removed unused imports

* Wed Nov 03 2010 Jan Pazdziora 5.5.7-1
- 649259 - do not fail with invalid user, if we are only testing if call exist
  (msuchy@redhat.com)

* Tue Nov 02 2010 Jan Pazdziora 5.5.6-1
- Update copyright years in the rest of the repo.

* Thu Sep 16 2010 Michael Mraka <michael.mraka@redhat.com> 5.5.5-1
- 600347 - added sat<540 compatibility functions

* Fri Jul 16 2010 Michael Mraka <michael.mraka@redhat.com> 5.5.4-1
- removed dead code

* Thu Jul 08 2010 Justin Sherrill <jsherril@redhat.com> 5.5.3-1
- set default server for rhnpush to localhost instead of
  rhn.redhat.com (jsherril@redhat.com)

* Thu Jul 01 2010 Miroslav Suchý <msuchy@redhat.com> 5.5.2-1
- Also fixed 'Info' -> 'info' as suggested by Milan Zazrivec.
  (jhutar@redhat.com)
- And one more space in 'sometime' as suggested by Jan Pazdziora
  (jhutar@redhat.com)
- Just put space to the correct side (jhutar@redhat.com)

* Tue May 18 2010 Miroslav Suchý <msuchy@redhat.com> 5.5.1-1
- 470154 - arch can be optional, do not freak out if it is not present
- 514805 - recognize X86 arch as i386
- 516898 - workaround for patches which do not have packed most top directory
- no need to copy file, we can operate directly on original
- do not read one file twice
- 559092 - recognize new sun patch cluster format
- 569946 - normalize solaris "x86" value to rhn known value

* Mon Apr 19 2010 Michael Mraka <michael.mraka@redhat.com> 5.4.14-1
- 563630 - Enable proxy support for rhnpush

* Sat Feb 06 2010 Michael Mraka <michael.mraka@redhat.com> 5.4.13-1
- removed duplicated __main__

* Thu Feb 04 2010 Michael Mraka <michael.mraka@redhat.com> 5.4.12-1
- updated copyrights

* Tue Feb 02 2010 Michael Mraka <michael.mraka@redhat.com> 5.4.11-1
- 537081 - don't fail if config file not found

* Mon Feb 01 2010 Michael Mraka <michael.mraka@redhat.com> 5.4.10-1
- removed dead python 1.5 code

* Wed Jan 27 2010 Miroslav Suchy <msuchy@redhat.com> 5.4.9-1
- import function directly; checksum namespace overlaps with a variable (michael.mraka@redhat.com)
- replaced popen2 with subprocess in client (michael.mraka@redhat.com)

* Thu Jan 14 2010 Michael Mraka <michael.mraka@redhat.com> 5.4.8-1
- fixed uninitialized values

* Thu Jan 07 2010 Michael Mraka <michael.mraka@redhat.com> 5.4.7-1
- code cleanup

* Thu Dec 10 2009 Michael Mraka <michael.mraka@redhat.com> 5.4.6-1
- added support for SHA256 rpms
- fixed namespace for rhn_rpm

* Mon Dec 07 2009 Michael Mraka <michael.mraka@redhat.com> 5.4.5-1
- moved code from rhnlib to spacewalk-backend-libs

* Fri Dec  4 2009 Miroslav Suchý <msuchy@redhat.com> 5.4.4-1
- merge uploadLib.py

* Fri Dec 04 2009 Michael Mraka <michael.mraka@redhat.com> 5.4.3-1
- rhn_rpm/rhn_mpm moved to rhnlib

* Thu Jun 25 2009 John Matthews <jmatthew@redhat.com> 5.4.2-1
- merging missed chances from previous commit (pkilambi@redhat.com)
- removing unused modules and some clean up (pkilambi@redhat.com)
-  fixing rhnpush to work on fedora-11 clients. Replaced the deprecated
  checksum modules and use hashlib instead. (pkilambi@redhat.com)

* Wed Apr 08 2009 Jan Pazdziora 5.4.1-1
- 488157 - turn sparcv9 into sparc

* Tue Apr 07 2009 Devan Goodwin <dgoodwin@redhat.com> 5.4.0-1
- Bump release following release of Spacewalk 0.5.

* Fri Apr  3 2009 Jan Pazdziora 5.3.0-1
- bump version to 5.3.0

* Wed Apr 01 2009 Pradeep Kilambi <pkilambi@redhat.com> 0.4.7-1
- new build for 485880 (pkilambi@redhat.com)
- 241221 - add release of the package (if it exists) to Provides (Jan P.)

* Wed Apr  1 2009 Pradeep Kilambi <pkilambi@redhat.com>
- Resolves: 485880 - missing help and man options for rhnpush - new build

* Wed Mar 11 2009 jesus m. rodriguez <jesusr@redhat.com> 0.4.6-1
- 485880 - adding missing man page options to rhnpush
- Fix tab in rhnpush.py.

* Thu Feb 26 2009 jesus m. rodriguez <jesusr@redhat.com> 0.4.5-1
- rebuild

* Wed Feb 25 2009 Pradeep Kilambi <pkilambi@redhat.com> 0.4.4-1
- Resolves: 487426 rhnpush should now require rhnlib

* Fri Feb 20 2009 Miroslav Suchy <msuchy@redhat.com> 0.4.4-1
- change builrequires from file dep. to package dep.

* Fri Feb 20 2009 Michael Stahnke <stahnma@fedoraproject.org> 0.4.3-1
- Package cleanup for Fedora Inclusion

* Thu Feb 12 2009 jesus m. rodriguez <jesusr@redhat.com> 0.4.2-1
- replace "!#/usr/bin/env python" with "!#/usr/bin/python"
- 436332 - return an error code other than 0 if there is a mismatch
- more changes for nvrea error handling
- 241127 - Solaris patch-requires fix
- 241369 - --force and --nullorg are incompatible options
- bump up version 0.4.1
- 461701 - don't use cached session if username is provided on commandline

* Wed Sep 24 2008 Milan Zazrivec 0.3.1-1
- Bumped version for spacewalk 0.3

* Tue Sep  2 2008 Milan Zazrivec 0.2.2-1
- Bumped version for spacewalk 0.2

* Thu Nov 02 2006 James Bowes <jbowes@redhat.com> - 4.2.0-48
- Initial seperate packaging.
