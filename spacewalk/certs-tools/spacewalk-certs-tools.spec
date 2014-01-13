
# needsbinariesforbuild

# package renaming fun :(
%define rhn_client_tools spacewalk-client-tools
%define rhn_setup	 spacewalk-client-setup
%define rhn_check	 spacewalk-check
%define rhnsd		 spacewalksd
#
Name: spacewalk-certs-tools
Summary: Spacewalk SSL Key/Cert Tool
Group: Applications/Internet
License: GPLv2
Version: 1.7.3.10
Release: 1%{?dist}
URL:      https://fedorahosted.org/spacewalk
Source0:  https://fedorahosted.org/releases/s/p/spacewalk/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
%if 0%{?suse_version}
Requires: openssl rpm
# put our new bootstrap rpm on the appliance
BuildRequires: sm-client-tools
%else
Requires: openssl rpm-build
%endif
%if 0%{?suse_version} || 0%{?rhel} >= 5
Requires: %{rhn_client_tools}
%endif
Requires: spacewalk-backend-libs >= 0.8.28
Requires: sudo
BuildRequires: docbook-utils
%if 0%{?suse_version}
BuildRequires: filesystem
%endif
BuildRequires: python
Obsoletes: rhns-certs < 5.3.0
Obsoletes: rhns-certs-tools < 5.3.0
# can not provides = %{version} since some old packages expect > 3.6.0
Provides:  rhns-certs = 5.3.0
Provides:  rhns-certs-tools = 5.3.0

%description
This package contains tools to generate the SSL certificates required by
Spacewalk.

%global rhnroot %{_datadir}/rhn

%prep
%setup -q

%build
#nothing to do here

%install
rm -rf $RPM_BUILD_ROOT
install -d -m 755 $RPM_BUILD_ROOT/%{rhnroot}/certs
%if 0%{?suse_version}
make PUB_BOOTSTRAP_DIR=/srv/www/htdocs/pub/bootstrap -f Makefile.certs install PREFIX=$RPM_BUILD_ROOT ROOT=%{rhnroot} \
    MANDIR=%{_mandir}

ln -s rhn-bootstrap $RPM_BUILD_ROOT/%{_bindir}/mgr-bootstrap
ln -s rhn-ssl-tool $RPM_BUILD_ROOT/%{_bindir}/mgr-ssl-tool
ln -s rhn-sudo-ssl-tool $RPM_BUILD_ROOT/%{_bindir}/mgr-sudo-ssl-tool
ln -s spacewalk-push-register $RPM_BUILD_ROOT/%{_sbindir}/mgr-push-register
ln -s spacewalk-ssh-push-init $RPM_BUILD_ROOT/%{_sbindir}/mgr-ssh-push-init

# fetch sm-client-tools and put it in the bootstrap dir
install -m 0644 /.build.binaries/sm-client-tools.rpm $RPM_BUILD_ROOT/srv/www/htdocs/pub/bootstrap/

%py_compile %{buildroot}/%{rhnroot}
%py_compile -O %{buildroot}/%{rhnroot}

%else
make -f Makefile.certs install PREFIX=$RPM_BUILD_ROOT ROOT=%{rhnroot} \
    MANDIR=%{_mandir}
