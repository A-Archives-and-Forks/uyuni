Summary: Support package for spacewalk koan interaction
Name: spacewalk-koan
Group: System Environment/Kernel
License: GPLv2
Source0: https://fedorahosted.org/releases/s/p/spacewalk/%{name}-%{version}.tar.gz
Version: 0.2.20
Release: 1%{?dist}
BuildArch : noarch
URL:            https://fedorahosted.org/spacewalk
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch:      noarch
BuildRequires:  python
Requires:       python >= 1.5
Requires:       koan >= 1.4.3
%if 0%{?suse_version}
# provide directories for filelist check in OBS
BuildRequires: rhn-client-tools
Requires:       rhn-virtualization-common
Requires:       rhn-virtualization-host
%endif
Conflicts: rhn-kickstart
Conflicts: rhn-kickstart-common
Conflicts: rhn-kickstart-virtualization

#this currently doesn't work for RHEL 2.1
%if 0%{?rhel} && 0%{?rhel} < 5
Requires: up2date
%else
Requires: rhn-check
%endif

%description
Support package for spacewalk koan interaction.

%prep
%setup -q

%build
make -f Makefile.spacewalk-koan all

%install
rm -rf $RPM_BUILD_ROOT
make -f Makefile.spacewalk-koan install PREFIX=$RPM_BUILD_ROOT ROOT=%{_datadir}/rhn/ \
    MANDIR=%{_mandir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%config(noreplace)  %{_sysconfdir}/sysconfig/rhn/clientCaps.d/kickstart
%{_sbindir}/*
%{_datadir}/rhn/spacewalkkoan/
%{_datadir}/rhn/actions/

%changelog
* Mon Jul 11 2011 Jan Pazdziora 0.2.20-1
- 691417 - allow extra whitespace behing nameserver IP in resolv.conf
  (tlestach@redhat.com)

* Fri May 27 2011 Jan Pazdziora 0.2.19-1
- 687850 - guest provisioning: correct block device detection
  (mzazrivec@redhat.com)

* Fri Apr 15 2011 Jan Pazdziora 0.2.18-1
- build spacewalk-koan on SUSE (mc@suse.de)

* Fri Apr 08 2011 Miroslav Suchý 0.2.17-1
- update copyright years (msuchy@redhat.com)

* Wed Feb 02 2011 Tomas Lestach <tlestach@redhat.com> 0.2.16-1
- Fixed typo in import subprocess (mmello@redhat.com)

* Tue Nov 02 2010 Jan Pazdziora 0.2.15-1
- Update copyright years in the rest of the repo.

* Fri Oct 29 2010 Michael Mraka <michael.mraka@redhat.com> 0.2.14-1
- spacewalk-koan should conflict with all rhn-kickstart subpackages

* Mon Oct 25 2010 Jan Pazdziora 0.2.13-1
- 645795 - changing spaceawlk-koan to use subproccess only if it is available
  and to fall back to popen2 if its not, this enables RHEL 4 support again
  (jsherril@redhat.com)

* Wed Oct 20 2010 Michael Mraka <michael.mraka@redhat.com> 0.2.12-1
- must not provide & conflict with same (unversioned) package

* Mon Oct 18 2010 Jan Pazdziora 0.2.11-1
- spacewalk-koan conflicts with any version of rhn-kickstart
  (michael.mraka@redhat.com)

* Mon Oct 18 2010 Jan Pazdziora 0.2.10-1
- 642629 - Disabling the defualt grubby copying behaviour in koan for args
  (paji@redhat.com)

* Mon Oct 04 2010 Michael Mraka <michael.mraka@redhat.com> 0.2.9-1
- replaced local copy of compile.py with standard compileall module

* Fri Sep 24 2010 Justin Sherrill <jsherril@redhat.com> 0.2.8-1
- 637273 - fixing error with reprovisiong (unexpected keyword argument
  cache_only) (jsherril@redhat.com)

* Tue Jul 20 2010 Miroslav Suchý <msuchy@redhat.com> 0.2.7-1
- add parameter cache_only to all client actions (msuchy@redhat.com)

* Thu Jul 01 2010 Miroslav Suchý <msuchy@redhat.com> 0.2.6-1
- initializing variable within koan that is not initialized
  (jsherril@redhat.com)

* Thu Feb 04 2010 Michael Mraka <michael.mraka@redhat.com> 0.2.5-1
- updated copyrights

* Fri Jan 29 2010 Miroslav Suchý <msuchy@redhat.com> 0.2.4-1
- replaced popen2 with subprocess in client (michael.mraka@redhat.com)

* Wed Nov 25 2009 Miroslav Suchý <msuchy@redhat.com> 0.2.3-1
- import virtualization module in kickstart_guest section (mzazrivec@redhat.com)
- 532429 - refresh virt. state after successful guest kickstart (mzazrivec@redhat.com)
- 530553 - wait for virt. domain installation to finish and restart (mzazrivec@redhat.com)

* Fri Aug 28 2009 Michael Mraka <michael.mraka@redhat.com> 0.2.2-1
- grep | awk is rarely needed
- 517876 - fixing spacewalk-koan so it doesnt require up2date on Fedora 11

* Tue Jul 21 2009 John Matthews <jmatthew@redhat.com> 0.1.17-1
- 510299 - static ks fix. (paji@redhat.com)
- 510299 - Big commit to get static networking to work (paji@redhat.com)

* Mon Jul 06 2009 John Matthews <jmatthew@redhat.com> 0.1.16-1
- 508956 - fixing file preservation to actually use updated initrd.img
  (mmccune@gibson.pdx.redhat.com)

* Thu Jun 25 2009 John Matthews <jmatthew@redhat.com> 0.1.15-1
- fixing spacewalk-koan spec file to build for 2.1 properly
  (jsherril@redhat.com)
- 497571 - switching to python 1.5 requires since we have to support 2.1
  (mmccune@gmail.com)
- 497571 - switch from True/False to 0/1 to support rhel 2.1 and
  (mmccune@gmail.com)
- 503996 - Added some information on the error message to the status returned
  to the server. (jason.dobies@redhat.com)

* Thu May 21 2009 jesus m. rodriguez <jesusr@redhat.com> 0.1.14-1
- 497424 - Slight redesign of the KS Virt UI to deal with duplicate virt paths (paji@redhat.com)

* Wed May 06 2009 jesus m. rodriguez <jesusr@redhat.com> 0.1.13-1
- 497871 - fixing issue where guest provisioning would show as succesful even
  when it had failed (jsherril@redhat.com)

* Wed Apr 22 2009 jesus m. rodriguez <jesusr@redhat.com> 0.1.12-1
- 494976 - adding cobbler system record name usage to reprovisioning (jsherril@redhat.com)
- update copyright and licenses (jesusr@redhat.com)

* Wed Mar 18 2009 Mike McCune <mmccune@gmail.com> 0.1.11-1
- 486186 - Update spacewalk spec files to require koan >= 1.4.3

* Thu Feb 26 2009 jesus m. rodriguez <jesusr@redhat.com> 0.1.10-1
- 486638- Updated spec to have it conflict with rhn-kickstart rpm instead of obsoleting it.

* Wed Feb 18 2009 Dave Parker <dparker@redhat.com> 0.1.9-1
- 486186 - Update spacewalk spec files to require cobbler >= 1.4.2

* Tue Feb 10 2009 Mike McCune <mmccune@gmail.com> 0.1.8-1
- 484793: Adde a basic setter to get rid of embed_kickstart check on koan

* Mon Jan 26 2009 Mike McCune <mmccune@gmail.com> 0.1.7-1
- spec file cleanups

* Tue Jan 13 2009 Mike McCune <mmccune@gmail.com> 0.1.6-1
- 461162 - missing var for koan

* Mon Jan 12 2009 Mike McCune <mmccune@gmail.com> 0.1.5-1
- 461162 - get the virtualization provisioning tracking system to work with a :virt system record.
- 461162 - Quick fix to get spacewalk koan going with a ks....

* Thu Jan 08 2009 Mike McCune <mmccune@gmail.com> 0.1.3-1
- minor virt fixes
* Tue Dec 23 2008 Mike McCune <mmccune@gmail.com> 0.1.2-1
- tagging release with support for virt
* Tue Nov 25 2008 Mike McCune - 0.1.1-1
- tagging release
* Tue Oct 28 2008 Mike McCune - 1.0.0-1
- Initial creation.
