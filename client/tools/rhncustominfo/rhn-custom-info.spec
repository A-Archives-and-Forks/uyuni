Name: rhn-custom-info
Summary: Set and list custom values for RHN-enabled machines
Group: Applications/System
License: GPLv2 and Python
Source0: https://fedorahosted.org/releases/s/p/spacewalk/%{name}-%{version}.tar.gz
URL:     https://fedorahosted.org/spacewalk
Version: 5.4.12
Release: 1%{?dist}
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch: noarch
BuildRequires: python-devel
%if 0%{?rhel} && 0%{?rhel} <= 4
BuildRequires: python
Requires: python-abi = %(%{__python} -c "import sys; print sys.version[:3]")
%endif
Requires: rhnlib

Requires: spacewalk-client-tools
%if 0%{?rhel} >= 5 || 0%{?fedora} >= 1
Requires: yum-rhn-plugin
%else
# rpm do not support elif
%if 0%{?suse_version}
Requires: zypp-plugin-spacewalk
# provide rhn directories for filelist check
BuildRequires: spacewalk-client-tools
%else
Requires: up2date
%endif
%endif

%description
Allows for the setting and listing of custom key/value pairs for
an RHN-enabled system.

%prep
%setup -q

%build
make -f Makefile.rhn-custom-info all

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT
make -f Makefile.rhn-custom-info install PREFIX=$RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_mandir}/man8/
install -m 644 rhn-custom-info.8 $RPM_BUILD_ROOT%{_mandir}/man8/
%if 0%{?suse_version}
ln -s rhn-custom-info $RPM_BUILD_ROOT/%{_bindir}/mgr-custom-info
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%dir %{_datadir}/rhn
%{_bindir}/*-custom-info
%dir %{_datadir}/rhn/custominfo
%{_datadir}/rhn/custominfo/rhn-custom-info.py*
%doc LICENSE PYTHON-LICENSES.txt
%{_mandir}/man8/rhn-custom-info.*

%changelog
* Fri Apr 15 2011 Jan Pazdziora 5.4.12-1
- build rhn-custom-info on SUSE (mc@suse.de)

* Fri Apr 08 2011 Miroslav Suchý 5.4.11-1
- update copyright years (msuchy@redhat.com)

* Fri Apr 08 2011 Miroslav Suchý 5.4.10-1
- both string and unicode are instance of basestring
- fix rhn-custom-info (mc@suse.de)

* Tue Apr 05 2011 Miroslav Suchý 5.4.9-1
- simplify read_username()
- 683200 - utilize up2date_client.config

* Wed Mar 30 2011 Miroslav Suchý 5.4.8-1
- no need to support rhel2
- Updating the copyright years to include 2010.

* Wed Dec 08 2010 Michael Mraka <michael.mraka@redhat.com> 5.4.7-1
- import Fault, ResponseError and ProtocolError directly from xmlrpclib

* Thu Nov 25 2010 Miroslav Suchý <msuchy@redhat.com> 5.4.6-1
- fix failing build in F13 (msuchy@redhat.com)

* Fri Nov 19 2010 Miroslav Suchý <msuchy@redhat.com> 5.4.5-1
- 553649 - we need to require X.Y version due to search path

* Thu Nov 18 2010 Miroslav Suchý <msuchy@redhat.com> 5.4.4-1
- 553649 - Requires correct, justified where necessary
- 553649 - fix changelog format

* Mon Oct 04 2010 Michael Mraka <michael.mraka@redhat.com> 5.4.3-1
- replaced local copy of compile.py with standard compileall module

* Mon Jan 18 2010 Miroslav Suchy <msuchy@redhat.com> 5.4.2-1
- polished spec for Fedora Review

* Fri Jan  8 2010 Miroslav Suchy <msuchy@redhat.com> 5.4.1-1
- added man page
- polished spec for Fedora Review

* Tue Jun 16 2009 Brad Buckingham <bbuckingham@redhat.com> 5.4.0-1
- bumping version (bbuckingham@redhat.com)

* Thu Apr 23 2009 jesus m. rodriguez <jesusr@redhat.com> 0.4.6-1
- update copyright and licenses (jesusr@redhat.com)

* Thu Feb 19 2009 Pradeep Kilambi <pkilambi@redhat.com> 0.4.5-1
- 485459 - constructed url should now point to right handler

* Tue Jan 27 2009 Miroslav Suchý <msuchy@redhat.com> 0.4.4-1
- fix typo in Source0

* Thu Jan 22 2009 Dennis Gilmore <dennis@ausil.us> 0.4.3-1
- BuildRequires python
- clean up handling of requires for up2date or yum-rhn-plugin

* Wed Jan 14 2009 Pradeep Kilambi <pkilambi@redhat.com> - 0.4.2-1
- Resolves - #251060

* Thu Sep  4 2008 Pradeep Kilambi <pkilambi@redhat.com> - 0.2.2-1
- adding dist tag

* Wed Mar 07 2007 Pradeep Kilambi <pkilambi@redhat.com> 5.0.0-1
- adding dist tag

* Mon May 17 2004 Bret McMillan <bretm@redhat.com>
- friendlier commandline usage
- change the executable from rhncustominfo to rhn-custom-info
- use up2date's config settings

* Mon Sep 24 2003 Bret McMillan <bretm@redhat.com>
- Initial build
