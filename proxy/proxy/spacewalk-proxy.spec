Name: spacewalk-proxy
Summary: Spacewalk Proxy Server
Group:   Applications/Internet
License: GPLv2
URL:     https://fedorahosted.org/spacewalk
Source0: https://fedorahosted.org/releases/s/p/spacewalk/%{name}-%{version}.tar.gz
Version: 1.6.5
Release: 1%{?dist}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: python
%if 0%{?suse_version}
BuildRequires: apache2
%endif
BuildArch: noarch
Requires: httpd

%define rhnroot %{_usr}/share/rhn
%define destdir %{rhnroot}/proxy
%define rhnconf %{_sysconfdir}/rhn
%if 0%{?suse_version}
%define httpdconf %{_sysconfdir}/apache2/conf.d
%define apache_user wwwrun
%define apache_group www
%else
%define httpdconf %{_sysconfdir}/httpd/conf.d
%define apache_user apache
%define apache_group apache
%endif

%description
This package is never built.

%package management
Summary: Packages required by the Spacewalk Management Proxy
Group:   Applications/Internet
Requires: squid
Requires: spacewalk-backend >= 1.2.32
# python-hashlib is optional for spacewalk-backend-libs
# but we need made it mandatory here
%if ! 0%{?suse_version}
Requires: python-hashlib
Requires: sos
Requires(preun): initscripts
Requires: spacewalk-proxy-selinux
%endif
Requires: %{name}-broker = %{version}
Requires: %{name}-redirect = %{version}
Requires: %{name}-common >= %{version}
Requires: %{name}-docs
Requires: %{name}-html
Requires: jabberd spacewalk-setup-jabberd
Requires: httpd
Obsoletes: rhns-proxy < 5.3.0
Obsoletes: rhns-proxy-management < 5.3.0
BuildRequires: /usr/bin/docbook2man
Obsoletes: rhns-proxy-tools < 5.3.0
Provides: rhns-proxy-tools = 5.3.0
Obsoletes: spacewalk-proxy-tools < 0.5.3
Provides: spacewalk-proxy-tools = %{version}
Obsoletes: rhns-auth-daemon < 5.2.0
Provides: rhns-auth-daemon = 1:%{version}
Obsoletes: rhn-modssl < 2.9.0
Provides: rhn-modssl = 1:%{version}
Obsoletes: rhn-modpython < 2.8.0
Provides: rhn-modpython = 1:%{version}
Obsoletes: rhn-apache < 1.4.0
Provides: rhn-apache = 1:%{version}

%description management
This package require all needed packages for Spacewalk Proxy Server.

%package broker
Group:   Applications/Internet
Summary: The Broker component for the Spacewalk Proxy Server
Requires: squid
Requires: spacewalk-certs-tools
Requires: spacewalk-proxy-package-manager
Requires: spacewalk-ssl-cert-check
Requires: httpd
%if 0%{?suse_version}
Requires: apache2-prefork
%else
Requires: mod_ssl
%endif
%if  0%{?rhel} && 0%{?rhel} < 6
Requires: mod_python
%else
Requires: mod_wsgi
%endif
Requires(post): %{name}-common
Conflicts: %{name}-redirect < %{version}-%{release}
Conflicts: %{name}-redirect > %{version}-%{release}
# We don't want proxies and satellites on the same box
Conflicts: rhns-satellite-tools
Obsoletes: rhns-proxy-broker < 5.3.0


%description broker
The Spacewalk Proxy Server allows package caching
and local package delivery services for groups of local servers from
Spacewalk Server. This service adds flexibility and economy of
resources to package update and deployment.

This package includes module, which request is cache-able and should
be sent to Squid and which should be sent directly to parent Spacewalk
server.

%package redirect
Group:   Applications/Internet
Summary: The SSL Redirect component for the Spacewalk Proxy Server
Requires: spacewalk-proxy-broker = %{version}-%{release}
Requires: httpd
Obsoletes: rhns-proxy-redirect < 5.3.0

%description redirect
The Spacewalk Proxy Server allows package caching
and local package delivery services for groups of local servers from
Spacewalk Server. This service adds flexibility and economy of
resources to package update and deployment.

This package includes module, which handle request passed through squid
and assures a fully secure SSL connection is established and maintained
between an Spacewalk Proxy Server and parent Spacewalk server.

%package common
Group:   Applications/Internet
Summary: Modules shared by Spacewalk Proxy components
%if 0%{?suse_version}
Requires: apache2-prefork
%else
Requires: mod_ssl
%endif
%if  0%{?rhel} && 0%{?rhel} < 6
Requires: mod_python
%else
Requires: mod_wsgi
%endif
Requires: %{name}-broker >= %{version}
Requires: spacewalk-backend >= 1.2.32
Requires: policycoreutils
Obsoletes: rhns-proxy-common < 5.3.0

%description common
The Spacewalk Proxy Server allows package caching
and local package delivery services for groups of local servers from
Spacewalk Server. This service adds flexibility and economy of
resources to package update and deployment.

This package contains the files shared by various
Spacewalk Proxy components.

%package package-manager
Summary: Custom Channel Package Manager for the Spacewalk Proxy Server
Group:   Applications/Internet
Requires: spacewalk-backend >= 1.2.32
Requires: rhnlib
Requires: python
Requires: rhnpush
BuildRequires: /usr/bin/docbook2man
BuildRequires: python-devel
Obsoletes: rhn_package_manager < 5.3.0
Obsoletes: rhns-proxy-package-manager < 5.3.0

