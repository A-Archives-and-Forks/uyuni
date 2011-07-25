Summary: Spacewalk packages yum repository configuration
Name: spacewalk-repo
Version: 1.6
Release: 1%{?dist}
License: GPLv2
Group: System Environment/Base
# This src.rpm is cannonical upstream
# You can obtain it using this set of commands
# git clone git://git.fedorahosted.org/git/spacewalk.git/
# cd spec-tree/spacewalk-repo
# make test-srpm
URL:          https://fedorahosted.org/spacewalk
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch: noarch

%description
This package contains the Spacewalk repository configuration for yum.

%package -n spacewalk-client-repo
Summary: Spacewalk client packages yum repository configuration
Group: System Environment/Base

%description -n spacewalk-client-repo
This package contains the Spacewalk repository configuration for yum.

%prep
mkdir -p $RPM_BUILD_ROOT

%build

%install
rm -rf $RPM_BUILD_ROOT

# some sane default value
%define reposubdir      RHEL/%{rhel}
# redefine on fedora
%{?fedora: %define reposubdir      Fedora/%{fedora}}

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d
cat >>$RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d/spacewalk.repo <<REPO
[spacewalk]
name=Spacewalk
baseurl=http://spacewalk.redhat.com/yum/%{version}/%{reposubdir}/\$basearch/
gpgkey=http://spacewalk.redhat.com/yum/RPM-GPG-KEY-spacewalk-2010
enabled=1
gpgcheck=1
REPO

cat >>$RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d/spacewalk-client.repo <<REPO
[spacewalk-client]
name=Spacewalk Client Tools
baseurl=http://spacewalk.redhat.com/yum/%{version}-client/%{reposubdir}/\$basearch/
gpgkey=http://spacewalk.redhat.com/yum/RPM-GPG-KEY-spacewalk-2010
enabled=1
gpgcheck=1
REPO

cat >>$RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d/spacewalk-source.repo <<REPO
[spacewalk-source]
name=Spacewalk SRPMS
baseurl=http://spacewalk.redhat.com/source/%{version}/%{reposubdir}/
gpgkey=http://spacewalk.redhat.com/yum/RPM-GPG-KEY-spacewalk-2010
enabled=0
gpgcheck=1
REPO

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%dir %{_sysconfdir}/yum.repos.d
%config %{_sysconfdir}/yum.repos.d/spacewalk.repo
%config %{_sysconfdir}/yum.repos.d/spacewalk-source.repo

%files -n spacewalk-client-repo
%defattr(-,root,root,-)
%config %{_sysconfdir}/yum.repos.d/spacewalk-client.repo

%changelog
* Mon Apr 11 2011 Miroslav Suchý 1.5-1
- bump up version for Spacewalk 1.5

* Wed Feb 02 2011 Tomas Lestach <tlestach@redhat.com> 1.4-1
- Bumping spacewalk-repo package version for 1.4

* Mon Jan 31 2011 Tomas Lestach <tlestach@redhat.com> 1.3-1
- enable rhel6 repo (tlestach@redhat.com)

* Mon Nov 15 2010 Jan Pazdziora 1.3-0
- Bumping up version for 1.3.

* Wed Aug 18 2010 Jan Pazdziora 1.2-0
- point the repos to new spacewalk gpg key

* Tue Aug 10 2010 Milan Zazrivec <mzazrivec@redhat.com> 1.1-2
- add spacewalk-source.repo to .spec

* Tue Aug 10 2010 Milan Zazrivec <mzazrivec@redhat.com> 1.1-1
- prepare for 1.1
- Define yum repo for source rpms

* Thu Feb 11 2010 Michael Mraka <michael.mraka@redhat.com> 0.9-1
- pointed to Spacewalk 0.9 repo

* Thu Feb 11 2010 Michael Mraka <michael.mraka@redhat.com> 0.8-1
- pointed to Spacewalk 0.8 repo

* Fri Nov 27 2009 Miroslav Suchý <msuchy@redhat.com> 0.7-4
- create subpackage spacewalk-client-repo

* Fri Oct 16 2009 Michael Mraka <michael.mraka@redhat.com> 0.7-3
- fixed version of spacewalk-repo

* Mon Aug 10 2009 jesus m. rodriguez 0.7.0-2
- rename rhel to RHEL
- rename fedora to Fedora
- remove Server from 5Server

* Thu Apr 30 2009 Jan Pazdziora 0.6-1
- bump version to 0.6

* Tue Mar 31 2009 jesus m. rodriguez <jesusr@redhat.com> 0.5.2-1
- rebuilding for 0.5

* Thu Jan 15 2009 Jan Pazdziora 0.4-1
- building new version to point to 0.4 repo

* Fri Oct 24 2008 Michael Mraka <michael.mraka@redhat.com> 0.3-1
- Initial release