%endif
chmod 755 $RPM_BUILD_ROOT/%{rhnroot}/certs/{rhn_ssl_tool.py,client_config_update.py,rhn_bootstrap.py}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%dir %{rhnroot}/certs
%{rhnroot}/certs/*.py*
%attr(755,root,root) %{rhnroot}/certs/sign.sh
%attr(755,root,root) %{rhnroot}/certs/gen-rpm.sh
%attr(755,root,root) %{_bindir}/rhn-sudo-ssl-tool
%attr(755,root,root) %{_bindir}/rhn-ssl-tool
%attr(755,root,root) %{_bindir}/rhn-bootstrap
%attr(755,root,root) %{_sbindir}/spacewalk-push-register
%attr(755,root,root) %{_sbindir}/spacewalk-ssh-push-init
%doc %{_mandir}/man1/rhn-*.1*
%doc LICENSE
%doc ssl-howto-simple.txt ssl-howto.txt
%if 0%{?suse_version}
%dir /srv/www/htdocs/pub
%dir /srv/www/htdocs/pub/bootstrap
%dir /usr/share/rhn
/srv/www/htdocs/pub/bootstrap/client_config_update.py*
/srv/www/htdocs/pub/bootstrap/sm-client-tools.rpm
%{_bindir}/mgr-bootstrap
%{_bindir}/mgr-ssl-tool
%{_bindir}/mgr-sudo-ssl-tool
%{_sbindir}/mgr-push-register
%{_sbindir}/mgr-ssh-push-init
%else
%{_var}/www/html/pub/bootstrap/client_config_update.py*
%endif


%changelog
* Fri Mar 02 2012 Jan Pazdziora 1.7.3-1
- Update the copyright year info.

* Thu Feb 23 2012 Michael Mraka <michael.mraka@redhat.com> 1.7.2-1
- we are now just GPL

* Fri Feb 10 2012 Michael Mraka <michael.mraka@redhat.com> 1.7.1-1
- code cleanup

* Wed Dec 21 2011 Milan Zazrivec <mzazrivec@redhat.com> 1.6.7-1
- update copyright info

* Wed Oct 19 2011 Michael Mraka <michael.mraka@redhat.com> 1.6.6-1
- removed dead function getCertValidityRange()
- removed dead function getCertValidityDates()
- removed dead function getExistingOverridesConfig()

* Fri Sep 30 2011 Jan Pazdziora 1.6.5-1
- 689939 - allow rhn-ssl-tool to work with --set-hostname='*.example.com'.

* Wed Aug 24 2011 Miroslav Suchý 1.6.4-1
- if subjectAltName is used, hostname must be present in dNSName

* Tue Aug 23 2011 Miroslav Suchý 1.6.3-1
- do not fail if --set-cname is not specified

* Mon Aug 22 2011 Miroslav Suchý 1.6.2-1
- ability to generate multihost ssl certificate

* Fri Aug 19 2011 Miroslav Suchý 1.6.1-1
- code cleanup

* Tue Jul 19 2011 Jan Pazdziora 1.5.3-1
- Updating the copyright years.

* Fri May 20 2011 Michael Mraka <michael.mraka@redhat.com> 1.5.2-1
- 704979 - use https:// for fetching org ca cert

* Fri Apr 15 2011 Jan Pazdziora 1.5.1-1
- support zypper in bootstrap script and allow multiple GPG keys (mc@suse.de)

* Fri Apr 08 2011 Miroslav Suchý 1.4.1-1
- Bumping package versions for 1.4 (tlestach@redhat.com)
- updating Copyright years for year 2011 (tlestach@redhat.com)

* Tue Jan 04 2011 Michael Mraka <michael.mraka@redhat.com> 1.3.2-1
- fixed rpmlint errors
- Updating the copyright years to include 2010.

* Wed Nov 24 2010 Michael Mraka <michael.mraka@redhat.com> 1.3.1-1
- removed unused imports

* Tue Nov 02 2010 Jan Pazdziora 1.2.2-1
- Update copyright years in the rest of the repo.

* Mon Oct 04 2010 Michael Mraka <michael.mraka@redhat.com> 1.2.1-1
- replaced local copy of compile.py with standard compileall module
- removed dead code

* Mon Apr 19 2010 Michael Mraka <michael.mraka@redhat.com> 1.1.1-1
- bumping spec files to 1.1 packages

* Tue Apr 13 2010 Jan Pazdziora 0.9.2-1
- Use tempfile.TemporaryFile and os.path.abspath, to avoid the need for
  spacewalk.common.fileutils in client_config_update.py.

* Wed Feb 24 2010 Michael Mraka <michael.mraka@redhat.com> 0.9.1-1
- 567271 - fixed import

* Thu Feb 04 2010 Michael Mraka <michael.mraka@redhat.com> 0.8.7-1
- updated copyrights

* Mon Jan 25 2010 Michael Mraka <michael.mraka@redhat.com> 0.8.6-1
- dead code / imports

* Fri Jan 15 2010 Michael Mraka <michael.mraka@redhat.com> 0.8.5-1
- fixed build error

* Thu Jan 14 2010 Michael Mraka <michael.mraka@redhat.com> 0.8.4-1
- removed duplicated code

* Mon Dec 14 2009 Michael Mraka <michael.mraka@redhat.com> 0.8.3-1
- fixed namespace of rhn_rpm
- removed dead code

* Mon Dec 07 2009 Michael Mraka <michael.mraka@redhat.com> 0.8.2-1
- moved code from rhnlib to spacewalk-backend-libs

* Fri Dec 04 2009 Michael Mraka <michael.mraka@redhat.com> 0.8.1-1
- rhn_rpm/rhn_mpm moved to rhnlib
- bumping Version to 0.8.0

* Wed Nov 18 2009 Miroslav Suchý <msuchy@redhat.com> 0.7.2-1
- 538046 - Polish the spec according Fedora Packaging Guidelines

* Tue Nov 17 2009 Miroslav Suchy <msuchy@redhat.com> 0.7.1-1
- fix rpmlint warnings

* Wed May 06 2009 jesus m. rodriguez <jesusr@redhat.com> 0.6.3-1
- adding optional way to specify profile name. (satoru.satoh@gmail.com)
- 497110 - Don't assume jabberd is installed in rhn-ssl-tool (dgoodwin@redhat.com)

* Thu Apr 23 2009 jesus m. rodriguez <jesusr@redhat.com> 0.6.2-1
- 465622 - setup config file deployment when it's due (mzazrivec@redhat.com)

* Wed Apr 22 2009 jesus m. rodriguez <jesusr@redhat.com> 0.6.1-1
- bump Versions to 0.6.0 (jesusr@redhat.com)
- update copyright and licenses (jesusr@redhat.com)

* Fri Mar 27 2009 Devan Goodwin <dgoodwin@redhat.com> 0.5.5-1
- Update for new jabberd cert location, and possiblity of jabber user instead of jabberd.

* Wed Mar 25 2009 Jan Pazdziora 0.5.4-1
- 491687 - wrapper around sudo /usr/bin/rhn-ssl-tool, to change SELinux domain

* Fri Mar 13 2009 Miroslav Suchy <msuchy@redhat.com> 0.5.3-1
- put Provides to satisfy older Proxies

* Thu Feb 05 2009 jesus m. rodriguez <jesusr@redhat.com> 0.5.2-1
- replace "!#/usr/bin/env python" with "!#/usr/bin/python"

* Mon Jan 19 2009 Jan Pazdziora 0.5.1-1
- rebuilt for 0.5, after repository reorg

* Tue Dec  9 2008 Michael Mraka <michael.mraka@redhat.com> 0.4.2-1
- fixed Obsoletes: rhns-* < 5.3.0

* Tue Sep 23 2008 Milan Zazrivec 0.3.1-1
- fixed package obsoletes

* Tue Sep  2 2008 Milan Zazrivec 0.2.2-1
- Bumped version for tag-release

* Tue Aug 18 2008 Mike McCune <mmccune@redhat.com> 0.2-1
- get rid of python-optik

* Tue Aug  5 2008 Miroslav Suchy <msuchy@redhat.com> 0.2-0
- Rename to spacewalk-certs-tools
- clean up spec

* Mon Aug  4 2008 Jan Pazdziora 0.1-1
- removed version and sources files

* Wed May 28 2008 Jan Pazdziora 5.2.0-2
- fix for padding L on RHEL 5

* Wed May 21 2008 Jan Pazdziora - 5.2.0-1
- rebuild in dist-cvs.

* Wed Mar 07 2007 Pradeep Kilambi <pkilambi@redhat.com> - 5.0.0-1
- adding dist tag

* Fri Dec 01 2006 Ryan Newberry <rnewberr@redhat.com>
- adding docbook2man to build requires

* Mon Dec 20 2004 Todd Warner <taw@redhat.com> 3.6.0
- requirement added: python-optik (bug: 143413)

* Tue Jul 06 2004 Todd Warner <taw@redhat.com>
- rhn-bootstrap and associated files added.

* Tue Apr 20 2004 Todd Warner <taw@redhat.com>
- added rhn-ssl-tool and associated modules
- using a Makefile which builds a tarball now.
- added man page
- added __init__.py*
- GPLed this code. No reason to do otherwise.

* Tue Aug 20 2002 Cristian Gafton <gafton@redhat.com>
- update for the new build system

* Tue May 21 2002 Cristian Gafton <gafton@redhat.com>
- no more RHNS

* Tue May 14 2002 Todd Warner <taw@redhat.com>
- Initial.