%description package-manager
The Spacewalk Proxy Server allows package caching
and local package delivery services for groups of local servers from
Spacewalk Server. This service adds flexibility and economy of
resources to package update and deployment.

This package contains the Command rhn_package_manager, which  manages
an Spacewalk Proxy Server's custom channel.

%prep
%setup -q

%build
make -f Makefile.proxy

%install
rm -rf $RPM_BUILD_ROOT
make -f Makefile.proxy install PREFIX=$RPM_BUILD_ROOT
install -d -m 750 $RPM_BUILD_ROOT/%{_var}/cache/rhn/proxy-auth

mkdir -p $RPM_BUILD_ROOT/%{_var}/spool/rhn-proxy/list

touch $RPM_BUILD_ROOT/%{httpdconf}/cobbler-proxy.conf

%if  0%{?rhel} && 0%{?rhel} < 6
rm -fv $RPM_BUILD_ROOT%{httpdconf}/spacewalk-proxy-wsgi.conf
rm -rfv $RPM_BUILD_ROOT%{rhnroot}/wsgi/
%else
rm -fv $RPM_BUILD_ROOT%{httpdconf}/spacewalk-proxy-python.conf
%endif

ln -sf rhn-proxy $RPM_BUILD_ROOT%{_sbindir}/spacewalk-proxy

%clean
rm -rf $RPM_BUILD_ROOT

%post broker
if [ -f %{_sysconfdir}/sysconfig/rhn/systemid ]; then
    chown root.%{apache_group} %{_sysconfdir}/sysconfig/rhn/systemid
    chmod 0640 %{_sysconfdir}/sysconfig/rhn/systemid
fi
%if 0%{?suse_version}
/sbin/service apache2 try-restart > /dev/null 2>&1
%else
/sbin/service httpd condrestart > /dev/null 2>&1
%endif

# In case of an upgrade, get the configured package list directory and clear it
# out.  Don't worry; it will be rebuilt by the proxy.

RHN_CONFIG_PY=%{rhnroot}/common/rhnConfig.py
RHN_PKG_DIR=%{_var}/spool/rhn-proxy

if [ -f $RHN_CONFIG_PY ] ; then

    # Check whether the config command supports the ability to retrieve a
    # config variable arbitrarily.  Versions of  < 4.0.6 (rhn) did not.

    python $RHN_CONFIG_PY proxy.broker > /dev/null 2>&1
    if [ $? -eq 1 ] ; then
        RHN_PKG_DIR=$(python $RHN_CONFIG_PY get proxy.broker pkg_dir)
    fi
fi

