Name:		spacewalk-oscap
Version:	0.0.4.6
Release:	1%{?dist}
Summary:	OpenSCAP plug-in for rhn-check

Group:		Applications/System
License:	GPLv2
URL:		https://fedorahosted.org/spacewalk
Source0:	https://fedorahosted.org/releases/s/p/spacewalk/%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch
BuildRequires:	python-devel
BuildRequires:	rhnlib
Requires:	openscap-utils >= 0.8.0
Requires:	libxslt
Requires:       rhnlib
Requires:       rhn-check
%description
spacewalk-oscap is a plug-in for rhn-check. With this plugin, user is able
to run OpenSCAP scan from Spacewalk or RHN Satellite server.

%prep
%setup -q


%build
make -f Makefile.spacewalk-oscap


%install
rm -rf $RPM_BUILD_ROOT
make -f Makefile.spacewalk-oscap install PREFIX=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%dir %{_datadir}/openscap
%dir %{_datadir}/openscap/xsl
%dir %{_datadir}/rhn
%dir %{_datadir}/rhn/actions
%dir /etc/sysconfig/rhn
%dir /etc/sysconfig/rhn/clientCaps.d/
%config  /etc/sysconfig/rhn/clientCaps.d/scap
%{_datadir}/rhn/actions/scap.*
%{_datadir}/openscap/xsl/xccdf-resume.xslt


%changelog
* Wed Feb 29 2012 Simon Lukasik <slukasik@redhat.com> 0.0.4-1
- Send capabilities to server. (slukasik@redhat.com)

* Tue Feb 28 2012 Simon Lukasik <slukasik@redhat.com> 0.0.3-1
- Do not unlink file, tempfile will do that automatically.
  (slukasik@redhat.com)
- This module is not supposed to be used as a stand-alone script.
  (slukasik@redhat.com)
- Do submit empty dict, when something goes wrong (slukasik@redhat.com)
- Fix syntax for python 2.4 (slukasik@redhat.com)

* Mon Feb 27 2012 Simon Lukasik <slukasik@redhat.com> 0.0.2-1
- new package built with tito