rm -rf $RHN_PKG_DIR/list/*

# Make sure the scriptlet returns with success
exit 0

%post common
%if 0%{?suse_version}
sysconf_addword /etc/sysconfig/apache2 APACHE_MODULES wsgi
sysconf_addword /etc/sysconfig/apache2 APACHE_MODULES proxy
sysconf_addword /etc/sysconfig/apache2 APACHE_MODULES rewrite
sysconf_addword /etc/sysconfig/apache2 APACHE_SERVER_FLAGS SSL
%endif

%post redirect
%if 0%{?suse_version}
/sbin/service apache2 try-restart > /dev/null 2>&1
%else
/sbin/service httpd condrestart > /dev/null 2>&1
%endif
# Make sure the scriptlet returns with success
exit 0

%post management
# The spacewalk-proxy-management package is also our "upgrades" package.
# We deploy new conf from configuration channel if needed
# we deploy new conf only if we install from webui and conf channel exist
if rhncfg-client verify %{_sysconfdir}/rhn/rhn.conf 2>&1|grep 'Not found'; then
     %{_bindir}/rhncfg-client get %{_sysconfdir}/rhn/rhn.conf
fi > /dev/null 2>&1
if rhncfg-client verify %{_sysconfdir}/squid/squid.conf | grep -E '(modified|missing)'; then
    rhncfg-client get %{_sysconfdir}/squid/squid.conf
    rm -rf %{_var}/spool/squid/*
    %{_usr}/sbin/squid -z
    /sbin/service squid condrestart
fi > /dev/null 2>&1

exit 0

%preun broker
if [ $1 -eq 0 ] ; then
    # nuke the cache
    rm -rf %{_var}/cache/rhn/*
fi

%preun
if [ $1 = 0 ] ; then
%if 0%{?suse_version}
    /sbin/service apache2 try-restart > /dev/null 2>&1
%else
    /sbin/service httpd condrestart > /dev/null 2>&1
%endif
fi

%posttrans common
if [ -n "$1" ] ; then # anything but uninstall
    mkdir /var/cache/rhn/proxy-auth 2>/dev/null
    chown %{apache_user}:root /var/cache/rhn/proxy-auth
    restorecon /var/cache/rhn/proxy-auth
fi


%files broker
%defattr(-,root,root)
%dir %{destdir}
%{destdir}/broker/__init__.py*
%{destdir}/broker/rhnBroker.py*
%{destdir}/broker/rhnRepository.py*
%attr(750,%{apache_user},%{apache_group}) %dir %{_var}/spool/rhn-proxy
%attr(750,%{apache_user},%{apache_group}) %dir %{_var}/spool/rhn-proxy/list
%attr(770,root,%{apache_group}) %dir %{_var}/log/rhn
%config(noreplace) %{_sysconfdir}/logrotate.d/rhn-proxy-broker
# config files
%attr(750,root,%{apache_group}) %dir %{_prefix}/share/rhn/config-defaults
%attr(640,root,%{apache_group}) %{_prefix}/share/rhn/config-defaults/rhn_proxy_broker.conf
%dir /usr/share/rhn
%dir /usr/share/rhn/proxy/broker

%files redirect
%defattr(-,root,root)
%dir %{destdir}
%{destdir}/redirect/__init__.py*
%{destdir}/redirect/rhnRedirect.py*
%attr(770,root,%{apache_group}) %dir %{_var}/log/rhn
%config(noreplace) %{_sysconfdir}/logrotate.d/rhn-proxy-redirect
# config files
%attr(750,root,%{apache_group}) %dir %{_prefix}/share/rhn/config-defaults
%attr(640,root,%{apache_group}) %{_prefix}/share/rhn/config-defaults/rhn_proxy_redirect.conf
%dir /usr/share/rhn
%dir /usr/share/rhn/proxy/redirect

%files common
%defattr(-,root,root)
%dir %{destdir}
%{destdir}/__init__.py*
%{destdir}/apacheServer.py*
%{destdir}/apacheHandler.py*
%{destdir}/rhnShared.py*
%{destdir}/rhnConstants.py*
%{destdir}/responseContext.py*
%{destdir}/rhnAuthCacheClient.py*
%{destdir}/rhnProxyAuth.py*
%{destdir}/rhnAuthProtocol.py*
%attr(750,%{apache_user},%{apache_group}) %dir %{_var}/spool/rhn-proxy
%attr(750,%{apache_user},%{apache_group}) %dir %{_var}/spool/rhn-proxy/list
%attr(770,root,%{apache_group}) %dir %{_var}/log/rhn
# config files
%attr(750,root,%{apache_group}) %dir %{rhnconf}
%attr(640,root,%{apache_group}) %config %{rhnconf}/rhn.conf
%attr(640,root,%{apache_group}) %{_prefix}/share/rhn/config-defaults/rhn_proxy.conf
%attr(640,root,%{apache_group}) %config %{httpdconf}/spacewalk-proxy.conf
# this file is created by either cli or webui installer
%ghost %config %{httpdconf}/cobbler-proxy.conf
%if  0%{?rhel} && 0%{?rhel} < 6
%attr(640,root,%{apache_group}) %config %{httpdconf}/spacewalk-proxy-python.conf
%else
%attr(640,root,%{apache_group}) %config %{httpdconf}/spacewalk-proxy-wsgi.conf
%{rhnroot}/wsgi/xmlrpc.py*
%{rhnroot}/wsgi/xmlrpc_redirect.py*
%endif
# the cache
%attr(750,%{apache_user},root) %dir %{_var}/cache/rhn
%attr(750,%{apache_user},root) %dir %{_var}/cache/rhn/proxy-auth
%dir /usr/share/rhn
%dir /usr/share/rhn/wsgi

%files package-manager
%defattr(-,root,root)
# config files
%attr(750,root,%{apache_group}) %dir %{_prefix}/share/rhn/config-defaults
%attr(640,root,%{apache_group}) %{_prefix}/share/rhn/config-defaults/rhn_proxy_package_manager.conf
%{_bindir}/rhn_package_manager
%{rhnroot}/PackageManager/rhn_package_manager.py*
%{rhnroot}/PackageManager/uploadLib.py*
%{rhnroot}/PackageManager/__init__.py*
%{_mandir}/man8/rhn_package_manager.8.gz
%dir /usr/share/rhn
%dir /usr/share/rhn/PackageManager

%files management
%defattr(-,root,root)
# dirs
%dir %{destdir}
# start/stop script
%attr(755,root,root) %{_sbindir}/rhn-proxy
%{_sbindir}/spacewalk-proxy
# mans
%{_mandir}/man8/rhn-proxy.8*
%dir /usr/share/rhn


%changelog
* Wed Oct 26 2011 Miroslav Suchý 1.6.5-1
- there is no rhn-proxy-debug for some time

* Mon Oct 17 2011 Miroslav Suchý 1.6.4-1
- 719659 - correctly handle getpeername() on IPv6

* Fri Sep 30 2011 Jan Pazdziora 1.6.3-1
- 621531 - move /etc/rhn/default to /usr/share/rhn/config-defaults (proxy).

* Thu Aug 11 2011 Miroslav Suchý 1.6.2-1
- do not mask original error by raise in execption

* Fri Jul 22 2011 Jan Pazdziora 1.6.1-1
- We only support version 5 and newer of RHEL, removing conditions for old
  versions.

* Tue Jul 19 2011 Jan Pazdziora 1.5.11-1
- Updating the copyright years.

* Wed Jul 13 2011 Miroslav Suchý 1.5.10-1
- 720837 - pass /ks handler through Broker

* Mon Jul 11 2011 Miroslav Suchý 1.5.9-1
- optparse is here since python 2.3 - remove optik (msuchy@redhat.com)
- code cleanup

* Fri Jun 17 2011 Miroslav Suchý 1.5.8-1
- 710433 - if we get data chunked, httplib of python will join them, so it is
  not correct to send chunked header when data may not be chunked

* Fri May 20 2011 Michael Mraka <michael.mraka@redhat.com> 1.5.7-1
- merged backend/common/UserDictCase.py into rhnlib/rhn/UserDictCase.py

* Fri May 13 2011 Miroslav Suchý 1.5.6-1
- 695651 - in mod_wsgi the URI is full URI (incl. protocol, hostname...) and
  not just the part beyond / (msuchy@redhat.com)
- 695651 - headers_in under mod_wsgi is dict, which does not have add()
  (msuchy@redhat.com)
- do not call function twice, store it in variable (msuchy@redhat.com)
- 695651 - pass /ty-cksm handler through Broker (msuchy@redhat.com)

* Wed May 11 2011 Miroslav Suchý 1.5.5-1
- 695651 - is_virtual is not exposed in mod_wsgi (msuchy@redhat.com)
- 695651 - pass /ty handler through Broker (tlestach@redhat.com)
- 695651 - pass /download handler through Broker (msuchy@redhat.com)

* Tue May 10 2011 Jan Pazdziora 1.5.4-1
- 678053 - add option --no-session-caching to rhn_package_manager
  (msuchy@redhat.com)

* Wed May 04 2011 Miroslav Suchý 1.5.3-1
- do not import modules through magic

* Tue Apr 19 2011 Miroslav Suchý <msuchy@redhat.com> 1.5.2-1
- 697447 - handle all other request

* Mon Apr 18 2011 Miroslav Suchý 1.5.1-1
- 697447 - pass /rpc/* through broker
- Bumping package versions for 1.5

* Thu Jan 20 2011 Tomas Lestach <tlestach@redhat.com> 1.3.11-1
- updating Copyright years for year 2011 (tlestach@redhat.com)
- remove redundant comment (msuchy@redhat.com)
- convert comment to docstring (msuchy@redhat.com)
- remove redundant comment (msuchy@redhat.com)

* Thu Jan 13 2011 Miroslav Suchý <msuchy@redhat.com> 1.3.10-1
- do not traceback if redirected location do not contain '?'
- fix module name during import
- replace tabs with space to fix indentation

* Tue Jan 04 2011 Michael Mraka <michael.mraka@redhat.com> 1.3.9-1
- fixed pylint errors

* Tue Jan 04 2011 Michael Mraka <michael.mraka@redhat.com> 1.3.8-1
- removed xxmlrpclib
- Updating the copyright years to include 2010.

* Mon Dec 13 2010 Michael Mraka <michael.mraka@redhat.com> 1.3.7-1
- fixed number of errors reported by pylint

* Wed Dec 08 2010 Michael Mraka <michael.mraka@redhat.com> 1.3.6-1
- import Fault, ResponseError and ProtocolError directly from xmlrpclib

* Fri Dec 03 2010 Miroslav Suchý <msuchy@redhat.com> 1.3.5-1
- 656746 - send to hosted md5 checksum of package (msuchy@redhat.com)
- 656746 - make _processFile and _processBatch method of UploadClass class
  (msuchy@redhat.com)
- 656753 - add namespace prefix to merged functions (msuchy@redhat.com)
- 656753 - fix TB during rhn_package_manager -v -l (msuchy@redhat.com)
- 658527 - create _split_url function (msuchy@redhat.com)
- use constant instead of hardcoded string (msuchy@redhat.com)
- import Fault from different class (msuchy@redhat.com)

* Tue Nov 30 2010 Miroslav Suchý <msuchy@redhat.com> 1.3.4-1
- 658303 - do not forward Host header, it will confuse target Satellite

* Mon Nov 29 2010 Miroslav Suchý <msuchy@redhat.com> 1.3.3-1
- 657956 - fix condrestart option (msuchy@redhat.com)

* Wed Nov 24 2010 Michael Mraka <michael.mraka@redhat.com> 1.3.2-1
- removed unused imports

* Sat Nov 20 2010 Miroslav Suchý <msuchy@redhat.com> 1.3.1-1
- 629552 - Proxy should allow all header from rfc2616 (msuchy@redhat.com)
- Bumping package versions for 1.3. (jpazdziora@redhat.com)

* Wed Nov 10 2010 Jan Pazdziora 1.2.15-1
- addressing rpmlint error non-standard-dir-perm (msuchy@redhat.com)
- fix spelling error (msuchy@redhat.com)
- update Makefile to reflect logrotate files rename (msuchy@redhat.com)
- rename logrotate/rhn_proxy_redirect to logrotate/rhn-proxy-redirect
  (msuchy@redhat.com)
- rename logrotate/rhn_proxy_broker to logrotate/rhn-proxy-broker
  (msuchy@redhat.com)
- mark logrotate.d files as %config(noreplace) (msuchy@redhat.com)
- correct description (msuchy@redhat.com)
- bumping up epoch in provides - do not self-obsolete (msuchy@redhat.com)
- escape entry in changelog (msuchy@redhat.com)

* Fri Nov 05 2010 Miroslav Suchý <msuchy@redhat.com> 1.2.14-1
- 514253 - file cobbler-proxy.conf should have owner, winner is spacewalk-
  proxy-common (msuchy@redhat.com)

* Wed Nov 03 2010 Jan Pazdziora 1.2.13-1
- remove RootDir (msuchy@redhat.com)

* Tue Nov 02 2010 Jan Pazdziora 1.2.12-1
- Update copyright years in the rest of the repo.

* Fri Oct 29 2010 Jan Pazdziora 1.2.11-1
- removed unused class rhnPackageManagerException (michael.mraka@redhat.com)

* Thu Oct 21 2010 Miroslav Suchý <msuchy@redhat.com> 1.2.10-1
- 612581 - spacewalk-backend modules has been migrated to spacewalk namespace

* Thu Oct 21 2010 Miroslav Suchý <msuchy@redhat.com> 1.2.9-1
- 641371 - do not read response body if request is HEAD

* Mon Oct 18 2010 Jan Pazdziora 1.2.8-1
- code cleanup - it does not have sense to require itself (msuchy@redhat.com)
- require policycoreutils due usage of restorecon (msuchy@redhat.com)

* Wed Oct 13 2010 Miroslav Suchý <msuchy@redhat.com> 1.2.7-1
- 640195 - do not produce warning if directory already exist
  (msuchy@redhat.com)

* Wed Oct 13 2010 Miroslav Suchý <msuchy@redhat.com> 1.2.6-1
- fix typo in macro (msuchy@redhat.com)

* Wed Oct 13 2010 Miroslav Suchý <msuchy@redhat.com> 1.2.5-1
- 640195 - put upgrade script to %%posttrans (msuchy@redhat.com)

* Wed Oct 13 2010 Jan Pazdziora 1.2.4-1
- bump up version of proxy (msuchy@redhat.com)

* Mon Oct 04 2010 Michael Mraka <michael.mraka@redhat.com> 1.2.3-1
- replaced local copy of compile.py with standard compileall module

* Wed Sep 01 2010 Miroslav Suchý <msuchy@redhat.com> 1.2.2-1
- 629330 - do not remove /var/cache/rhn/* during upgrade
- 629330 - do not remove /var/spool/rhn-proxy/list itself, only its content

* Tue Aug 31 2010 Justin Sherrill <jsherril@redhat.com> 1.2.1-1
- 629102 - Adding range to the allowed header list for proxy
  (jsherril@redhat.com)
- bumping package versions for 1.2 (mzazrivec@redhat.com)

* Fri Jul 16 2010 Milan Zazrivec <mzazrivec@redhat.com> 1.1.3-1
- oracle client has been removed from /opt/oracle ages ago

* Tue Jun 29 2010 Miroslav Suchý <msuchy@redhat.com> 1.1.2-1
- 609040 - if we request checksum of file, do not sent Range http header

* Mon Apr 19 2010 Michael Mraka <michael.mraka@redhat.com> 1.1.1-1
- merge 2 duplicate byterange module to common.byterange
- bumping spec files to 1.1 packages
- 578854 - read response even if HEADER_CONTENT_LENGTH is not present

* Mon Mar 29 2010 Michael Mraka <michael.mraka@redhat.com> 0.9.3-1
- modified to use mod_wsgi on Fedora 11 and 12

* Thu Mar 25 2010 Miroslav Suchy <msuchy@redhat.com> 0.9.1-1
- 566124 - do not distribute jabber configuration file
- user spacewalk-setup-jabberd to configure jabberd

* Thu Feb 04 2010 Michael Mraka <michael.mraka@redhat.com> 0.8.3-1
- updated copyrights

* Wed Jan 27 2010 Miroslav Suchy <msuchy@redhat.com> 0.8.2-1
- fix usage of uploadLib, which has been rewriten
- remove python-optik
- no hashlib, no checksums :( (michael.mraka@redhat.com)

* Fri Dec  4 2009 Miroslav Suchý <msuchy@redhat.com> 0.8.1-1
- sha256 support

* Wed Nov 25 2009 Miroslav Suchý <msuchy@redhat.com> 0.7.2-1
- 499020 - bump up proxy version to 5.3.1 to enable CDN

* Thu Aug 20 2009 Miroslav Suchý <msuchy@redhat.com> 0.7.1-1
- 503187 - do not automaticaly download rhn_proxy.conf
- 516624 - allow upgrade proxy using CLI to 5.3 from 5.0

* Tue Jul 21 2009 John Matthews <jmatthew@redhat.com> 0.6.8-1
- 503187 - rewrite old config during upgrade, old file will be saved as
  .rpmorig (msuchy@redhat.com)

* Mon Jul 06 2009 John Matthews <jmatthew@redhat.com> 0.6.7-1
- 509522 - remove conflicts and put provides to spacewalk-proxy-management
  (msuchy@redhat.com)

* Fri Jun 26 2009 John Matthews <jmatthew@redhat.com> 0.6.6-1
- fix build error

* Thu Jun 25 2009 John Matthews <jmatthew@redhat.com> 0.6.5-1
- change comments to docstrings (msuchy@redhat.com)
- change comments to docstrings (msuchy@redhat.com)

* Mon Jun 15 2009 Miroslav Suchy <msuchy@redhat.com> 0.6.4-1
- 503187 - close tag

* Wed Jun 10 2009 Miroslav Suchy <msuchy@redhat.com> 0.6.3-1
- 503187 - set MaxRequestsPerChild to 200 (Proxy CLI)

* Wed May  6 2009 Miroslav Suchý <msuchy@redhat.com> 0.6.2-1
- 493428 - require spacewalk-proxy-selinux so we can run in permissive mode

* Wed Apr 22 2009 jesus m. rodriguez <jesusr@redhat.com> 0.6.1-1
- code cleanup (msuchy@redhat.com)
- bump Versions to 0.6.0 (jesusr@redhat.com)
- update copyright and licenses (jesusr@redhat.com)

* Thu Mar 26 2009 Miroslav Suchý <msuchy@redhat.com> 0.5.7-1
- add dependency on httpd

* Thu Jan 29 2009 Miroslav Suchý <msuchy@redhat.com> 0.5.6-1
- 482831 - support redirect to Akamai

* Wed Jan 21 2009 Miroslav Suchý <msuchy@redhat.com> 0.5.5-1
- fix conflicts with spacewalk-proxy-tools
- management do not need to require specific version of package manager

* Tue Jan 20 2009 Miroslav Suchý <msuchy@redhat.com> 0.5.2-1
- 480328 - do not call chkconfig on
- 480326 - do not start services
- 465947 - remove rhn-proxy-debug
- 465947 - remove spacewalk-proxy-tools package

* Mon Jan 19 2009 Miroslav Suchý <msuchy@redhat.com> 0.5.1-1
- 480341 - /etc/init.d/rhn-proxy should be in /etc/rc.d/init.d/rhn-proxy
- point Source0 to fedorahosted.org

* Wed Jan 14 2009 Miroslav Suchý <msuchy@redhat.com> 0.4.5-1
- own /var/cache/rhn/proxy-auth
- fix typo in broker/rhnBroker.py

* Mon Dec  8 2008 Michael Mraka <michael.mraka@redhat.com> 0.4.3-1
- fixed Obsoletes: rhns-* < 5.3.0

* Tue Nov 25 2008 Miroslav Suchý <msuchy@redhat.com> 0.4.2-1
- 470010 - install spacewalk-proxy-common before the broker

* Wed Oct  1 2008 Miroslav Suchý <msuchy@redhat.com> 0.3.3-1
- move rhn-proxy-activate to installer

* Mon Sep 22 2008 Devan Goodwin <dgoodwin@redhat.com> 0.3.2-1
- Correct problems with /var/log/rhn permissions.

* Thu Sep 11 2008 Miroslav Suchý <msuchy@redhat.com> 0.3.1-1
- add meaningful exit code to initscript, remove reload, add condrestart
- add LSB header to init script
- do not enable proxy if user previously disabled it

* Wed Sep 10 2008 Miroslav Suchý <msuchy@redhat.com> 0.2.3-1
- add rhnAuthProtocol.py back, we still need it

* Tue Sep  2 2008 Milan Zazrivec 0.2.2-1
- fix requirements for proxy-broker and proxy-management

* Thu Aug  7 2008 Miroslav Suchy <msuchy@redhat.com> 0.1-2
- rename to spacewalk-proxy-*
- clean up spec
- rewrite descriptions of packages

* Thu Jun 19 2008 Miroslav Suchy <msuchy@redhat.com>
- migrating nocpulse home dir (BZ 202614)

* Fri Apr 11 2008 Miroslav Suchy <msuchy@redhat.com>
- Extracted rhns-proxy-doc and rhns-proxy-html to separate package.
- removing rhnAuthProtocol, rhnException

* Fri Jan 4 2008 Miroslav Suchy <msuchy@redhat.com>
- removing rhns-auth-daemon. We do not use it anymore.

* Wed Oct 1 2007 Miroslav Suchy <msuchy@redhat.com>
- removing old rhn-proxy-upgrade*

* Wed Sep 19 2007 Miroslav Suchy <msuchy@redhat.com>
- moving to apache2 from rhel

* Fri Aug 22 2007 Miroslav Suchy <msuchy@redhat.com>
- replace rhn_mod_python with mod_python
- replace rhn_mod_ssl with mod_ssl
- we do not use mod_perl any more

* Fri Aug 08 2007 Miroslav Suchy <msuchy@redhat.com>
- add byte range support to broker so we can handle local files

* Fri Feb 16 2007 Miroslav Suchy <msuchy@redhat.com>
- BZ 228684 squid support for byte range

* Thu Dec 13 2006 Miroslav Suchy <msuchy@redhat.com>
- BZ 220436 (tools require perl-DateTime to build)

* Wed Dec 12 2006 Miroslav Suchy <msuchy@redhat.com>
- broker require squid

* Thu Dec 09 2004 Todd Warner <taw@redhat.com> 3.6.0
- /usr/sbin/squid, not /usr/bin/squid
- version, squid.conf.sample, and httpd.conf.sample files moved to
  rhns-proxy-tools package to avoid complications with files being in
  place before the script that requires them needs them.

* Tue Dec 07 2004 Todd Warner <taw@redhat.com> 3.6.0
- /var/up2date/packages and /var/up2date/list have been replaced with
  /var/spool/rhn-proxy and /var/spool/rhn-proxy/list
- version has to be passed into rhn-proxy-upgrade-services to ensure it
  is the correct version being used (had problem with %%post reading the
  version from a file that exists within another package even though that
  package is installed in the same package set.

* Wed Nov 03 2004 Todd Warner <taw@redhat.com> 3.6.0
- version file added to rhns-proxy-management
- getProxyVersion() uses that version file to get the correct RHN Proxy version
  fixes a bug in rhns-proxy-tools RPM post script
- updated the "Requires: rhns" for package-manager

* Sun Oct 17 2004 Todd Warner <taw@redhat.com>
- upgrade support stuff: tools package now auto-upgrades the rhn.conf,
  httpd.conf, and squid.conf files.
- added new upgrade executables, libraries, and man pages to the tools
  package.
- tools package restarts apache *everytime* - the code changed.
- added back the squid.conf.sample and httpd.conf.sample files. We
  need them for upgrades.
- we take a hands off approach to rhn_auth_cache now. It is no
  longer the default mechanism, but we don't touch it during the
  post install.

* Tue Oct 05 2004 Todd Warner <taw@redhat.com>
- The rhn.conf.sample and squid.conf.sample files are no longer used. Pulled
  from the RPMs.

* Mon Sep 20 2004 Mihai Ibanescu <misa@redhat.com> 3.6.0-5
- rhns-proxy is now obsoleted by rhns-proxy-management which is the de-facto
  meta-package (bug #130293)

* Sun Jun 27 2004 Todd Warner <taw@redhat.com>
- bugzilla: 125203 - updated requires for RHEL 3 support.

* Fri May 28 2004 Todd Warner <taw@redhat.com>
- pulling rhn_rpm.py* from package manager files. Using common's.
- we don't use rhnHTTPlib.py anymore. Pulled from proxy/broker.
- we don't use rhnAuthProtocol.py or xxmlrpclib.py in rhns-auth-daemon anymore.

* Tue Mar 02 2004 Todd Warner <taw@redhat.com>
- rhn-proxy-tools package added.
- altered some of the requires (broker, redirect and rhn_auth_cache) *must* be
  on the same box now.

* Wed Jan 07 2004 Todd Warner <taw@redhat.com>
- html landing page added.

* Wed Jan 07 2004 Todd Warner <taw@redhat.com>
- rhn_rpm.py* added to lineup until more current "common" code is merged.

* Fri Feb 07 2003 Todd Warner <taw@redhat.com>
- Changed the name of the existing guides and added a bunch more.
- Changed the rhn-proxy-docs rpm description to relect.

* Fri Nov 01 2002 Todd Warner <taw@redhat.com>
- service httpd graceful's for both redirect and broker.

* Tue Oct 15 2002 Todd Warner <taw@redhat.com>
- We're a bit too rigid on the version requirement for rhns-certs-tools.

* Wed Oct  2 2002 Mihai Ibanescu <misa@redhat.com>
- Removed the conflicts with redhat-release

* Tue Sep 17 2002 Todd Warner <taw@redhat.com>
- s/rhns-common/rhns

* Fri Sep 13 2002 Todd Warner <taw@redhat.com>
- need to bounce the rhn_auth_cache upon install
- shouldn't depend on the version of rhns-common

* Wed Sep 11 2002 Todd Warner <taw@redhat.com>
- s/python-clap/python-optik

* Tue Aug 20 2002 Mihai Ibanescu <misa@redhat.com>
- Updated to build in the new environment
- PackageManager and authd build from the same spec file with proxy

* Fri Jun 14 2002 Todd Warner <taw@redhat.com>
- new rpm build: rhns-proxy-docs

* Tue Jun 11 2002 Todd Warner <taw@redhat.com>
- doc dir made more generic. If running both broker and redirect on the
  same machine, two rhn.conf.sample files confuses the issue.

* Fri Jun 07 2002 Todd Warner <taw@redhat.com>
- redirect needs no squid.conf.sample file.

* Thu Jun 06 2002 Todd Warner <taw@redhat.com>
- requires s/rhn_package_manager/rhns-proxy-package-manager now.

* Tue May 21 2002 Cristian Gafton <gafton@redhat.com>
- new location for config files
- stop using RHNS
- fix the damn license field...
- remove docdir hacks (unless there is something I didn't get right)
- saner permissions for config files

* Tue May 21 2002 Todd Warner <taw@redhat.com>
- req on rhns-certs.
- minor descript wording changes.

* Tue May 14 2002 Todd Warner <taw@redhat.com>
- Requires should filter on version only when important (not release as well).
- sign.sh and gen-rpm.sh need to be in their own package.

* Tue May 14 2002 Cristian Gafton <gafton@redhat.com>
- add support for multiple release building

* Fri Apr 19 2002 Cristian Gafton <gafton@redhat.com>
- rhnServer -> apacheHandler

* Wed Apr 10 2002 Todd Warner <taw@redhat.com>
- systemid needs to be chmod'ed to 0640.
- rhns-proxy requires commmon, broker, *and* redirect for the time being.

* Tue Mar 26 2002 Todd Warner <taw@redhat.com>
- added /usr/share/doc/rhn-%%{version}/squid.conf.sample to the proxy broker.

* Wed Mar 20 2002 Todd Warner <taw@redhat.com>
- added /usr/share/doc/rhn-%%{version}/rhn.conf.sample to the offering.

* Sat Mar 16 2002 Todd Warner <taw@redhat.com>
- /etc/rhn/rhn.conf a 0 length config file now.

* Thu Mar 14 2002 Todd Warner <taw@redhat.com>
- broker/redirect specific %%post's.
- %%preun's added that rpmsave the rhn.conf file upon rpm -e.
  This was chosen in opposition to making rhn.conf a %%config'ed
  %%file... which has its own side-effects.
- need to Require rhns-common as well.

* Wed Mar 13 2002 Cristian Gafton <gafton@redhat.com>
- update for building in the new buildsystem

* Wed Mar 13 2002 Todd Warner <taw@redhat.com>
- incorrect path to /en and /ro -- blew up in new build system.

* Tue Mar 12 2002 Mihai Ibanescu <misa@redhat.com>
- proxy -> broker
- log file rotation names changed as well.
- building two rpms: rhns-proxy-broker and rhns-proxy-redirect

* Mon Mar 11 2002 Todd Warner <taw@redhat.com>
- added a spec file 'variable' rhnconf to closer match other spec files.
- properly touch, chown, chmod config file.
- httpd conf files now called: rhn_proxy.httpd.conf and rhn_redirect.httpd.conf

* Sun Mar 10 2002 Mihai Ibanescu <misa@redhat.com>
- Installing the default configuration files

* Thu Mar 07 2002 Todd Warner <taw@redhat.com>
- /etc/rhn/rhn.conf ghosted and merely touched, post install.
- /etc/sysconfig/rhn/systemid give proper permissions.
- /etc/sysconfig/rhn/systemid is a requirement now (proxy only).
- fixed missing Requires for the redirect (Requires are not inherited).
- _proxy --> proxy_ and _redirect --> redirect_ (see PEP 8)
- give ownership of /etc/rhn/rhn.conf to apache
- log rotate files for proxy and redirect added.

* Tue Mar  6 2002 Todd Warner <taw@redhat.com>
- added (noreplace) on the config file crap.

* Tue Mar  5 2002 Todd Warner <taw@redhat.com>
- not using _proxy/rhnConfig.py or _redirect/rhnConfig.py anymore.
- siteConfig*.py not used anymore.
- added support for /etc/rhn/rhn.conf stuff

* Fri Mar  1 2002 Mihai Ibanescu <misa@redhat.com>
- Added rhnHTTPlib.py
- Create /var/log/rhn
- Create /var/up2date/list

* Wed Feb 27 2002 Mihai Ibanescu <misa@redhat.com>
- No picklerpc anymore

* Wed Dec 12 2001 Todd Warner <taw@redhat.com>
- Updated package summaries and descriptions.

* Wed Dec  5 2001 Mihai Ibanescu <misa@redhat.com>
- Splitted in two rpms
- Added conflicts lines

* Fri Nov 21 2001 Todd Warner <taw@redhat.com>
- RHN Proxy SSL Redirect Server code functional.
- Commented out apacheServer_redirect.py until we can make this spew
  two rpms.

* Tue Nov 16 2001 Todd Warner <taw@redhat.com>
- Began process of incorporating RHN Proxy SSL Redirect Server.

* Fri Oct 19 2001 Todd Warner <taw@redhat.com>
- Commented out references to rhnHTTPLogRotate since that should be the
  job of rhns-reports.

* Wed Oct 17 2001 Todd Warner <taw@redhat.com>
- Generic rhnroot added and perculated within.

* Thu Aug 30 2001 Mihai Ibanescu <misa@redhat.com>
- Missing dependency on rhns-common added (#52671)

* Fri Jul 13 2001 Mihai Ibanescu <misa@redhat.com>
- The package manager has its own package now
- Removed the dependency on python-clap
- small comment/description changes.

* Thu Jul 12 2001 Mihai Ibanescu <misa@redhat.com>
- Added rhn_package_manager.py*
- Rearranged the files a bit
- We create /var/up2date/packages by default now
- Added a dependency on python-clap
- siteConfig.py is config(noreplace) now

* Tue Jul 10 2001 Mihai Ibanescu <misa@redhat.com>
- Added rhn_package_manager

* Mon Jul  9 2001 Mihai Ibanescu <misa@redhat.com>
- Added an explicit dependency on python-xmlrpc >= 1.4.4
- Added a dependency on python-picklerpc

* Fri Jul  6 2001 Mihai Ibanescu <misa@redhat.com>
- Added the config files

* Tue Jun 19 2001 Cristian Gafton <gafton@redhat.com>
- import the version and release from the version file

* Mon Jun 18 2001 Mihai Ibanescu <misa@redhat.com>
- Building noarch packages

* Thu Jun 14 2001 Cristian Gafton <gafton@redhat.com>
- siteConfig is now created by the Makefile
- rhnConfig doesn't need to be a config file since we have siteConfig
- make siteConfig common with the server packages

* Tue Jun 12 2001 Cristian Gafton <gafton@redhat.com>
- update to build with the new layout
- don't obsolete unrelated packages like rhns and rhns-head
- removed the cache package too, since now it is a separate module
- remove the server subpackage

* Wed Jun  6 2001 Mihai Ibanescu <misa@redhat.com>
- Build from the CVS tree.

* Mon May 21 2001 Mihai Ibanescu <misa@redhat.com>
- db_build_config is now noreplace

* Fri May 18 2001 Mihai Ibanescu <misa@redhat.com>
- Build from the CVS tree.

* Thu May 17 2001 Mihai Ibanescu <misa@redhat.com>
- Added rhnConfigServer.py
- Changed the spec to avoid installing the local siteConfig.py
- Added webapp files - the server needs them.
- Added Adrian's scripts for database creation
- create_listall changed a bit

* Wed May 16 2001 Mihai Ibanescu <misa@redhat.com>
- Proxy code added
- Moved some files from the main package to the head package, since that
  one will be Red Hat-specific.
- We'll go with rhns-proxy and rhns-proxy-server for now; I know it's very
  confusing.

* Fri Mar 16 2001 Cristian Gafton <gafton@redhat.com>
- deploy the new code layout
- ship a compiled version of config as well
- don't ship default config files that open holes to the world

* Fri Mar 16 2001 Adrian Likins <alikins@redhat.com>
- add the bugzilla_errata stuff to app packages

* Mon Mar 12 2001 Cristian Gafton <gafton@redhat.com>
- get rid of the bsddbmodule source code (unused in the live site)

