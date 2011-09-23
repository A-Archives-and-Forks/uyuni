%define rhnroot %{_prefix}/share/rhn
%define rhnconf %{_sysconfdir}/rhn
%define httpdconf %{rhnconf}/satellite-httpd/conf
%if 0%{?suse_version}
%define apacheconfd %{_sysconfdir}/apache2/conf.d
%define apache_user wwwrun
%define apache_group www
%else
%define apacheconfd %{_sysconfdir}/httpd/conf.d
%define apache_user apache
%define apache_group apache
%endif
%if 0%{?fedora} < 13 && 0%{?rhel} < 6
%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%endif
%global pythonrhnroot %{python_sitelib}/spacewalk

Name: spacewalk-backend
Summary: Common programs needed to be installed on the Spacewalk servers/proxies
Group: Applications/Internet
License: GPLv2 and Python
Version: 1.2.74
Release: 1%{?dist}
URL:       https://fedorahosted.org/spacewalk
Source0: https://fedorahosted.org/releases/s/p/spacewalk/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-build

%if !0%{?suse_version} || 0%{?suse_version} >= 1120
BuildArch: noarch
%endif

%if 0%{?suse_version} >= 1100
# these are only needed for running the unittests in %check
BuildRequires: python-mock
BuildRequires: python-unittest2
BuildRequires: yum
BuildRequires: rhnlib
BuildRequires: python-debian

# for pylint
BuildRequires: pylint
BuildRequires: spacewalk-client-tools
BuildRequires: python-gzipstream
BuildRequires: python-psycopg2
BuildRequires: python(:DBAPI:oracle)
BuildRequires: PyPAM
%endif

%if 0%{?suse_version}
BuildRequires: spacewalk-config
Requires(pre): apache2
PreReq:         %fillup_prereq
%else
Requires(pre): httpd
%endif

Requires: python, rpm-python
# /etc/rhn is provided by spacewalk-proxy-common or by spacewalk-config
Requires: /etc/rhn
Requires: rhnlib >= 1.8
# for Debian support
Requires: python-debian
Requires: %{name}-libs = %{version}-%{release}
BuildRequires: /usr/bin/msgfmt
BuildRequires: /usr/bin/docbook2man
BuildRequires: docbook-utils
# we don't really want to require this redhat-release, so we protect
# against installations on other releases using conflicts...
Obsoletes: rhns-common < 5.3.0
Obsoletes: rhns < 5.3.0
Provides: rhns = 1:%{version}-%{release}
Provides: rhns-common = 1:%{version}-%{release}
Obsoletes: spacewalk-backend-upload-server < 1.2.28
Provides: spacewalk-backend-upload-server = 1:%{version}-%{release}

%description
Generic program files needed by the Spacewalk server machines.
This package includes the common code required by all servers/proxies.

%package sql
Summary: Core functions providing SQL connectivity for the Spacewalk backend modules
Group: Applications/Internet
Requires(pre): %{name} = %{version}-%{release}
Requires: %{name} = %{version}-%{release}
Obsoletes: rhns-sql < 5.3.0
Provides: rhns-sql = 1:%{version}-%{release}
Requires: %{name}-sql-virtual = %{version}-%{release}

%description sql
This package contains the basic code that provides SQL connectivity for
the Spacewalk backend modules.

%package sql-oracle
Summary: Oracle backend for Spacewalk
Group: Applications/Internet
Requires: python(:DBAPI:oracle)
Provides: %{name}-sql-virtual = %{version}-%{release}

%description sql-oracle
This package contains provides Oracle connectivity for the Spacewalk backend
modules.

%package sql-postgresql
Summary: Postgresql backend for Spacewalk
Group: Applications/Internet
Requires: python-psycopg2
Provides: %{name}-sql-virtual = %{version}-%{release}

%description sql-postgresql
This package contains provides PostgreSQL connectivity for the Spacewalk
backend modules.

%package server
Summary: Basic code that provides Spacewalk Server functionality
Group: Applications/Internet
Requires(pre): %{name}-sql = %{version}-%{release}
Requires: %{name}-sql = %{version}-%{release}
Requires: PyPAM
Obsoletes: rhns-server < 5.3.0
Provides: rhns-server = 1:%{version}-%{release}

%if  0%{?rhel} && 0%{?rhel} < 6
Requires: mod_python
%else
Requires: mod_wsgi
%endif


%description server
This package contains the basic code that provides server/backend
functionality for a variety of XML-RPC receivers. The architecture is
modular so that you can plug/install additional modules for XML-RPC
receivers and get them enabled automatically.

%package xmlrpc
Summary: Handler for /XMLRPC
Group: Applications/Internet
Requires: %{name}-server = %{version}-%{release}
Obsoletes: rhns-server-xmlrpc < 5.3.0
Obsoletes: rhns-xmlrpc < 5.3.0
Provides: rhns-server-xmlrpc = 1:%{version}-%{release}
Provides: rhns-xmlrpc = 1:%{version}-%{release}

%description xmlrpc
These are the files required for running the /XMLRPC handler, which
provide the basic support for the registration client (rhn_register)
and the up2date clients.

%package applet
Summary: Handler for /APPLET
Group: Applications/Internet
Requires: %{name}-server = %{version}-%{release}
Obsoletes: rhns-applet < 5.3.0
Provides: rhns-applet = 1:%{version}-%{release}

%description applet
These are the files required for running the /APPLET handler, which
provides the functions for the Spacewalk applet.

%package app
Summary: Handler for /APP
Group: Applications/Internet
Requires: %{name}-server = %{version}-%{release}
Obsoletes: rhns-server-app < 5.3.0
Obsoletes: rhns-app < 5.3.0
Provides: rhns-server-app = 1:%{version}-%{release}
Provides: rhns-app = 1:%{version}-%{release}

%description app
These are the files required for running the /APP handler.
Calls to /APP are used by internal maintenance tools (rhnpush).

%package xp
Summary: Handler for /XP
Group: Applications/Internet
Requires: %{name}-server = %{version}-%{release}
Obsoletes: rhns-server-xp < 5.3.0
Obsoletes: rhns-xp < 5.3.0
Provides: rhns-server-xp = 1:%{version}-%{release}
Provides: rhns-xp = 1:%{version}-%{release}

%description xp
These are the files required for running the /XP handler.
Calls to /XP are used by tools publicly available (like rhn_package_manager).

%package iss
Summary: Handler for /SAT
Group: Applications/Internet
Requires: %{name}-server = %{version}-%{release}
Obsoletes: rhns-sat < 5.3.0
Provides: rhns-sat = 1:%{version}-%{release}

%description iss
%{name} contains the basic code that provides server/backend
functionality for a variety of XML-RPC receivers. The architecture is
modular so that you can plug/install additional modules for XML-RPC
receivers and get them enabled automatically.

This package contains /SAT handler, which provide Inter Spacewalk Sync
capability.

%package iss-export
Summary: Listener for the Server XML dumper
Group: Applications/Internet
Requires: rpm-python
Requires: %{name}-xml-export-libs = %{version}-%{release}

%description iss-export
%{name} contains the basic code that provides server/backend
functionality for a variety of XML-RPC receivers. The architecture is
modular so that you can plug/install additional modules for XML-RPC
receivers and get them enabled automatically.

This package contains listener for the Server XML dumper.

%package libs
Summary: Spacewalk server and client tools libraries
Group: Applications/Internet
%if 0%{?suse_version}
BuildRequires: python-devel
%if 0%{?suse_version} >= 1110
Requires: python-base
%else
Requires: python
Requires: python-hashlib
%endif
%else
BuildRequires: python2-devel
Requires: python-hashlib
%endif

%description libs
Libraries required by both Spacewalk server and Spacewalk client tools.

%package config-files-common
Summary: Common files for the Configuration Management project
Group: Applications/Internet
Requires: %{name}-server = %{version}-%{release}
Obsoletes: rhns-config-files-common < 5.3.0
Provides: rhns-config-files-common = 1:%{version}-%{release}

%description config-files-common
Common files required by the Configuration Management project

%package config-files
Summary: Handler for /CONFIG-MANAGEMENT
Group: Applications/Internet
Requires: %{name}-config-files-common = %{version}-%{release}
Obsoletes: rhns-config-files < 5.3.0
Provides: rhns-config-files = 1:%{version}-%{release}

%description config-files
This package contains the server-side code for configuration management.

%package config-files-tool
Summary: Handler for /CONFIG-MANAGEMENT-TOOL
Group: Applications/Internet
Requires: %{name}-config-files-common = %{version}-%{release}
Obsoletes: rhns-config-files-tool < 5.3.0
Provides: rhns-config-files-tool = 1:%{version}-%{release}

%description config-files-tool
This package contains the server-side code for configuration management tool.

%package package-push-server
Summary: Listener for rhnpush (non-XMLRPC version)
Group: Applications/Internet
Requires: %{name}-server = %{version}-%{release}
Obsoletes: rhns-package-push-server < 5.3.0
Provides: rhns-package-push-server = 1:%{version}-%{release}

%description package-push-server
Listener for rhnpush (non-XMLRPC version)

%package tools
Summary: Spacewalk Services Tools
Group: Applications/Internet
Requires: %{name}-xmlrpc = %{version}-%{release}
Requires: %{name}-app = %{version}-%{release}
Requires: %{name}
Requires: spacewalk-certs-tools
Requires: spacewalk-admin >= 0.1.1-0
Requires: python-gzipstream
%if 0%{?suse_version}
Requires: python-base
%else
Requires: python-hashlib
%endif
Requires: PyXML
%if 0%{?suse_version}
Requires: apache2-prefork
%else
Requires: mod_ssl
%endif
Requires: %{name}-xml-export-libs
Requires: cobbler >= 1.4.3
%if 0%{?rhel} && 0%{?rhel} < 5
Requires: rhnlib  >= 2.1.4-14
%else
Requires: rhnlib  >= 2.5.22
%endif
Obsoletes: rhns-satellite-tools < 5.3.0
Obsoletes: spacewalk-backend-satellite-tools <= 0.2.7
Provides: spacewalk-backend-satellite-tools = %{version}-%{release}
Provides: rhns-satellite-tools = 1:%{version}-%{release}

%description tools
Various utilities for the Spacewalk Server.

%package xml-export-libs
Summary: Spacewalk XML data exporter
Group: Applications/Internet
Requires: %{name}-server = %{version}-%{release}
Obsoletes: rhns-xml-export-libs < 5.3.0
Provides: rhns-xml-export-libs = 1:%{version}-%{release}

%description xml-export-libs
Libraries required by various exporting tools

%prep
%setup -q

%build
%if !0%{?suse_version}
sed -i 's/^INSTALL_DEST.*/INSTALL_DEST = \/etc\/httpd\/conf.d/' apache-conf/Makefile
%endif
make -f Makefile.backend all
export PYTHON_MODULE_NAME=%{name}
export PYTHON_MODULE_VERSION=%{version}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/%{rhnroot}
install -d $RPM_BUILD_ROOT/%{pythonrhnroot}
make -f Makefile.backend install PREFIX=$RPM_BUILD_ROOT \
    MANDIR=%{_mandir}
export PYTHON_MODULE_NAME=%{name}
export PYTHON_MODULE_VERSION=%{version}

%if 0%{?rhel} && 0%{?rhel} < 6
rm -fv $RPM_BUILD_ROOT/%{apacheconfd}/zz-spacewalk-server-wsgi.conf
rm -rfv $RPM_BUILD_ROOT/%{rhnroot}/wsgi
%else
rm -fv $RPM_BUILD_ROOT/%{apacheconfd}/zz-spacewalk-server-python.conf
%endif
rm -f $RPM_BUILD_ROOT/%{_mandir}/man8/satellite-sync.8*

%find_lang %{name}-server

%check
# only run unittests on versions where we have all the right BuildRequires
%if 0%{?suse_version} >= 1100
export PYTHONPATH=%{buildroot}%{python_sitelib}:%{_datadir}/rhn
make -f Makefile.backend pylint
unset PYTHONPATH
pushd %{buildroot}
find -name '*.py' -print0 | xargs -0 python %py_libdir/py_compile.py
popd
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%pre server
OLD_SECRET_FILE=%{_var}/www/rhns/server/secret/rhnSecret.py
if [ -f $OLD_SECRET_FILE ]; then
    install -d -m 750 -o root -g %{apache_group} %{rhnconf}
    mv ${OLD_SECRET_FILE}*  %{rhnconf}
fi

%post server
%if 0%{?suse_version}
sysconf_addword /etc/sysconfig/apache2 APACHE_MODULES wsgi
sysconf_addword /etc/sysconfig/apache2 APACHE_MODULES perl
%endif

# Is secret key in our config file?
regex="^[[:space:]]*(server\.|)secret_key[[:space:]]*=.*$"

if grep -E -i $regex %{rhnconf}/rhn.conf > /dev/null 2>&1 ; then
    # secret key already there
    rm -f %{rhnconf}/rhnSecret.py*
    exit 0
fi

# Generate a secret key if old one is not present
if [ -f %{rhnconf}/rhnSecret.py ]; then
    secret_key=$(PYTHONPATH=%{rhnconf} %{__python} -c \
        "from rhnSecret import SECRET_KEY; print SECRET_KEY")
else
    secret_key=$(dd if=/dev/urandom bs=1024 count=1 2>/dev/null | sha1sum - |
        awk '{print $1}')
fi

echo "server.secret_key = $secret_key" >> %{rhnconf}/rhn.conf
rm -f %{rhnconf}/rhnSecret.py*

%post tools
%{fillup_only -nd reposync rhn}

%files
%defattr(-,root,root)
%doc PYTHON-LICENSES.txt LICENSE
%dir %{pythonrhnroot}
%dir %{pythonrhnroot}/common
%{pythonrhnroot}/common/suseLib.py*
%{pythonrhnroot}/common/apache.py*
%{pythonrhnroot}/common/byterange.py*
%{pythonrhnroot}/common/rhn_posix.py*
%{pythonrhnroot}/common/rhnApache.py*
%{pythonrhnroot}/common/rhnCache.py*
%{pythonrhnroot}/common/rhnConfig.py*
%{pythonrhnroot}/common/rhnException.py*
%{pythonrhnroot}/common/rhnFlags.py*
%{pythonrhnroot}/common/rhnLib.py*
%{pythonrhnroot}/common/rhnLog.py*
%{pythonrhnroot}/common/rhnMail.py*
%{pythonrhnroot}/common/rhnTB.py*
%{pythonrhnroot}/common/rhnRepository.py*
%{pythonrhnroot}/common/rhnTranslate.py*
%{pythonrhnroot}/common/RPC_Base.py*
%attr(770,root,%{apache_group}) %dir %{_var}/log/rhn
# config files
%attr(755,root,%{apache_group}) %dir %{rhnconf}/default
%attr(644,root,%{apache_group}) %{rhnconf}/default/rhn.conf
%attr(755,root,root) %{_bindir}/spacewalk-cfg-get
%{_mandir}/man8/spacewalk-cfg-get.8.gz
# wsgi stuff
%if !0%{?rhel} || 0%{?rhel} >= 6
%dir %{rhnroot}/wsgi
%{rhnroot}/wsgi/__init__.py*
%{rhnroot}/wsgi/wsgiHandler.py*
%{rhnroot}/wsgi/wsgiRequest.py*
%endif

%files sql
%defattr(-,root,root)
%doc PYTHON-LICENSES.txt LICENSE
%if 0%{?suse_version}
%dir %{rhnroot}/server
%endif
# Need __init__ = share it with rhns-server
%dir %{pythonrhnroot}/server
%{pythonrhnroot}/server/__init__.py*
%{rhnroot}/server/__init__.py*
%dir %{pythonrhnroot}/server/rhnSQL
%{pythonrhnroot}/server/rhnSQL/const.py*
%{pythonrhnroot}/server/rhnSQL/dbi.py*
%{pythonrhnroot}/server/rhnSQL/__init__.py*
%{pythonrhnroot}/server/rhnSQL/sql_*.py*

%files sql-oracle
%defattr(-,root,root,-)
%doc PYTHON-LICENSES.txt LICENSE
%{pythonrhnroot}/server/rhnSQL/driver_cx_Oracle.py*

%files sql-postgresql
%defattr(-,root,root,-)
%doc PYTHON-LICENSES.txt LICENSE
%{pythonrhnroot}/server/rhnSQL/driver_postgresql.py*

%files server -f %{name}-server.lang
%defattr(-,root,root)
%doc PYTHON-LICENSES.txt LICENSE
%if 0%{?suse_version}
%dir %{rhnroot}/server
%endif
# modules
%{pythonrhnroot}/server/apacheAuth.py*
%{pythonrhnroot}/server/apacheHandler.py*
%{pythonrhnroot}/server/apacheRequest.py*
%{pythonrhnroot}/server/apacheServer.py*
%{pythonrhnroot}/server/apacheUploadServer.py*
%{pythonrhnroot}/server/rhnAction.py*
%{pythonrhnroot}/server/rhnAuthPAM.py*
%{pythonrhnroot}/server/rhnCapability.py*
%{pythonrhnroot}/server/rhnChannel.py*
%{pythonrhnroot}/server/rhnKickstart.py*
%{pythonrhnroot}/server/rhnDependency.py*
%{pythonrhnroot}/server/rhnPackage.py*
%{pythonrhnroot}/server/rhnPackageUpload.py*
%{pythonrhnroot}/server/basePackageUpload.py*
%{pythonrhnroot}/server/rhnHandler.py*
%{pythonrhnroot}/server/rhnImport.py*
%{pythonrhnroot}/server/rhnLib.py*
%{pythonrhnroot}/server/rhnMapping.py*
%{pythonrhnroot}/server/rhnRepository.py*
%{pythonrhnroot}/server/rhnSession.py*
%{pythonrhnroot}/server/rhnUser.py*
%{pythonrhnroot}/server/rhnVirtualization.py*
%{pythonrhnroot}/server/taskomatic.py*
%dir %{pythonrhnroot}/server/rhnServer
%{pythonrhnroot}/server/rhnServer/*
%dir %{pythonrhnroot}/server/importlib
%{pythonrhnroot}/server/importlib/__init__.py*
%{pythonrhnroot}/server/importlib/archImport.py*
%{pythonrhnroot}/server/importlib/backend.py*
%{pythonrhnroot}/server/importlib/backendLib.py*
%{pythonrhnroot}/server/importlib/backendOracle.py*
%{pythonrhnroot}/server/importlib/blacklistImport.py*
%{pythonrhnroot}/server/importlib/channelImport.py*
%{pythonrhnroot}/server/importlib/debPackage.py*
%{pythonrhnroot}/server/importlib/errataCache.py*
%{pythonrhnroot}/server/importlib/errataImport.py*
%{pythonrhnroot}/server/importlib/headerSource.py*
%{pythonrhnroot}/server/importlib/importLib.py*
%{pythonrhnroot}/server/importlib/kickstartImport.py*
%{pythonrhnroot}/server/importlib/mpmSource.py*
%{pythonrhnroot}/server/importlib/packageImport.py*
%{pythonrhnroot}/server/importlib/packageUpload.py*
%{pythonrhnroot}/server/importlib/productNamesImport.py*
%{pythonrhnroot}/server/importlib/userAuth.py*
%{rhnroot}/server/handlers/__init__.py*

# Repomd stuff
%dir %{pythonrhnroot}/server/repomd
%{pythonrhnroot}/server/repomd/__init__.py*
%{pythonrhnroot}/server/repomd/domain.py*
%{pythonrhnroot}/server/repomd/mapper.py*
%{pythonrhnroot}/server/repomd/repository.py*
%{pythonrhnroot}/server/repomd/view.py*

# the cache
%attr(755,%{apache_user},%{apache_group}) %dir %{_var}/cache/rhn
# config files
%attr(644,root,%{apache_group}) %{rhnconf}/default/rhn_server.conf
# main httpd config
%attr(644,root,%{apache_group}) %config %{apacheconfd}/zz-spacewalk-server.conf

%if 0%{?rhel} && 0%{?rhel} < 6
%attr(644,root,%{apache_group}) %config %{apacheconfd}/zz-spacewalk-server-python.conf
%else
# wsgi stuff
%attr(644,root,%{apache_group}) %config %{apacheconfd}/zz-spacewalk-server-wsgi.conf
%{rhnroot}/wsgi/app.py*
%{rhnroot}/wsgi/applet.py*
%{rhnroot}/wsgi/config.py*
%{rhnroot}/wsgi/config_tool.py*
%{rhnroot}/wsgi/package_push.py*
%{rhnroot}/wsgi/package_upload.py*
%{rhnroot}/wsgi/sat.py*
%{rhnroot}/wsgi/sat_dump.py*
%{rhnroot}/wsgi/xmlrpc.py*
%{rhnroot}/wsgi/xp.py*
%endif

# logs and other stuff
%config(noreplace) %{_sysconfdir}/logrotate.d/spacewalk-backend-server

%files xmlrpc
%defattr(-,root,root)
%doc PYTHON-LICENSES.txt LICENSE
%dir %{rhnroot}/server/handlers/xmlrpc
%{rhnroot}/server/handlers/xmlrpc/*
%dir %{pythonrhnroot}/server/action
%{pythonrhnroot}/server/action/*
%dir %{pythonrhnroot}/server/action_extra_data
%{pythonrhnroot}/server/action_extra_data/*
# config files
%attr(644,root,%{apache_group}) %{rhnconf}/default/rhn_server_xmlrpc.conf
%attr(644,root,%{apache_group}) %config %{httpdconf}/rhn/spacewalk-backend-xmlrpc.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/spacewalk-backend-xmlrpc
%if 0%{?suse_version}
%dir %{rhnroot}/server
%dir %{rhnroot}/server/handlers
%endif

%files applet
%defattr(-,root,root)
%doc PYTHON-LICENSES.txt LICENSE
%if 0%{?suse_version}
%dir %{rhnroot}/server
%endif
%dir %{rhnroot}/server/handlers/applet
%{rhnroot}/server/handlers/applet/*
# config files
%attr(644,root,%{apache_group}) %{rhnconf}/default/rhn_server_applet.conf
%attr(644,root,%{apache_group}) %config %{httpdconf}/rhn/spacewalk-backend-applet.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/spacewalk-backend-applet

%files app
%defattr(-,root,root)
%doc PYTHON-LICENSES.txt LICENSE
%if 0%{?suse_version}
%dir %{rhnroot}/server
%endif
%dir %{rhnroot}/server/handlers/app
%{rhnroot}/server/handlers/app/*
# config files
%attr(644,root,%{apache_group}) %{rhnconf}/default/rhn_server_app.conf
%attr(644,root,%{apache_group}) %config %{httpdconf}/rhn/spacewalk-backend-app.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/spacewalk-backend-app

%files xp
%defattr(-,root,root)
%doc PYTHON-LICENSES.txt LICENSE
%if 0%{?suse_version}
%dir %{rhnroot}/server
%endif
%dir %{rhnroot}/server/handlers/xp
%{rhnroot}/server/handlers/xp/*
# config files
%attr(644,root,%{apache_group}) %{rhnconf}/default/rhn_server_xp.conf
%attr(644,root,%{apache_group}) %config %{httpdconf}/rhn/spacewalk-backend-xp.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/spacewalk-backend-xp

%files iss
%defattr(-,root,root)
%doc PYTHON-LICENSES.txt LICENSE
%if 0%{?suse_version}
%dir %{rhnroot}/server
%endif
%dir %{rhnroot}/server/handlers/sat
%{rhnroot}/server/handlers/sat/*
%config(noreplace) %{_sysconfdir}/logrotate.d/spacewalk-backend-iss
%attr(644,root,%{apache_group}) %config %{httpdconf}/rhn/spacewalk-backend-sat.conf

%files iss-export
%defattr(-,root,root)
%doc PYTHON-LICENSES.txt LICENSE
%dir %{pythonrhnroot}/satellite_exporter
%{pythonrhnroot}/satellite_exporter/__init__.py*
%{pythonrhnroot}/satellite_exporter/satexport.py*

%dir %{rhnroot}/satellite_exporter
%dir %{rhnroot}/satellite_exporter/handlers
%{rhnroot}/satellite_exporter/__init__.py*
%{rhnroot}/satellite_exporter/handlers/__init__.py*
%{rhnroot}/satellite_exporter/handlers/non_auth_dumper.py*
# config files
%attr(644,root,%{apache_group}) %config %{httpdconf}/rhn/spacewalk-backend-sat-dump-internal.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/spacewalk-backend-iss-export


%files libs
%defattr(-,root,root)
%doc PYTHON-LICENSES.txt LICENSE
%{pythonrhnroot}/__init__.py*
%dir %{pythonrhnroot}/common
%{pythonrhnroot}/common/__init__.py*
%{pythonrhnroot}/common/checksum.py*
%{pythonrhnroot}/common/fileutils.py*
%{pythonrhnroot}/common/rhn_deb.py*
%{pythonrhnroot}/common/rhn_mpm.py*
%{pythonrhnroot}/common/rhn_pkg.py*
%{pythonrhnroot}/common/rhn_rpm.py*

%files config-files-common
%defattr(-,root,root)
%doc PYTHON-LICENSES.txt LICENSE
%{pythonrhnroot}/server/configFilesHandler.py*
%dir %{pythonrhnroot}/server/config_common
%{pythonrhnroot}/server/config_common/*

%files config-files
%defattr(-,root,root)
%doc PYTHON-LICENSES.txt LICENSE
%if 0%{?suse_version}
%dir %{rhnroot}/server
%endif
%dir %{rhnroot}/server/handlers/config
%{rhnroot}/server/handlers/config/*
%attr(644,root,%{apache_group}) %{rhnconf}/default/rhn_server_config-management.conf
%attr(644,root,%{apache_group}) %config %{httpdconf}/rhn/spacewalk-backend-config-management.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/spacewalk-backend-config-files

%files config-files-tool
%defattr(-,root,root)
%doc PYTHON-LICENSES.txt LICENSE
%if 0%{?suse_version}
%dir %{rhnroot}/server
%endif
%dir %{rhnroot}/server/handlers/config_mgmt
%{rhnroot}/server/handlers/config_mgmt/*
%attr(644,root,%{apache_group}) %{rhnconf}/default/rhn_server_config-management-tool.conf
%attr(644,root,%{apache_group}) %config %{httpdconf}/rhn/spacewalk-backend-config-management-tool.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/spacewalk-backend-config-files-tool

%files package-push-server
%defattr(-,root,root)
%doc PYTHON-LICENSES.txt LICENSE
%dir %{rhnroot}/upload_server
%{rhnroot}/upload_server/__init__.py*
%dir %{rhnroot}/upload_server/handlers
%{rhnroot}/upload_server/handlers/__init__.py*
%{rhnroot}/upload_server/handlers/package_push
%attr(644,root,%{apache_group}) %{rhnconf}/default/rhn_server_upload.conf
%attr(644,root,%{apache_group}) %{rhnconf}/default/rhn_server_upload_package-push.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/spacewalk-backend-package-push-server
%attr(644,root,%{apache_group}) %config %{httpdconf}/rhn/spacewalk-backend-package-push.conf

%files tools
%defattr(-,root,root)
%doc PYTHON-LICENSES.txt LICENSE
%attr(644,root,%{apache_group}) %{rhnconf}/default/rhn_server_satellite.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/spacewalk-backend-tools
/var/adm/fillup-templates/sysconfig.reposync
%attr(755,root,root) %{_sysconfdir}/cron.daily/suse.de-clean-reposync-logs
%attr(755,root,root) %{_bindir}/rhn-charsets
%attr(755,root,root) %{_bindir}/rhn-satellite-activate
%attr(755,root,root) %{_bindir}/rhn-schema-version
%attr(755,root,root) %{_bindir}/rhn-ssl-dbstore
# unsupported in SUSE Manager 1.2 (bnc #669610)
# %attr(755,root,root) %{_bindir}/satellite-sync
%attr(755,root,root) %{_bindir}/spacewalk-debug
%attr(755,root,root) %{_bindir}/rhn-satellite-exporter
%attr(755,root,root) %{_bindir}/update-packages
%attr(755,root,root) %{_bindir}/spacewalk-repo-sync
%attr(755,root,root) %{_bindir}/rhn-db-stats
%attr(755,root,root) %{_bindir}/rhn-schema-stats
%attr(755,root,root) %{_bindir}/satpasswd
%attr(755,root,root) %{_bindir}/satwho
%attr(755,root,root) %{_bindir}/spacewalk-remove-channel*
%attr(755,root,root) %{_bindir}/rhn-entitlement-report
%attr(755,root,root) %{_bindir}/spacewalk-update-signatures
%{pythonrhnroot}/satellite_tools/SequenceServer.py*
%{pythonrhnroot}/satellite_tools/messages.py*
%{pythonrhnroot}/satellite_tools/progress_bar.py*
%{pythonrhnroot}/satellite_tools/req_channels.py*
%{pythonrhnroot}/satellite_tools/satsync.py*
%{pythonrhnroot}/satellite_tools/satCerts.py*
%{pythonrhnroot}/satellite_tools/satComputePkgHeaders.py*
%{pythonrhnroot}/satellite_tools/syncCache.py*
%{pythonrhnroot}/satellite_tools/sync_handlers.py*
%{pythonrhnroot}/satellite_tools/rhn_satellite_activate.py*
%{pythonrhnroot}/satellite_tools/rhn_ssl_dbstore.py*
%{pythonrhnroot}/satellite_tools/xmlWireSource.py*
%{pythonrhnroot}/satellite_tools/updatePackages.py*
%{pythonrhnroot}/satellite_tools/reposync.py*
%{pythonrhnroot}/satellite_tools/constants.py*
%dir %{pythonrhnroot}/satellite_tools/disk_dumper
%{pythonrhnroot}/satellite_tools/disk_dumper/__init__.py*
%{pythonrhnroot}/satellite_tools/disk_dumper/iss.py*
%{pythonrhnroot}/satellite_tools/disk_dumper/iss_ui.py*
%{pythonrhnroot}/satellite_tools/disk_dumper/iss_isos.py*
%{pythonrhnroot}/satellite_tools/disk_dumper/iss_actions.py*
%{pythonrhnroot}/satellite_tools/disk_dumper/dumper.py*
%{pythonrhnroot}/satellite_tools/disk_dumper/string_buffer.py*
%dir %{pythonrhnroot}/satellite_tools/repo_plugins
%attr(755,root,%{apache_group}) %dir %{_var}/log/rhn/reposync
%{pythonrhnroot}/satellite_tools/repo_plugins/__init__.py*
%{pythonrhnroot}/satellite_tools/repo_plugins/yum_src.py*
%config %attr(644,root,%{apache_group}) %{rhnconf}/default/rhn_server_iss.conf
%{_mandir}/man8/rhn-satellite-exporter.8*
%{_mandir}/man8/rhn-charsets.8*
%{_mandir}/man8/rhn-satellite-activate.8*
%{_mandir}/man8/rhn-schema-version.8*
%{_mandir}/man8/rhn-ssl-dbstore.8*
%{_mandir}/man8/rhn-db-stats.8*
%{_mandir}/man8/rhn-schema-stats.8*
# %{_mandir}/man8/satellite-sync.8*
%{_mandir}/man8/spacewalk-debug.8*
%{_mandir}/man8/satpasswd.8*
%{_mandir}/man8/satwho.8*
%{_mandir}/man8/spacewalk-remove-channel.8*
%{_mandir}/man8/spacewalk-repo-sync.8*
%{_mandir}/man8/spacewalk-update-signatures.8*
%{_mandir}/man8/update-packages.8*
%{_mandir}/man8/rhn-entitlement-report.8*

%files xml-export-libs
%defattr(-,root,root)
%doc PYTHON-LICENSES.txt LICENSE
%dir %{pythonrhnroot}/satellite_tools
%{pythonrhnroot}/satellite_tools/__init__.py*
%{pythonrhnroot}/satellite_tools/geniso.py*
# A bunch of modules shared with satellite-tools
%{pythonrhnroot}/satellite_tools/connection.py*
%{pythonrhnroot}/satellite_tools/diskImportLib.py*
%{pythonrhnroot}/satellite_tools/syncLib.py*
%{pythonrhnroot}/satellite_tools/xmlDiskSource.py*
%{pythonrhnroot}/satellite_tools/xmlSource.py*
%dir %{pythonrhnroot}/satellite_tools/exporter
%{pythonrhnroot}/satellite_tools/exporter/__init__.py*
%{pythonrhnroot}/satellite_tools/exporter/exportLib.py*
%{pythonrhnroot}/satellite_tools/exporter/xmlWriter.py*

# $Id$
%changelog
* Thu Nov 18 2010 Jan Pazdziora 1.2.74-1
- Fixing error in backend spec (unpackaged file) (lzap+git@redhat.com)

* Thu Nov 18 2010 Jan Pazdziora 1.2.73-1
- fixed iss (michael.mraka@redhat.com)
- fixed mod_wsgi configuration (michael.mraka@redhat.com)
- 652625 - fixed file path (michael.mraka@redhat.com)

* Sun Nov 14 2010 Michael Mraka <michael.mraka@redhat.com> 1.2.72-1
- speed up satellite-sync - skip packages we already processed
- speed up satellite-sync - download and parse only missing packages
- kickstart files should be processed one by one
- replaced hashPackageId() with hash_object_id()

* Fri Nov 12 2010 Michael Mraka <michael.mraka@redhat.com> 1.2.71-1
- fixed import of removed function, fixed inversed set operator
- removed unnecessary double assigning

* Fri Nov 12 2010 Lukas Zapletal 1.2.70-1
- Adding missing SQL AS keywords (several patches)
- do not raise exception in exception in case stream is None

* Thu Nov 11 2010 Lukas Zapletal 1.2.69-1
- Adding missing AS keyword to SELECT clause
- Force EVR to be strings in the backend

* Thu Nov 11 2010 Michael Mraka <michael.mraka@redhat.com> 1.2.68-1
- removed dead unique() and intersection()
- replaced own intersection() and unique() with faster builtin set operations

* Thu Nov 11 2010 Lukas Zapletal 1.2.67-1
- Fixing space in SQL bind parameter
- Keyword MINUS is not recognized by PostgreSQL
- Fixing indentation in spacewalk-remove-channel
- l10n: Updates to German
- Revert "l10n: Updates to Swedish
- l10n: Updates to Swedish

* Thu Nov 11 2010 Jan Pazdziora 1.2.66-1
- Update copyright years in backend.

* Wed Nov 10 2010 Jan Pazdziora 1.2.65-1
- use ansi syntax in left join (mzazrivec@redhat.com)

* Wed Nov 10 2010 Jan Pazdziora 1.2.64-1
- removed dead _lookup_last_modified() (michael.mraka@redhat.com)
- removed dead _generate_executemany_data() (michael.mraka@redhat.com)

* Wed Nov 10 2010 Jan Pazdziora 1.2.63-1
- fixed Exception exceptions.AssertionError: <exceptions.AssertionError
  instance at 0x2b4a22e18368> in <bound method Syncer.__del__ of
  <spacewalk.satellite_tools.satsync.Syncer instance at 0x2b4a22e1a0e0>>
  ignored (michael.mraka@redhat.com)

* Tue Nov 09 2010 Michael Mraka <michael.mraka@redhat.com> 1.2.62-1
- fixed exporter issues caused by code removal

* Mon Nov 08 2010 Michael Mraka <michael.mraka@redhat.com> 1.2.61-1
- modified satsync to use uniform interface for disk and wire dumps

* Sat Nov 06 2010 Michael Mraka <michael.mraka@redhat.com> 1.2.60-1
- merged duplicated code in kickstart_guest.py
- merged "attempt to avoid giving out the compat-* packages" blocks
- merged packages to list translation blocks into function
- merged duplicated file checking code into procedure
- merged action code into a single function
- reused code for simple dump_* functions
- merged the same query originaly defined in two places
- merged duplicated code from _add_dists() and _update_dists()
- merged duplicated code in list_packages_sql() and list_all_packages_sql()
- merged duplicated code from list_channel_families() and list_channels()
- SourcePackageContainer can now also reuse diskImportLibContainer
- set ignoreUploaded = 1 in SourcePackageImport by default
- PackageContainer can now also reuse diskImportLibContainer
- set ignoreUploaded = 1 in PackageImport by default
- merged endContainerCallback() definiton into superclass
- merged get_*_handler() code
- redefined SourcePackageContainer via SyncHandlerContainer
- redefined PackageContainer via SyncHandlerContainer
- redefined ShortPackageContainer via SyncHandlerContainer
- redefined KickstartableTreesContainer via SyncHandlerContainer
- redefined ErrataContainer via SyncHandlerContainer
- created general SyncHandlerContainer and redefined ChannelContainer using the
  general one
- removed duplicated _send_headers_rpm()
- fixed XML_Dumper namespace
- reused BaseQueryDumper() fore some more classes
- merged trivial set_iterator() classes into BaseQueryDumper()
- merged checksum handling into BaseChecksumRowDumper()
- reused BaseSubelementDumper() for some more classes
- merged a lot of classes which had differed only in dump_sublement() method
- _get_kickstartable_trees() rewritten via _get_ids()
- merged _get_package_ids() and _get_errata_ids()
- merged rhnSQL.prepare() and h.execute() calls which differs only in query and
  args
- merged duplicated code for writing dumps
- merged id verification code
- fixed typo
- merged _get_key()
- call original dump_subelement() instead of creating _dump_subelement() in
  every subclass
- DatabaseStatement() does exactly what rhnSQL does; removing
- fixed typos
- merged NonAuthenticatedDumper.dump_kickstartable_trees() back to
  XML_Dumper.dump_kickstartable_trees()
- h is used only in verify_errata=True branch
- merged NonAuthenticatedDumper.dump_errata() back to XML_Dumper.dump_errata()
- h is used only in verify_packages=True branch
- merged NonAuthenticatedDumper._packages() back to XML_Dumper._packages()
- added method stubs to main XML_Dumper class
- removed code already commented out
- merged NonAuthenticatedDumper.dump_channel_packages_short() back to
  XML_Dumper.dump_channel_packages_short()
- merged dumper._ChannelsDumper changes back to exportLib._ChannelDumper

* Thu Nov 04 2010 Michael Mraka <michael.mraka@redhat.com> 1.2.59-1
- merged import / download loop code into procedure
- merged several Traceback blocks
- merged StreamProducer setup into its constructor
- moved channel printing code to _printChannel()
- moved progress bar blocks into function

* Thu Nov 04 2010 Lukas Zapletal 1.2.58-1
- Adding missing colon in channelImport.py

* Wed Nov 03 2010 Michael Mraka <michael.mraka@redhat.com> 1.2.57-1
- merged simple sql fetches into a single command
- merged channelManagePermission() and revokeChannelPermission()
- every function calls get('session') and _validate_session(session)
- merged duplicated code into _get_file_revision()
- moved duplicate code for 'dists' and 'release' to a procedure

* Wed Nov 03 2010 Lukas Zapletal 1.2.56-1
- Adding one parameter to to_number functions to be PG compatible
- Fixing query in dumper to be PostgreSQL compatible
- Rewriting SQL JOIN to ANSI syntax in test-dump-channel
- Rewriting SQL JOIN to ANSI syntax in exporter
- Rewriting SQL JOIN to ANSI syntax in disk_dumper
- Rewriting SQL JOIN to ANSI syntax in spacewalk-remove-channel
- 644239 - do not check minor version of xml_dump_version

* Wed Nov 03 2010 Jan Pazdziora 1.2.55-1
- fixed couple of root_dir leftovers from commit
  6a6e58f490b97f941687b56f38e29aad1d6ed69f (michael.mraka@redhat.com)

* Tue Nov 02 2010 Miroslav Suchý <msuchy@redhat.com> 1.2.54-1
- remove RootDir (msuchy@redhat.com)
- fixing package push error 'Not all variables bound', 'ORGID'
  (jsherril@redhat.com)

* Tue Nov 02 2010 Jan Pazdziora 1.2.53-1
- remove RootDir (msuchy@redhat.com)
- fixing package push error 'Not all variables bound', 'ORGID'
  (jsherril@redhat.com)

* Tue Nov 02 2010 Jan Pazdziora 1.2.52-1
- Update copyright years in backend/.
- allow to enable/disable QOS in config file (msuchy@redhat.com)
- do not throttle by default (msuchy@redhat.com)
- update .po and .pot files for spacewalk-backend

* Tue Nov 02 2010 Jan Pazdziora 1.2.51-1
- fixed Error importing xp: No module named handlers.app.packages
  (michael.mraka@redhat.com)

* Mon Nov 01 2010 Jan Pazdziora 1.2.50-1
- Use current_timestamp instead of SYSDATE.
- fixing package upload, to pass in checksums (jsherril@redhat.com)
- fixing wsgiHandler to look in new location for apacheServer
  (jsherril@redhat.com)
- Use current_timestamp with numtodsinterval instead of sysdate.
- Fixing decimal2intfloat -- the function is passed str, not decimal.Decimal;
  we just try to convert to int or float.
- The conversion should take place both for remote and local connections.

* Mon Nov 01 2010 Jan Pazdziora 1.2.49-1
- Use _buildExternalValue to properly sanitize Unicode strings.

* Mon Nov 01 2010 Miroslav Suchý <msuchy@redhat.com> 1.2.48-1
- 612581 - take ownership of /usr/lib/python2.7/site-packages/spacewalk/wsgi
  (msuchy@redhat.com)
- 612581 - change egrep to grep -E (msuchy@redhat.com)
- even getPackageChecksum() and getPackageChecksumBySession() can be merged
  into a single function (michael.mraka@redhat.com)
- fixed typo and syntax error (michael.mraka@redhat.com)
- merged getSourcePackageChecksum() into getPackageChecksum()
  (michael.mraka@redhat.com)
- merged getSourcePackageChecksumBySession() to getPackageChecksumBySession()
  (michael.mraka@redhat.com)
- merged duplicated code into _get_package_checksum()
  (michael.mraka@redhat.com)
- reordered commands to put checksum stuff together (michael.mraka@redhat.com)
- merged 2 calls with just different arguments (michael.mraka@redhat.com)
- moved X-RHN-Action stuff into one place (michael.mraka@redhat.com)
- moved duplicated code to a function (michael.mraka@redhat.com)

* Fri Oct 29 2010 Jan Pazdziora 1.2.47-1
- For Function in PostgreSQL, we have to not just execute, but also fetch the
  value to return.
- Move the SQL munging messages to debug level 6, to be above the "Executing
  SQL" message level.

* Fri Oct 29 2010 Jan Pazdziora 1.2.46-1
- Removing select with rownum. It seems not that useful anyway.

* Fri Oct 29 2010 Jan Pazdziora 1.2.45-1
- Function fix_url not used anywhere, removing; removing its tests as well.
- The common.rhn_memusage is also only used by tests, moving to test/attic.
- Class CVE does not seem to be used, removing.
- Moved server.rhnServerGroup to test/attic.
- Moved server.rhnActivationKey to test/attic, not shipped.
- Method _execute_next does not seem to be used, removing.
- Method _do_snapshot does not seem to be used in Satellite, removing.
- Method _count_channel_servers not used in _channelPackageSubscription in
  Satellite, removing.
- Method checkSatEntitlement not used in Satellite code, hosted only, removing.
- Method updateAndPrint not used, removing.
- Method addToAndPrint not used, removing.
- Method addFromPackageBatch not used, removing.
- The comment says we do not want to use rpmLabelCompare, let us just remove
  it.
- The method _handle_virt_guest_params was commented out for ages; the
  virt_type processing is done in create_system anyway.

* Fri Oct 29 2010 Jan Pazdziora 1.2.44-1
- /XP handler defines just 4 calls identical to /APP calls
  (michael.mraka@redhat.com)
- removed unused class WarningParseException (michael.mraka@redhat.com)
- removed unused class VirtualizationListenerError (michael.mraka@redhat.com)

* Wed Oct 27 2010 Jan Pazdziora 1.2.43-1
- Class UpdateSlots unused, removing.
- Exception SatCertNoFreeEntitlementsException not used, removing.
- Classes _KickstartTreeTypeDumper and _KickstartInstalTypeDumper do not seem
  to be used, removing.
- Exceptions IncompleteLimitInfo and IncompleteLimitInfo* not used, removing.
- Exception genServerCertError not used, removing.
- Exception ForceNotSpecified not used, removing.
- Class ConfigFileMissingStatInfo not used, removing.
- The rhn_timer.py does not seem to be used anywhere, removing.
- Class SourcePackageFile does not seem to be invoked, removing.
- Class ServerGroupTypeDumper not used anywhere, removing.

* Wed Oct 27 2010 Lukas Zapletal 1.2.42-1
- Fixing c89830b90cb36bd6a79641553c5091c57af8fb8e typo

* Wed Oct 27 2010 Lukas Zapletal 1.2.41-1
- Fixing typo in driver_postgresql.py
- Class ReleaseChannelMapImport does not seem to be called, removing.
- fixed NameError: name 'SourcePackageImport' is not defined
- removed redundant empty tagMaps
- reused load_sql
- XXX: not used currently; removing

* Wed Oct 27 2010 Lukas Zapletal 1.2.40-1
- In PostgreSQL NUMERIC types are returned as int or float now
- Rewritten DECODE to ANSI CASE-WHEN syntax for yum
- Class FileWireSource does not seem to be used, removing.
- Class ChannelProductsDumper does not seem to be used, removing.


* Wed Oct 27 2010 Jan Pazdziora 1.2.39-1
- Previous commit leaves __single_query unused, removing.
- Six find_by_* functions do not seem to be called by our code, removing.
- Removal of spacewalk-backend-upload-server makes source_match not called
  anywhere, removing.
- The _timeString0 function looks unused, we shall consider it a dead code.
- The sql_exception_text utility function never called, seems like a dead code.
- The sortHeaders is not called in our code base, removing.
- That setup_old function in test does not seem to be called, we better remove
  it.
- If remove_listener not in our code, remove(remove_listener).
- Function register_system not called, removing.
- Method parse_url not used in backend, removing as dead code.
- The method _line_value does not seem to be used in the test.
- Removing get_kickstart_label which does not seem to be used anywhere.
- Removing function create_user from test.
- After removal of __check_unique_email_db, fault 102 is not longer used.
- Method check_unique_email (and __check_unique_email_db) not used anywhere,
  removing.
- Exception PackageConflictError was only used in check_package_exists,
  removing.
- Removal of spacewalk-backend-upload-server makes check_package_exists unused,
  removing.
- Method channels_for_org not called, removing as dead code.
- Method build_sql_args is not called, removing.
- Method auth_org_access is not used in our code, removing as dead code.

* Mon Oct 25 2010 Miroslav Suchý <msuchy@redhat.com> 1.2.38-1
- 623966 - add man page for rhn-entitlement-report
- 623964 - add man page for update-packages
- 623967 - write man page for spacewalk-update-signatures
- if package is not on disk do not throw TB

* Mon Oct 25 2010 Jan Pazdziora 1.2.37-1
- The psycopg2 seems to be handling unicode strings just fine.
- packages_cursor() and _source_packages_cursor() are dead; removing
  (michael.mraka@redhat.com)
- errata_cursor() and _errata_cursor() are dead; removing
  (michael.mraka@redhat.com)

* Mon Oct 25 2010 Jan Pazdziora 1.2.36-1
- Reset the System Currency multipliers to the original values
  (colin.coe@gmail.com)
- Need to truncate the values upon select as well.

* Fri Oct 22 2010 Jan Pazdziora 1.2.35-1
- Remove duplicates from package changelog.
- Load the appropriate database backend.
- Replace sysdate with current_timestamp.
- Need to avoid inserting empty strings, we use NULL (None) instead.

* Fri Oct 22 2010 Jan Pazdziora 1.2.34-1
- Put import sys back, needed for sys.argv.

* Fri Oct 22 2010 Miroslav Suchý <msuchy@redhat.com> 1.2.33-1
- 612581 - removing /usr/share/rhn from PYTHONPATH
- 612581 - fixing dynamic import

* Thu Oct 21 2010 Miroslav Suchý <msuchy@redhat.com> 1.2.32-1
- 612581 - move python modules from /usr/share/rhn to python site-packages

* Wed Oct 20 2010 Jan Pazdziora 1.2.31-1
- Changing backend (satellite-sync) to use the new rhnPackageChangeLogRec and
  rhnPackageChangeLogData tables.
- autonomous_transaction not supported by PostgreSQL.

* Tue Oct 19 2010 Jan Pazdziora 1.2.30-1
- check_package_spec() already defined in handlers/xmlrpc/up2date.py
  (michael.mraka@redhat.com)
- startswith(), endswith() are builtin functions since RHEL4
  (michael.mraka@redhat.com)
- _delete_channel() is dead after delete_channel() removal
  (michael.mraka@redhat.com)
- _delete_channel_family() is dead after delete_channel_families() removal
  (michael.mraka@redhat.com)
- removed delete_channel_families() -  it is used only in self unit tests
  (michael.mraka@redhat.com)
- removed delete_channel() - it is used only in self unit test
  (michael.mraka@redhat.com)
- Insert current_timestamp instead of sysdate.
- Move the debugging print to log_debug.
- Use numtodsinterval instead of the arithmetics.
- Revert "Using the interval syntax instead of the arithmetic."

* Mon Oct 18 2010 Jan Pazdziora 1.2.29-1
- Using the interval syntax instead of the arithmetic.
- If the epoch is an empty string, make it None (NULL), to avoid bad surprise
  in PostgreSQL later.
- Replace sysdate with current_timestamp in insert.
- If the checksum value is empty string, do not try to look it up.

* Mon Oct 18 2010 Miroslav Suchý <msuchy@redhat.com> 1.2.28-1
- remove package spacewalk-backend-upload-server

* Mon Oct 18 2010 Lukas Zapletal 1.2.27-1
- Constraint vn_rhnservernetinterface_broadcast fixed (PostgreSQL)

* Mon Oct 18 2010 Jan Pazdziora 1.2.26-1
- Fix the placeholder tagging.
- Even when handling evrs, we do not want to store empty strings, we want to
  store NULLs because that is what Oracle will make of them anyway.
- Not only we do not want to convert NULLs to empty strings, we have to convert
  empty strings to NULLs.
- Make the comps-updating block PostgreSQL compatible.
- Add processing of the params parameter for anonymous PL/pgSQL blocks.
- The tag in dollar quoting cannot start with number, which can happen with
  SHA1s from time to time.
- Reserved words problem for Postgresql fixed correctly (lzap+git@redhat.com)

* Fri Oct 15 2010 Jan Pazdziora 1.2.25-1
- Reserved words problem for Postgresql fixed (lzap+git@redhat.com)
- Now that we have unique key on rhnChannelComps(channel_id), we can simplify
  the select which searches for the comps record.
- Prevent satellite-sync from inserting empty strings when it means to insert
  NULLs.

* Wed Oct 13 2010 Lukas Zapletal 1.2.24-1
- Procedure call now general (update_needed_cache) in backend
- Vn_constriant violation in Postgres (vn_rhnpackageevr_epoch)
- Postgres reserved word fix
- Vn_constriant violation in Postgres
- Sysdate changed to current_timestamp
- ANSI syntax for outer join during system registration
- Debug log from postgresql backend driver removed
- Postgres python backend driver functions support
- Postgres savepoint support in backend code

* Wed Oct 13 2010 Michael Mraka <michael.mraka@redhat.com> 1.2.23-1
- speed up queries
- deleted unused code
- 642142 - Fix to make sat-activate zero out ents that are not in the certificate

* Tue Oct 12 2010 Lukas Zapletal 1.2.22-1
- Sysdate replaced with current_timestamp during client reg
- Use e.pgerror instead of e.message for psycopg2.OperationalError.

* Tue Oct 12 2010 Lukas Zapletal 1.2.21-1
- Decode function replaced with case-when in backend

* Tue Oct 12 2010 Jan Pazdziora 1.2.20-1
- Load the appropriate backend and initialize it (twice).
- Load the appropriate backend and initialize it.
- 640526: Fixed a missed logic for entitlement  purging (paji@redhat.com)

* Thu Oct 07 2010 Jan Pazdziora 1.2.19-1
- We cannot insert empty string and depend on the database to convert it to
  null for "is null" to work -- this will fail on PostgreSQL.
- Fix the logic of the adjusted_port.
- Load the appropriate backend and initialize it (rhnPackageUpload.py).
- The AUTONOMOUS_TRANSACTION does not seem to be needed, plus it is not
  supported in PostgreSQL; removing.
- fixing stray comma (jsherril@redhat.com)
- log_debug is not used in sql_base.py, removing the import.

* Mon Oct 04 2010 Michael Mraka <michael.mraka@redhat.com> 1.2.18-1
- replaced local copy of compile.py with standard compileall module
- removed a lot of dead code
- 637155 - pad --start-date, --end-date with zeros

* Thu Sep 23 2010 Shannon Hughes <shughes@redhat.com> 1.2.17-1
- modify reposync logrotate to include channel label log files
  (shughes@redhat.com)
- fixed spec after file rename (michael.mraka@redhat.com)

* Thu Sep 23 2010 Michael Mraka <michael.mraka@redhat.com> 1.2.16-1
- 634559 - fixed component name

* Thu Sep 23 2010 Michael Mraka <michael.mraka@redhat.com> 1.2.15-1
- 634280 - errata should remain associated with already synced channels
- 634263 - allow guests to register across orgs

* Mon Sep 20 2010 Michael Mraka <michael.mraka@redhat.com> 1.2.14-1
- 627566 - update package checksum with value found in database
- 629986 - updating channels last synced time from spacewalk-repo-sync
- initCFG('server') before initDB

* Tue Sep 14 2010 Milan Zazrivec <mzazrivec@redhat.com> 1.2.13-1
- fixing brokeness with spacewalk-update-signatures
- --db option is no longer valid

* Fri Sep 10 2010 Justin Sherrill <jsherril@redhat.com> 1.2.12-1
- 626764 - adding man page for spacewalk-repo-sync (jsherril@redhat.com)
- style fixes (jsherril@redhat.com)
- 571355 - fixing issue where packages that were physically deleted are not re-
  downloaded during a reposync (jsherril@redhat.com)

* Wed Sep 08 2010 Miroslav Suchý <msuchy@redhat.com> 1.2.11-1
- 555046 - when installtime change, update package in db
- create string representation of object dbPackage for better debugging
- 555046 - use constants instead hardcoded values
- fixing common typo pacakges -> packages (tlestach@redhat.com)
- remove oval files during errata import (mzazrivec@redhat.com)

* Mon Sep 06 2010 Michael Mraka <michael.mraka@redhat.com> 1.2.10-1
- 573630 - reused pl/sql implementation of update_needed_cache in python
- fixing broken string substitiution (wrong number of arguments)

* Mon Aug 30 2010 Justin Sherrill <jsherril@redhat.com> 1.2.9-1
- 626749 - fixing spacewalk-repo-sync to ignore source packages
  (jsherril@redhat.com)
- adding missing commit to make repo generation after reposync work again
  (jsherril@redhat.com)
- 579588 - adding a more stern warning message to activating a ceertificate of
  a different version (jsherril@redhat.com)
- 593896 - Moved Kickstart Parition UI logic (paji@redhat.com)

* Tue Aug 24 2010 Michael Mraka <michael.mraka@redhat.com> 1.2.8-1
- fixed update_errata_cache_by_channel job for channels in NULL org

* Thu Aug 19 2010 Michael Mraka <michael.mraka@redhat.com> 1.2.7-1
- 623699 - systemid is not mandatory for ISS
- 624732 - use original config file names
- localization of satellite-sync
- 591050 - satellite sync report type of disk dump

* Tue Aug 17 2010 Justin Sherrill <jsherril@redhat.com> 1.2.6-1
- fixing small mistake where the wrong variable name was
  used (jsherril@redhat.com)

* Tue Aug 17 2010 Justin Sherrill <jsherril@redhat.com> 1.2.5-1
- 619337 - making it so that repodata will be scheduled for regeneration on all
  channels that a package is in.  This will be ignored if not needed (i.e. last
  modified date is not updated) (jsherril@redhat.com)

* Tue Aug 17 2010 Shannon Hughes <shughes@redhat.com> 1.2.4-1
- cartesian product is seldomly wanted (michael.mraka@redhat.com)
- Revert "612581 - move all python libraries to standard python path"
  (msuchy@redhat.com)

* Fri Aug 13 2010 Miroslav Suchý <msuchy@redhat.com> 1.2.3-1
- 612581 - move all python libraries to standard python path
  (msuchy@redhat.com)
- 612581 - for every Requires(pre) add pure Requires (msuchy@redhat.com)
- 612581 - removing notes (msuchy@redhat.com)
- 612581 -  use %%{__python} macro rather then direct call of python
  (msuchy@redhat.com)
- 612581 - use %%global instead of %%define (msuchy@redhat.com)
- 612581 - use macro only for F12/RHEL-5 (msuchy@redhat.com)
- 612581 - use BR python2-devel rather then python-devel (msuchy@redhat.com)
- 589524 - select packages, erratas and kickstart trees according to import
  date (michael.mraka@redhat.com)
- Revert "589524 - select packages, erratas and kickstart trees according to
  import date" (michael.mraka@redhat.com)

* Wed Aug 11 2010 Jan Pazdziora 1.2.2-1
- Check if the function used for the anonymous block already exists -- do not
  attempt to create it again.
- Quote percent char to avoid it from being considered as a placeholder by
  psycopg2.
- With PostgreSQL, the lob value that we get is already a read-only buffer;
  let's stringify it.
- Change the syntax in backend to match python-psycopg2.
- If host is none (we are using the Unix domain socket), we should not pass the
  host parameter at all.
- Replace pgsql by psycopg2 which should give us live upstream again.

* Wed Aug 11 2010 Michael Mraka <michael.mraka@redhat.com> 1.2.1-1
- 614345 - fixed ISS server component name
- 591050 - add meta information to dump

* Tue Aug 10 2010 Milan Zazrivec <mzazrivec@redhat.com> 1.1.48-1
- Revert "591050 - add meta information to dump" (msuchy@redhat.com)

* Tue Aug 10 2010 Milan Zazrivec <mzazrivec@redhat.com> 1.1.47-1
- l10n: Updates to German (de) translation (ttrinks@fedoraproject.org)
- 591050 - add meta information to dump (msuchy@redhat.com)
- dead code - we set end_date, but later we always use self.end_date. Dtto for
  start_date (msuchy@redhat.com)
- code style - expand tabs to whitespace (msuchy@redhat.com)

* Mon Aug 09 2010 Milan Zazrivec <mzazrivec@redhat.com> 1.1.46-1
- l10n: Updates to Swedish (sv) translation (goeran@fedoraproject.org)
- l10n: German translation added (gkoenig@fedoraproject.org)

* Tue Aug 03 2010 Partha Aji <paji@redhat.com> 1.1.45-1
- got the rhncfg manager diff revisions to work with symlinks (paji@redhat.com)
- Fixed config_mgmt diff stuff (paji@redhat.com)

* Fri Jul 30 2010 Jan Pazdziora 1.1.44-1
- It is dbname without underscore for PostgreSQL.
- 619699 - do not blow out if we get unicode string (msuchy@redhat.com)

* Thu Jul 29 2010 Partha Aji <paji@redhat.com> 1.1.43-1
- Config Management schema update + ui + symlinks (paji@redhat.com)
- send only actions which we are able to cache (msuchy@redhat.com)
- add comment to function (msuchy@redhat.com)
- 577868 - adding proper handling of multiline key/value values
  (jsherril@redhat.com)
- 582646 - making spacewalk-remove-channel communicate better about what child
  channels a channel has (jsherril@redhat.com)

* Fri Jul 23 2010 Michael Mraka <michael.mraka@redhat.com> 1.1.42-1
- unified database connection information
- rename rhn_server_*.conf files
- 617188 - fixed name of Swedish translation file

* Tue Jul 20 2010 Milan Zazrivec <mzazrivec@redhat.com> 1.1.41-1
- fix /var/log/rhn permissions
- add missing import

* Mon Jul 19 2010 Miroslav Suchý <msuchy@redhat.com> 1.1.40-1
- add logging hooks (msuchy@redhat.com)
- fix sql syntax error (msuchy@redhat.com)

* Mon Jul 19 2010 Miroslav Suchý <msuchy@redhat.com> 1.1.39-1
- fix syntax error (msuchy@redhat.com)

* Fri Jul 16 2010 Miroslav Suchý <msuchy@redhat.com> 1.1.38-1
- fix build error (msuchy@redhat.com)
- 615298 - if rpm install time is None, do not pass it to time.localtime
  (msuchy@redhat.com)

* Fri Jul 16 2010 Michael Mraka <michael.mraka@redhat.com> 1.1.37-1
- removed handlers/app/rhn_mpm

* Fri Jul 16 2010 Milan Zazrivec <mzazrivec@redhat.com> 1.1.36-1
- check if staging_content_enabled is enabled for our organization

* Thu Jul 15 2010 Milan Zazrivec <mzazrivec@redhat.com> 1.1.35-1
- fix syntax errors (assignments, negations)

* Thu Jul 15 2010 Milan Zazrivec <mzazrivec@redhat.com> 1.1.34-1
- fix requires for spacewalk-backend-sql
- 614667 - provide better error message

* Wed Jul 14 2010 Miroslav Suchý <msuchy@redhat.com> 1.1.33-1
- define new parameter dry_run for all actions (msuchy@redhat.com)
- basic framework for prefetching content from spacewalk (msuchy@redhat.com)
- 604094 - fixing issue where package profile sync would not be scheduled if
  associated with a kickstart profile (jsherril@redhat.com)
- code cleanup - remove unused function schedule_virt_pkg_install
  (msuchy@redhat.com)
- Cleaned up web_customer, rhnPaidOrgs, and rhnDemoOrgs inaddition to moving
  OrgImpl- Org. These are unused tables/views/columns.. Added upgrade scripts
  accordingly (paji@redhat.com)
- adding missing import for inter-satellite-sync (jsherril@redhat.com)
- fixing import errors for inter-satellite sync (jsherril@redhat.com)

* Mon Jul 12 2010 Justin Sherrill <jsherril@redhat.com> 1.1.32-1
- fixing missing import (jsherril@redhat.com)

* Mon Jul 12 2010 Justin Sherrill <jsherril@redhat.com> 1.1.31-1
- 613585 - fixing inter satellite sync and removing HandlerWrap
  (jsherril@redhat.com)
- fixing missing import (jsherril@redhat.com)

* Fri Jul 09 2010 Miroslav Suchý <msuchy@redhat.com> 1.1.30-1
- create virtual package spacewalk-backend-sql-virtual (msuchy@redhat.com)
- removed code which called rhn_ep package because rhn_ep had vanished long
  time ago (michael.mraka@redhat.com)

* Thu Jul 08 2010 Miroslav Suchý <msuchy@redhat.com> 1.1.29-1
- remove shebang from handlers/xmlrpc/get_handler.py (msuchy@redhat.com)
- provide Provides: (msuchy@redhat.com)
- macros should not be used in changelog (msuchy@redhat.com)

* Thu Jul 08 2010 Miroslav Suchý <msuchy@redhat.com> 1.1.28-1
- move %%defattr before %%doc (msuchy@redhat.com)
- rename /usr/share/rhn/satellite_tools/updateSignatures.py to /usr/bin
  /spacewalk-update-signatures (msuchy@redhat.com)
- add epoch to Provides (msuchy@redhat.com)
- logrotate scripts should have noreplace flag (msuchy@redhat.com)
- forgot to save file after resolving conflict during rebase of
  7d48d4d7ab096551c7a53c7670c76ec83c441303 (msuchy@redhat.com)
- wrap long lines (msuchy@redhat.com)
- remove shebang from modules (msuchy@redhat.com)
- fix spelling error (msuchy@redhat.com)
- add logrotate entry for reposync.log (msuchy@redhat.com)
- fix not standard dir permisions (msuchy@redhat.com)
- fix Makefile - pack new renamed logrotate files (msuchy@redhat.com)
- rename logrotate/rhn_server_satellite to logrotate/spacewalk-backend-tools
  (msuchy@redhat.com)
- rename logrotate/rhn_package_push to logrotate/spacewalk-backend-package-
  push-server (msuchy@redhat.com)
- rename logrotate/rhn_package_upload to logrotate/spacewalk-backend-upload-
  server (msuchy@redhat.com)
- rename logrotate/rhn_server to logrotate/spacewalk-backend-server
  (msuchy@redhat.com)
- rename logrotate/rhn_sat_export_internal to logrotate/spacewalk-backend-iss-
  export (msuchy@redhat.com)
- rename logrotate/rhn_server_sat to logrotate/spacewalk-backend-iss
  (msuchy@redhat.com)
- rename logrotate/rhn_config_management_tool to logrotate/spacewalk-backend-
  config-files-tool (msuchy@redhat.com)
- rename logrotate/rhn_config_management to logrotate/spacewalk-backend-config-
  files (msuchy@redhat.com)
- rename logrotate/rhn_server_applet to logrotate/spacewalk-backend-applet
  (msuchy@redhat.com)
- rename logrotate/rhn_server_app to logrotate/spacewalk-backend-app
  (msuchy@redhat.com)
- rename logrotate/rhn_server_xmlrpc to logrotate/spacewalk-backend-xmlrpc
  (msuchy@redhat.com)
- rename ./logrotate/rhn_server_xp to logrotate/spacewalk-backend-xp
  (msuchy@redhat.com)
- set default config files readable by all users (msuchy@redhat.com)
- add to license PYTHON since we use compile.py (msuchy@redhat.com)
- add licensing files to %%doc (msuchy@redhat.com)
- spelling error (msuchy@redhat.com)
- make config files readable (msuchy@redhat.com)
- 453457 - extract from package spacewalk-backend-sql new packages spacewalk-
  backend-sql-oracle and spacewalk-backend-sql-postgresql (msuchy@redhat.com)

* Wed Jul 07 2010 Justin Sherrill <jsherril@redhat.com> 1.1.27-1
- 612163 - fixing issue with satellite sync where rh-public channel family
  information is not set properly (jsherril@redhat.com)
- create repogen after set of packages pushed instead of individually
  (shughes@redhat.com)

* Thu Jul 01 2010 Miroslav Suchý <msuchy@redhat.com> 1.1.26-1
- We need to force port into integer. (jpazdziora@redhat.com)
- adding new virtualization strings for RHEL 6 (jsherril@redhat.com)
- bug fixing for reposync (shughes@redhat.com)
- modified reposync script to handle 1:many channel content source objects
  (shughes@redhat.com)

* Wed Jun 30 2010 Jan Pazdziora 1.1.25-1
- We now call prepare with params for PostgreSQL, for Oracle we will take the
  parameter and ignore it.
- fixing small issue with wsgi handler where status was not a string
  (jsherril@redhat.com)
- adding removed option during alphabetization of command line arguments
  (jsherril@redhat.com)

* Tue Jun 29 2010 Jan Pazdziora 1.1.24-1
- We want to pull the backend type from the config file as well.
- Add initial support for anonymous PL/pgSQL blocks.
- adding flex guest detection at registration time (jsherril@redhat.com)
- few fixes for rhn cert activation, cert activation now works and populates
  max_members correctly, but not populating fve_max_members yet
  (jsherril@redhat.com)
- a few fixse for sat cert handling (jsherril@redhat.com)
- first attempt at adding flex guest to sat cert processing
  (jsherril@redhat.com)
- 608677 - export rhnChannelProduct information into a channel dump
  (mzazrivec@redhat.com)
- 608657 - if --consider-full is set, interpret disk dump as full export,
  otherwise it is used as incremental dump (msuchy@redhat.com)
- 608657 - add option --consider-full to man page of satellite-sync and to
  output of --help (msuchy@redhat.com)
- sort command line parameters alphabeticaly (msuchy@redhat.com)

* Mon Jun 28 2010 Jan Pazdziora 1.1.23-1
- Remove a debugging print.
- do need to check date, we can get anything (msuchy@redhat.com)
- evr should be parsed from the end (msuchy@redhat.com)
- Parse the default_db; the DNS part (the one after @) is DBI-style connect
  string.

* Fri Jun 18 2010 Miroslav Suchý <msuchy@redhat.com> 1.1.22-1
- fix rpmlint warning (msuchy@redhat.com)
- fix rpmlint warning (msuchy@redhat.com)
- fix rpmlint warning (msuchy@redhat.com)
- remove shebang from module (msuchy@redhat.com)
- remove shebang from module (msuchy@redhat.com)
- remove shebang from module (msuchy@redhat.com)
- remove shebang from module (msuchy@redhat.com)
- fixed wording for incompatible checksum error (michael.mraka@redhat.com)
- l10n: Updates to Russian (ru) translation (ypoyarko@fedoraproject.org)

* Wed Jun 09 2010 Justin Sherrill <jsherril@redhat.com> 1.1.21-1
- 600323 - fixing checksums KeyError with rhnpush and channel association
  (jsherril@redhat.com)
- fix broken solaris package downloads
- 600323 - fixing checksums KeyError with rhnpush (jsherril@redhat.com)

* Tue Jun 08 2010 Michael Mraka <michael.mraka@redhat.com> 1.1.20-1
- more exporter code cleanup
- 589524 - select packages, erratas and kickstart trees according to import

* Thu Jun 03 2010 Michael Mraka <michael.mraka@redhat.com> 1.1.19-1
- removed duplicated code from export routines
* Mon May 31 2010 Michael Mraka <michael.mraka@redhat.com> 1.1.18-1
- fixed package build error

* Fri May 28 2010 Michael Mraka <michael.mraka@redhat.com> 1.1.17-1
- removed code relying on dead rhnDumpSnapshot* tables

* Thu May 27 2010 Michael Mraka <michael.mraka@redhat.com> 1.1.16-1
- block old spacewalk from syncing sha256 channels via ISS
- improved performance of linking packages during satellite-sync

* Wed May 19 2010 Michael Mraka <michael.mraka@redhat.com> 1.1.15-1
- 589299 - excluded checksum_list from headers

* Tue May 18 2010 Michael Mraka <michael.mraka@redhat.com> 1.1.14-1
- satellite-sync optimization

* Fri May 14 2010 Michael Mraka <michael.mraka@redhat.com> 1.1.13-1
- fixed performance issue in satellite-sync
- update po files
- l10n: russian added

* Tue May 04 2010 Michael Mraka <michael.mraka@redhat.com> 1.1.12-1
- modified satellite-sync to new xml dumps

* Mon May 03 2010 Jan Pazdziora 1.1.11-1
- 585233 - the has-comps attribute will no longer be used by hosted.
- add dependency information for DEB packages (lukas.durfina@gmail.com)

* Fri Apr 30 2010 Miroslav Suchý <msuchy@redhat.com> 1.1.10-1
- Support for uploading deb packages (lukas.durfina@gmail.com)

* Fri Apr 30 2010 Jan Pazdziora 1.1.9-1
- 585233 - use log2stderr instead of the (debugging) print.
- 585233 - fix the logic handling has_comps and missing comps_last_modified.
- implemented <checksums> in <rhn-package-short> (michael.mraka@redhat.com)

* Thu Apr 29 2010 Jan Pazdziora 1.1.8-1
- 585233 - replace has-comps with rhn-channel-comps-last-modified.
- 585233 - use the rhn-channel-comps-last-modified element instead of boolean
  has-comps.
- fixed HandlerWrap class implementation from commit
  356bddff66b3f7c50ff06f7062d8d111c3f189ff (michael.mraka@redhat.com)
- rhnLib's timestamp2dbtime not used anywhere, removing as dead code.
- The checksumtype is now called checksum_type.

* Tue Apr 27 2010 Michael Mraka <michael.mraka@redhat.com> 1.1.6-1
- implemented dump version 3.6 in rhn-satellite-exporter

* Tue Apr 27 2010 Jan Pazdziora 1.1.5-1
- 585233 - add support for syncing comps data.

* Thu Apr 22 2010 Miroslav Suchý <msuchy@redhat.com> 1.1.4-1
- networkRetries is set in /etc/sysconfig/rhn/up2date and not in rhn.conf

* Tue Apr 20 2010 Miroslav Suchý <msuchy@redhat.com> 1.1.2-1
- fixing build error on RHEL 5

* Mon Apr 19 2010 Michael Mraka <michael.mraka@redhat.com> 1.1.1-1
- merge 2 duplicate byterange module to common.byterange
- bumping spec files to 1.1 packages

* Thu Apr 15 2010 Michael Mraka <michael.mraka@redhat.com> 0.9.23-1
- 582203 - skip failed packages on spacewalk-repo-sync
- use CFG.NETWORK_RETRIES instead of hardcoded value
- removed dead code

* Tue Apr 13 2010 Miroslav Suchý <msuchy@redhat.com> 0.9.21-1
- 175155 - do not use X-RHN-Satellite-XML-Dump-Version on two places
- code cleanup (jpazdziora@redhat.com)

* Wed Apr 07 2010 Michael Mraka <michael.mraka@redhat.com> 0.9.19-1
- 574334 - fixed Error: NameError caught!

* Wed Mar 31 2010 Partha Aji <paji@redhat.com> 0.9.18-1
- 575867 - Fixed a registration issue where config channels
  in reactivation key +  activation key combination got ranked
  the same value causing all sorts of errors. (paji@redhat.com)
- 175155 - require specific version of rhnlib (msuchy@redhat.com)

* Tue Mar 30 2010 Michael Mraka <michael.mraka@redhat.com> 0.9.17-1
- 577668 - fixed spacewalk-repo-sync behaviour for ftp and file

* Mon Mar 29 2010 Michael Mraka <michael.mraka@redhat.com> 0.9.16-1
- more modification to support mod_wsgi in proxy

* Fri Mar 26 2010 Michael Mraka <michael.mraka@redhat.com> 0.9.14-1
- fixed spacewalk-backend packaging

* Thu Mar 25 2010 Michael Mraka <michael.mraka@redhat.com> 0.9.13-1
- moved mod_wsgi stuff from spacewalk-backend-server to spacewalk-backend
- added tomcat6 to satelite-debug

* Mon Mar 22 2010 Michael Mraka <michael.mraka@redhat.com> 0.9.12-1
- 571413 - fixed source rpackage push
- fixing wsgi error handling

* Thu Mar 18 2010 Michael Mraka <michael.mraka@redhat.com> 0.9.11-1
- 561553 - fixed missing commit
- 564278 - fixed satellite-sync call from rhn-satellite-activate

* Wed Mar 17 2010 Michael Mraka <michael.mraka@redhat.com> 0.9.10-1
- 568958 - package removal and verify
- 573140 - solaris packages with duplicate requires

* Fri Mar 12 2010 Michael Mraka <michael.mraka@redhat.com> 0.9.9-1
- Fixed constraint violation when satellite had multiple certs
- 558502 - fixed ordering issue in reprovisioning

* Wed Mar 10 2010 Michael Mraka <michael.mraka@redhat.com> 0.9.8-1
- 571365 - fixed solaris mpm packages import
- spacewalk-remove-channel improvements

* Mon Mar 08 2010 Michael Mraka <michael.mraka@redhat.com> 0.9.7-1
- fixed import to work with satellites running older versions of rhnLib
- 568371 - fix an ORA-00918 on config file import
- fixed error ihandling for spacewalk-channel-remove
- 570176 - disable caching the channel info during export
- spacewalk-remove-channel script enhancements
- 569233 - exit with error value upon error

* Wed Feb 24 2010 Michael Mraka <michael.mraka@redhat.com> 0.9.6-1
- fixed missing require
- fixed dates in rhn-satellite-exporter

* Tue Feb 23 2010 Michael Mraka <michael.mraka@redhat.com> 0.9.5-1
- improved spacewalk-repo-sync

* Mon Feb 22 2010 Michael Mraka <michael.mraka@redhat.com> 0.9.4-1
- fixed import error proxy ImportError: No module named server
- 246480 - sync last_modified column for rhnKickstartableTree as well.
- 501024 - want to preserve families for channels which are already in the dump

* Fri Feb 19 2010 Michael Mraka <michael.mraka@redhat.com> 0.9.1-1
- added repo deletion to channel remove script
- added spacewalk-remove-channel
- added mechanism for updating existing sha256 packages
- 562644 - added class to emulate mod_python's mp_table

* Thu Feb 04 2010 Michael Mraka <michael.mraka@redhat.com> 0.8.43-1
- updated copyrights
- 479911 - removing duplicate rewrites and consolidating to a single location
- added utility to update package checksums

* Wed Feb 03 2010 Michael Mraka <michael.mraka@redhat.com> 0.8.42-1
- implemented satellite-sync --dump-version
- 556761 - existing packages result in not importing gpg signature
- fixed config files not be deployed if system is subscribed to config channel

* Mon Feb 01 2010 Michael Mraka <michael.mraka@redhat.com> 0.8.41-1
- removed unreferenced functions
- let use rhnLockfile from rhnlib
- removed old python 1.5 code
- Revert "543509 - do not fail if machine has not uuid set (like qemu)"

* Fri Jan 29 2010 Michael Mraka <michael.mraka@redhat.com> 0.8.40-1
- fixed the sha module is deprecated
- fixed maximum recursion depth exceeded

* Fri Jan 29 2010 Michael Mraka <michael.mraka@redhat.com> 0.8.39-1
- fixed ISE on F12 mod_wsgi
- 545389 - initial satellite-sync performance issue -- force use of index.

* Wed Jan 27 2010 Michael Mraka <michael.mraka@redhat.com> 0.8.38-1
- fixed packaging of wsgi handler files

* Tue Jan 26 2010 Michael Mraka <michael.mraka@redhat.com> 0.8.37-1
- fixed HTTP 404 on package download
- execute commands through shell

* Fri Jan 22 2010 Michael Mraka <michael.mraka@redhat.com> 0.8.36-1
- fixed handling subprocess.poll() return codes
- 557581 - fixed config deployment would fail when multiple activation keys present

* Thu Jan 21 2010 Michael Mraka <michael.mraka@redhat.com> 0.8.35-1
- fixed bug from popen2 -> subprocess migration
- check parent_channel label only if exists
- 526696 - checking whether server already uses a token
- 528214 - Encode DBstrings as utf-8 bytes before truncating

* Wed Jan 20 2010 Michael Mraka <michael.mraka@redhat.com> 0.8.33-1
- fixed payload_size always = 0 error
- removed dead code in rhn_rpm.py

* Tue Jan 19 2010 Michael Mraka <michael.mraka@redhat.com> 0.8.32-1
- 556460 - time values are <long> on Fedora 12
- fixed DeprecationWarnings on Fedora 12
- 524722 - add /etc/httpd/conf.d to the spacewalk-debug

* Mon Jan 18 2010 Michael Mraka <michael.mraka@redhat.com> 0.8.31-1
- fixed import errors

* Fri Jan 15 2010 Michael Mraka <michael.mraka@redhat.com> 0.8.30-1
- added import of rhn-channel-checksum-type

* Thu Jan 14 2010 Michael Mraka <michael.mraka@redhat.com> 0.8.28-1
- SHA256 code cleanup

* Wed Jan 13 2010 Michael Mraka <michael.mraka@redhat.com> 0.8.25-1
- ISS should work again

* Wed Jan 13 2010 Tomas Lestach <tlestach@redhat.com> 0.8.23-1
- preparations for srpm sync (tlestach@redhat.com)

* Tue Jan 12 2010 Michael Mraka <michael.mraka@redhat.com> 0.8.22-1
- fixed more ISS SHA256 errors
- Force correct UTF-8 for changelog name and text.

* Mon Jan 11 2010 Michael Mraka <michael.mraka@redhat.com> 0.8.21-1
- fixed satsync -l over ISS
- fixed failure of httpd to (re)start
* Sat Jan 09 2010 Michael Mraka <michael.mraka@redhat.com> 0.8.20-1
- fixed SHA256 packages import

* Fri Jan 08 2010 Michael Mraka <michael.mraka@redhat.com> 0.8.19-1
- fixed rhnpush and satellite-sync sha256 errors
- adding wsgi support adapter and removing code dependence on mod_python
- 528833 - having username printed instead of user object

* Thu Jan 07 2010 Michael Mraka <michael.mraka@redhat.com> 0.8.18-1
- made satelite-sync understand both 3.4 and 3.5 dumps
- 175155 - bump up protocol version to 3.5

* Tue Jan 05 2010 Michael Mraka <michael.mraka@redhat.com> 0.8.16-1
- made rhn-satellite-exporter SHA256 ready

* Tue Jan 05 2010 Michael Mraka <michael.mraka@redhat.com> 0.8.15-1
- merged satellite_exporter/exporter into satellite_tools/disk_dumper

* Mon Jan 04 2010 Michael Mraka <michael.mraka@redhat.com> 0.8.14-1
- more fixes in SHA256 implementation

* Thu Dec 17 2009 Michael Mraka <michael.mraka@redhat.com> 0.8.13-1
- fixed kickastart import for sha256 exports
- 528833 - fixed using an activation key of a disabled user

* Wed Dec 16 2009 Michael Mraka <michael.mraka@redhat.com> 0.8.12-1
- fixed satellite-sync of pre-sha256 exports

* Mon Dec 14 2009 Jan Pazdziora 0.8.10-1
- reporting: add column total to the entitlements report

* Mon Dec 14 2009 Michael Mraka <michael.mraka@redhat.com> 0.8.11-1
- fixed satellite-sync errata import

* Fri Dec 11 2009 Michael Mraka <michael.mraka@redhat.com> 0.8.8-1
- removed a lot of dead code
- fixed getFileChecksum usage
- SHA256 fixes
* Thu Dec 10 2009 Michael Mraka <michael.mraka@redhat.com> 0.8.7-1
- added support for uploading SHA256 rpms
- 541078 - rhn-satellite-exporter --start-date and --end-date issues fixed

* Wed Dec 09 2009 Michael Mraka <michael.mraka@redhat.com> 0.8.5-1
- 516767 - create files with default repository owner/group/permissions
- removed duplicated code from syncLib

* Tue Dec 08 2009 Michael Mraka <michael.mraka@redhat.com> 0.8.4-1
- fixed file glob for -libs

* Mon Dec 07 2009 Michael Mraka <michael.mraka@redhat.com> 0.8.3-1
- moved code from rhnlib to spacewalk-backend-libs
- 543509 - do not fail if machine has not uuid set (like qemu)

* Fri Dec  4 2009 Miroslav Suchý <msuchy@redhat.com> 0.8.2-1
- sha256 support

* Fri Dec 04 2009 Michael Mraka <michael.mraka@redhat.com> 0.8.1-1
- rhn_rpm/rhn_mpm moved to rhnlib
- bumping Version to 0.8.0

* Tue Dec  1 2009 Miroslav Suchý <msuchy@redhat.com> 0.7.18-1
- 449167 - time.strptime can not handle None values

* Thu Nov 26 2009 Miroslav Suchý <msuchy@redhat.com> 0.7.17-1
- fix compilation error

* Wed Nov 25 2009 Miroslav Suchý <msuchy@redhat.com> 0.7.16-1
- 540544 - raise error if channel do not exist or you are not allowed to add or remove it
- 540544 - fix usage of check_user_password
- made conditions more readable (michael.mraka@redhat.com)

* Thu Nov 19 2009 Jan Pazdziora 0.7.15-1
- 537063 - drop the report-specific options

* Wed Nov 18 2009 Jan Pazdziora 0.7.14-1
- reporting: add reports "users" and "users-systems".

* Thu Nov 12 2009 Michael Mraka <michael.mraka@redhat.com> 0.7.13-1
- merged exportLib from satellite_exporter to satellite_tools
* Thu Nov  5 2009 Miroslav Suchy <msuchy@redhat.com> 0.7.12-1
- save some time
- replace isinstance with has_key
- do not check xml corectness twice
- call _dict_to_utf8 only once
- 528227 - Warning in case sync would move the channel between orgs.
- do not vaste time checking if string is instance of UnicodeType
- order test according to probability that the type will appear
- reverting 68bed9e28e2973d3e1e30816d9090b7f5e1d4005
- do not ask repeatedly if types has attribute UnicodeKey
- removing unnecessary condition
- optimize code

* Fri Oct 30 2009 Jan Pazdziora 0.7.11-1
- reporting: add column type to the errata-list report.
- removed redundant else; we call associate_package anyway (Michael M.)

* Mon Oct 26 2009 Jan Pazdziora 0.7.10-1
- reporting: added --info options and documentation of reports and fields

* Fri Oct 23 2009 Jan Pazdziora 0.7.9-1
- reporting: added report errata-list and errata-system

* Thu Oct 22 2009 Miroslav Suchy <msuchy@redhat.com> 0.7.8-1
- 449167 - record installation date of rpm package

* Mon Oct 19 2009 Miroslav Suchy <msuchy@redhat.com> 0.7.7-1
- removed unused parameter
- changed get_package_path comment to reflect new package path
- Include constraint info in schema statistics

* Fri Oct 02 2009 Michael Mraka <michael.mraka@redhat.com> 0.7.6-1
- spacewalk-backend-tools requires python-hashlib

* Thu Oct 01 2009 Milan Zazrivec <mzazrivec@redhat.com> 0.7.5-1
- rhn-db-stats: split database & schema statistics (mzazrivec@redhat.com)
- fixes for 524231, 523393, 523760, 523384 (jpazdziora@redhat.com)
- catch all exceptions, so that we commit in all cases. (jpazdziora@redhat.com)
- If we fail, let us commit the previous updates (done in this transaction).
  (jpazdziora@redhat.com)
- Do the rhn_rpm.get_package_header before we do the actual move.
  (jpazdziora@redhat.com)
- No commit in processPackageKeyAssociations. (jpazdziora@redhat.com)
- clean up (pkilambi@redhat.com)
- if nevra enabled use md5sum as a unique constraint for package pushes
  (pkilambi@redhat.com)
- Move the debug message up; if the OS operation fail, we will know what we
  were trying to do. (jpazdziora@redhat.com)
- Add more actual values to log messages, to make debugging easier.
  (jpazdziora@redhat.com)
- No need to sleep if we want the /var/satellite migration to be faster.
  (jpazdziora@redhat.com)
- Update using id, as there is no index on rhnPackage.path which could be used.
  (jpazdziora@redhat.com)

* Fri Sep 04 2009 Michael Mraka <michael.mraka@redhat.com> 0.7.4-1
- fixed output of multivalue variables in spacewalk-cfg-get

* Tue Sep 01 2009 Michael Mraka <michael.mraka@redhat.com> 0.7.3-1
- 494813 - print error message instead of traceback
- postgresql dependency moved to spacewalk-postgresql

* Fri Aug 28 2009 Michael Mraka <michael.mraka@redhat.com> 0.7.2-1
- use spacewalk-cfg-get instead of awk
- added mirror list support to spacewalk-repo-sync
- fixed an ISE relating to config management w/selinux

* Thu Aug 13 2009 Devan Goodwin <dgoodwin@redhat.com> 0.7.1-1
- Add spacewalk-backend Requires on python-pgsql. (dgoodwin@redhat.com)
- 516237 - Fix the channel family population task to take into account None
  counts and use 0 instead while computing the purge count.
  (pkilambi@redhat.com)
- bumping versions to 0.7.0 (jmatthew@redhat.com)

* Wed Aug 05 2009 Pradeep Kilambi <pkilambi@redhat.com> 0.6.30-1
-

* Wed Aug 05 2009 Jan Pazdziora 0.6.29-1
- reporting: add the entitlements report
- enhancing logging mechanism for spacewalk-repo-sync (jsherril@redhat.com)
- Merge branch 'master' into repo-sync (jsherril@redhat.com)
- Patch: Selinux Context support for config files (joshua.roys@gtri.gatech.edu)
- merge conflict (jsherril@redhat.com)
- adding newline to error message output (jsherril@redhat.com)
- fixing small method call in reposync (jsherril@redhat.com)
- fixing specfile to create directory for reposync (jsherril@redhat.com)
- fixing small whitespace error with reposync (jsherril@redhat.com)
- adding better logging for spacewalk-repo-sync (jsherril@redhat.com)
- 467281 - Instead of checksing for the start now we cechk if tools is in the
  channel label. This is not a perfect solution but atleast covers few more
  cases. An ideal solution would be to add some kind of a relation ship between
  parent and child signifying that this is a tools channel for a given parent.
  (pkilambi@redhat.com)
- 505559 - spacewalk-debug now captures database tablespace usage report
  (pkilambi@redhat.com)
- making the logging a bit cleaner (jsherril@redhat.com)
- fixing some import things to actually work on an installed system
  (jsherril@redhat.com)
- adding logging, cache clearing, and a few fixes to reposync
  (jsherril@redhat.com)
- adding makefile to repo_plugins (pkilambi@redhat.com)
- updating spacewalk backend spec file with reposync stuff
  (pkilambi@redhat.com)
- updating Makefile with reposync files (pkilambi@redhat.com)
- some clean up on repo sync stuff (pkilambi@redhat.com)
- adding repo sync task and other UI bits for spacewalk repo sync
  (jsherril@redhat.com)
- backend/satellite_tools/repo_plugins/yum_src.py (jsherril@redhat.com)

* Wed Jul 29 2009 Pradeep Kilambi <pkilambi@redhat.com> 0.6.28-1
-

* Mon Jul 27 2009 Devan Goodwin <dgoodwin@redhat.com> 0.6.27-1
- Fix rhnSQL pgsql driver when sql not provided to Cursor class.
  (dgoodwin@redhat.com)
- Replace Oracle blob update syntax with our rhnSQL wrapper.
  (dgoodwin@redhat.com)
- Add missing cursor method to pgsql rhnsql driver. (dgoodwin@redhat.com)
- Minor pgsql query fix in satCerts.py. (dgoodwin@redhat.com)
- Modify rhn-ssl-dbstore script to not be Oracle specific.
  (dgoodwin@redhat.com)
- Postgresql query fix. (dgoodwin@redhat.com)
- Remove unused query in sync_handlers.py. (dgoodwin@redhat.com)
- Add "as" to query to work with both databases. (dgoodwin@redhat.com)
- Fix Oracle specific setDateFormat call in backend.py. (dgoodwin@redhat.com)
- Change Oracle nextval to sequence_nextval. (dgoodwin@redhat.com)
- Convert Oracle sequence.nextval's to use nextval compatability function.
  (dgoodwin@redhat.com)
- Add rhnSQL Cursor update_blob function. (dgoodwin@redhat.com)
- Change satCerts.py query to be more clear. (dgoodwin@redhat.com)
- Convert unicode Python strings into strings for PostgreSQL.
  (dgoodwin@redhat.com)
- Remove type mapping code from PostgreSQL rhnSQL driver. (dgoodwin@redhat.com)
- Purge munge_args insanity from PostgreSQL rhnSQL driver.
  (dgoodwin@redhat.com)
- Adjust satCerts.py query to work with both databases. (dgoodwin@redhat.com)
- Fix some rhnSQL error reporting for PostgreSQL. (dgoodwin@redhat.com)
- Fix bug in rhnSQL PostgreSQL named -> positional argument conversion.
  (dgoodwin@redhat.com)
- Initial rhnSQL PostgreSQL Procedure implementation. (dgoodwin@redhat.com)
- Modify rhn-satellite-activate to communicate with PostgreSQL.
  (dgoodwin@redhat.com)
- rhnSQL: Adjust and comment out some PostgreSQL Procedure code.
  (dgoodwin@redhat.com)
- Add support for calling PostgreSQL stored procedures with rhnSQL.
  (dgoodwin@dangerouslyinc.com)
- Implement rhnSQL Cursor.execute_bulk for PostgreSQL.
  (dgoodwin@dangerouslyinc.com)

* Mon Jul 27 2009 John Matthews <jmatthew@redhat.com> 0.6.26-1
- 513073 - Fix rhnpush of packages with duplicate requires.
  (dgoodwin@redhat.com)

* Fri Jul 24 2009 Pradeep Kilambi <pkilambi@redhat.com> 0.6.25-1
- 513652 - Dumping the debug level so the info shows up only with --debug flag.
  (pkilambi@redhat.com)
- 513435 - WebUI creates these for us at the org creation time. So dont try to
  insert those at the sync time as ui is not smart enough to check if exists
  before inserting a row. (pkilambi@redhat.com)

* Fri Jul 24 2009 Jan Pazdziora 0.6.24-1
- add spacewalk-report script and inventory report.

* Thu Jul 23 2009 Pradeep Kilambi <pkilambi@redhat.com> 0.6.23-1
- 513432, 513435 : Our channel family import is written such that we compare
  and resync the red hat channel families. But in iss case we can have provate
  channel family ties to a channel ebing imported that will not match whats on
  the slave as slaves default to org 1. This fix should only post process the
  channel families if its a non custom one. (pkilambi@redhat.com)
- reporting: add report option for listing fields for report.
  (jpazdziora@redhat.com)
- reporting: after having parsed the common options, put the rest back to
  sys.argv. (jpazdziora@redhat.com)
- reporting: show error message when unknown report is specified.
  (jpazdziora@redhat.com)
- reporting: change structure of the report definition file to also include
  column names. (jpazdziora@redhat.com)
- reporting: add channel(s) to which the server is registered.
  (jpazdziora@redhat.com)
- reporting: add number of out-of-date packages and errata.
  (jpazdziora@redhat.com)
- reporting: add kernel version to the report. (jpazdziora@redhat.com)
- reporting: when report name is not specified on the command line, show list
  of available reports. (jpazdziora@redhat.com)
- reporting: move the SQL to definition file, to allow for multiple reports.
  (jpazdziora@redhat.com)
- reporting: add registration time and last check-in time.
  (jpazdziora@redhat.com)
- reporting: add the registered by information. (jpazdziora@redhat.com)
- reporting: add hostname and IP address to the report. (jpazdziora@redhat.com)
- reporting: output field names as the first row. (jpazdziora@redhat.com)
- reporting: output formatted as csv. (jpazdziora@redhat.com)
- reporting: initial prepare, execute, and fetch loop. (jpazdziora@redhat.com)
- reporting: add spacewalk-report to the rpm package. (jpazdziora@redhat.com)
- reporting: a stub for new script, spacewalk-report. (jpazdziora@redhat.com)

* Wed Jul 22 2009 John Matthews <jmatthew@redhat.com> 0.6.22-1
- 511283 - Package compare between db and cache should see if the db is newer
  than cache and only then import the content. (pkilambi@redhat.com)

* Tue Jul 21 2009 John Matthews <jmatthew@redhat.com> 0.6.21-1
- 512936 - Changing the custom channel rule to always defalt to org 1 for
  custom channels unless --org option is used. This will avoid the confusion of
  putting the channel is some random org on slaves. (pkilambi@redhat.com)

* Tue Jul 21 2009 Devan Goodwin <dgoodwin@redhat.com> 0.6.20-1
- 512960 - check for the proper attr name on rpm for header reading
  (jbowes@redhat.com)

* Thu Jul 16 2009 Pradeep Kilambi <pkilambi@redhat.com> 0.6.19-1
- 512236 - the org id checks were defaulting to None in custom channel cases
  instead of 1. Also the metadata sting frommaster is a string None so we need
  to check for the string. This should fix both custom and null org content in
  iss case. hosted syncs should work as usual. (pkilambi@redhat.com)
- Return config channels sorted highest to lowest priority.
  (dgoodwin@redhat.com)
- 511116 - changing updatePackages to change the permissions on the kickstart
  trees in the same way we do for packages within /var/satellite
  (jsherril@redhat.com)

* Fri Jul 10 2009 Pradeep Kilambi <pkilambi@redhat.com> 0.6.18-1
- If not commandline options given, compare the erratum channels to the already
  imported ones (pkilambi@redhat.com)
- If not commandline options given, compare the erratum channels to the already
  imported ones (pkilambi@redhat.com)
- compute the channel filtering only if a channel is specified in the
  commandline. If not, use the default (pkilambi@redhat.com)

* Thu Jul 09 2009 John Matthews <jmatthew@redhat.com> 0.6.17-1
- Only include the channels that are being synced to each errata. This will
  help taskomatic not spam users with irrelevant errata mails
  (pkilambi@redhat.com)

* Fri Jul  3 2009 Miroslav Suchy <msuchy@redhat.com> 0.6.16-1
- 509516 - failure to check for non-existant header (Mark Chappell <m.d.chappell@bath.ac.uk>)
- 509444 - remove delete action system from virt page (Shannon Hughes <shughes@redhat.com>)
- 509371 - SSM->Install,Remove,Verify - minor fixes to Package Name and Arch (Brad Buckingham <bbuckingham@redhat.com>)

* Thu Jun 25 2009 John Matthews <jmatthew@redhat.com> 0.6.15-1
- change comments to docstrings (msuchy@redhat.com)
- change comments to docstrings (msuchy@redhat.com)
- change comments to docstrings (msuchy@redhat.com)
- change comments to docstrings (msuchy@redhat.com)
- change comments to docstrings (msuchy@redhat.com)
- change comments to docstrings (msuchy@redhat.com)
- change comments to docstrings (msuchy@redhat.com)
- change comments to docstrings (msuchy@redhat.com)
- change comments to docstrings (msuchy@redhat.com)
- change comments to docstrings (msuchy@redhat.com)
- 499723 - accept follow-redirects with value greater then 2
  (msuchy@redhat.com)
- change comments to docstrings (msuchy@redhat.com)
- change comments to docstrings (msuchy@redhat.com)
- 507867 - Schedule repo gen once the channel package associations is complete
  (pkilambi@redhat.com)
- 505680 - channel_product_id is computed based on the name, product and
  version so it will not match the cache as cache is always None. Also dont
  update the channel_product_id uless the id is different from whats being
  updated (pkilambi@redhat.com)
- Update HACKING file for backend test instructions. (dgoodwin@redhat.com)
- Integrate some PostgreSQL rhnSQL driver unit tests. (dgoodwin@redhat.com)
- First cut of a unit test framework for Python backend. (dgoodwin@redhat.com)
- 507593 - fixing eus registration tracebacks (pkilambi@redhat.com)
- Adding repodata details for a given channel to channelDetails page.
  (pkilambi@redhat.com)
- Revert "503090 - Exclude rhnlib from kickstart profile sync."
  (dgoodwin@redhat.com)
- remove short package dependency on rpms. User might wanna skip the rpms and
  still import metadata. (pkilambi@redhat.com)
- 422611 - Warn that satrm.py is not a supported script. (dgoodwin@redhat.com)
- fixing the unsubscriptable object error when package is not yet in rhnPackage
  table (pkilambi@redhat.com)
- 506264 - This commit includes: (pkilambi@redhat.com)
- 505680 - When satsync tries to do an import it compares whats in cache to db
  and tries to import only new content, but since the last_modified date always
  differ we end up updating the rhnChannel table even when there is nothing to
  sync. Adding last_modified to ignore keys list so that we dont decide the
  diff based on this field. We still continue to compare the rest of the
  fields. (pkilambi@redhat.com)
- 495790 - force uploading a package ends up with duplicate entries in
  rhnPackage table. This is because we use md5sum along with name, evr, package
  arch and org as a primary key while deciding whether to perform an insert or
  an update. Since the solaris packages had same nvrea and org and different
  md5 sums it was doing an insert instead of update on the existing row. Fixed
  the schema wrapper to only use md5sum as a primary key if nvrea feature is
  enabled. Also fixed the package uniquifies to use md5sum only for nvrea.
  (pkilambi@redhat.com)
- Catch the systemExit and preserve the error code. Also fixing the traceback
  issue when db is not accessible (pkilambi@redhat.com)
- removing bugzilla handler specific tests (pkilambi@redhat.com)
- 502581 - splitting the data to smaller chunks to please cx_oracle to avoid
  throwing array too big errors (pkilambi@redhat.com)
- 503090 - Exclude rhnlib from kickstart profile sync. (dgoodwin@redhat.com)

* Fri Jun 05 2009 jesus m. rodriguez <jesusr@redhat.com> 0.6.11-1
- fixing duplicate entries in repogen tables and other clean aup
  (pkilambi@redhat.com)
- add rhn-db-stats manual page (mzazrivec@redhat.com)
- allow rhn-db-stats to write to arbitrary location with running selinux
  (mzazrivec@redhat.com)
- Fixes to support mod_jk >= 2.2.26. (dgoodwin@redhat.com)
- 503243 - Dropping the is_default column as we now determine the default in
  the app code based on the compatible eus channel instead of jus the default.
  (pkilambi@redhat.com)
- Show all available eus channels during registration (jbowes@redhat.com)
- removing some unused hosted stuff (pkilambi@redhat.com)
- removing leftover code after a removed query (jsherril@redhat.com)
- 498517 fixing the error message to show the needed free entitlements for the
  activation to proceed (pkilambi@redhat.com)
- 502060 - The uniquify filter for deps is causing missing deps in repodata gen
  as we should be looking into the name + version instead of just name. Also
  since the f10+ rpms have issues with only duplicate provides, lets process
  the rest of the capabilities. (pkilambi@redhat.com)

* Wed May 27 2009 Brad Buckingham <bbuckingham@redhat.com> 0.6.10-1
- 309601 - removing md5crypt from spacewalk-backend-tools
  (bbuckingham@redhat.com)

* Wed May 27 2009 Jan Pazdziora 0.6.9-1
- spacewalk-backend: add command-line utility spacewalk-cfg-get to
  print config values

* Tue May 26 2009 Devan Goodwin <dgoodwin@redhat.com> 0.6.7-1
- fixing the keyError as we should be using smbios.system.uuid
  (pkilambi@redhat.com)
- 495778 - process UTF-8 input. (jpazdziora@redhat.com)
- 491831 - fix detection if monitoring is enabled (msuchy@redhat.com)
- make variables attributes of instance and not class itself
  (msuchy@redhat.com)
- change comments to docstrings (msuchy@redhat.com)
- make attributes real attributes and not global variables (msuchy@redhat.com)

* Thu May 21 2009 jesus m. rodriguez <jesusr@redhat.com> 0.6.6-1
- 485698 - manual page: fix --db option syntax (mzazrivec@redhat.com)
- 469219 - Adding the permissions ability to our caching mechanism. (pkilambi@redhat.com)
- simplifying the previos commit even more. All we need to check here is if the
  hostename is in the allowed list or not. Jus this one line should accomplish
  that (pkilambi@redhat.com)
- list.pop is causing some unexpected behavior causing to retain the popped
  list in memory and failing the subsequent compares as the list is not being
  garbage collected looks like. very weird behavior and causes the slave check
  ins to fail with ISS not allowed errors. This should resolve the issue as we
  dont modify the list object in place (pkilambi@redhat.com)
- 500168 - fixed virt guest install was marked complete when it was not (jsherril@redhat.com)
- 486526 - use getent instead of grep /etc/{passwd|group} (mzazrivec@redhat.com)
- 439042 - Another pass at conveying a better error message (pkilambi@redhat.com)
- 499560 - sysexit trap is overriding the error codes returned by the
  businesslogic with 0. removing the catch so the exit codes propogate all the
  way through when exporter fails. (pkilambi@redhat.com)
- 477703 - Adding the size limit changes to disk dumper as well (pkilambi@redhat.com)
- 477703 - Porting changes from hosted to limit the size of the data being
  exported slave satellite is pulling content from master (pkilambi@redhat.com)
- Basic support for detecting a KVM/QEMU guest on registration (jbowes@redhat.com)

* Mon May 11 2009 Brad Buckingham <bbuckingham@redhat.com> 0.6.5-1
- 309601 - updating satpasswd/satwho to pull db info from rhn.conf
  (bbuckingham@redhat.com)
* Wed May 06 2009 jesus m. rodriguez <jesusr@redhat.com> 0.6.4-1
- 498273 - removing incorrect index busting package list updates for custom
  base channels (shughes@redhat.com)
- 1000010021 - fixing issue where you could not remove packages from rhel 4
  systems (jsherril@redhat.com)
- 497871 - fixing issue where guest provisioning would show as succesfull even
  when it had failed (jsherril@redhat.com)
- 486526 - put db creation / upgrade logs into spacewalk-debug
  (mzazrivec@redhat.com)
- 486526 - put dump files from embedded db into spacewalk-debug
  (mzazrivec@redhat.com)
- 486526 - put audit.log into spacewalk-debug (mzazrivec@redhat.com)
- 486526 - put schema upgrade logs into spacewalk-debug (mzazrivec@redhat.com)
- 492903 - fixing the sql fetch (pkilambi@redhat.com)

* Fri Apr 24 2009 Brad Buckingham <bbuckingham@redhat.com> 0.6.3-1
- 309601 - adding satpasswd, satwho and md5crypt to spacewalk-backend-tools

* Wed Apr 22 2009 jesus m. rodriguez <jesusr@redhat.com> 0.6.2-1
- 494976 - adding cobbler systme record name usage to reprovisioning
  (jsherril@redhat.com)
- 443500 - Changed logic to determine packages to remove to include the
  server's current package information. (jason.dobies@redhat.com)
- When a new system is registered it will notify search service
  (jmatthew@redhat.com)

* Fri Apr 17 2009 Devan Goodwin <dgoodwin@redhat.com> 0.6.1-1
- 439042 - fixing the not enough entitlements error to more descriptive.
  (pkilambi@redhat.com)
- 495928 - adding cobbler collection to spacewalk-debug (jsherril@redhat.com)
- moving migrate-system-profile to spacewalk-utils package
  (pkilambi@redhat.com)
- 492903 - fix the query to include the privatechannelfamily org into
  rhnprivatecahnnelfamily (pkilambi@redhat.com)
- 495396 - let the commandline ca-cert option override the cert when using in
  conjunction with iss (pkilambi@redhat.com)
- 494982 - fixing the error message to not take extra strings cusing parse
  errors (pkilambi@redhat.com)
- 486526 - display the created and modified information in ISO format.
  (jpazdziora@redhat.com)
- 486526 - add history of schema upgrades to spacewalk-debug
  (mzazrivec@redhat.com)
- 149695 - Including channel_id as part of rhnErrataQueue table so that
  taskomatic can send errata notifications based on channel_id instead of
  sending to everyone subscribed to the channel. The changes include db change
  to rhnErrataQueue table and backend change to satellite-sync's errata import.
  (pkilambi@redhat.com)
- 485870 - only recalculate the channel family counts once per family.
  (mmccune@gmail.com)
- 488062 - fixing the activation to be more careful in checking the integrity
  of variables before assigning slots (pkilambi@redhat.com)
- 494968 - typo in config comment (pkilambi@redhat.com)
- 494593 - fixing the repofile compare to use the right type for java date
  object obtained through hibernate (pkilambi@redhat.com)
- bumping the protocol version on exporter (pkilambi@redhat.com)
- 491668 - update Spacewalk Apache conf to support .htaccess
  (bbuckingham@redhat.com)
- 486526 - store alert.log into the database/ directory.
  (jpazdziora@redhat.com)
- 486526 - renaming directory for database-related stuff, we will want to store
  alert.log here as well. (jpazdziora@redhat.com)
- check the attr instead of try catch (pkilambi@redhat.com)
- 493583 - fixing the rhnpush to call old rpm libraries for RHEL-4
  (pkilambi@redhat.com)
- adding some additional checks before creating first org info
  (pkilambi@redhat.com)
- bump Versions to 0.6.0 (jesusr@redhat.com)
- minor default args clean up (pkilambi@redhat.com)
- Fixing the first org creation to check for ChannelFamily existance and create
  row if missing so the channel shows up in channels tab on sync
  (pkilambi@redhat.com)

* Fri Apr 17 2009 Pradeep Kilambi <pkilambi@redhat.com>
- move the migrate systems script to utils package

* Mon Mar 30 2009 Milan Zazrivec <mzazrivec@redhat.com> 0.5.28-1
- 485698 - rhn-satellite-exporter manual page fixes

* Thu Mar 26 2009 Milan Zazrivec <mzazrivec@redhat.com> 0.5.27-1
- 486526 - additional system files and db statistics included into spacewalk-debug archive

* Wed Mar 25 2009 Devan Goodwin <dgoodwin@redhat.com> 0.5.26-1
- 487621 - Fix segfaults rhnpush has been causing server-side on Fedora 10.
- Fix Oracle exception handling in procedure calls.
- 485529 - Fix to handle empty or missing ip_addr on a disabled interface.
- 482830 - Fix rpm fetch to include the xml-dump-version in httpd headers during GET requests.
- 483811 - Fix orgid based sync logic.
- 480252 - Raise meaningful exception instead of traceback on Oracle column size error.

* Thu Mar 19 2009 Pradeep Kilambi <pkilambi@redhat.com> 0.5.25-1
- 468686 - restricts deactivated accounts from registering systems and managing systems.
- 485532 - Adding the overriding config values for apachec process sizelimit issue

* Wed Mar 18 2009 Mike McCune <mmccune@gmail.com> 0.5.23-1
- 486186 - Update spacewalk spec files to require cobbler >= 1.4.3

* Fri Mar 13 2009 Miroslav Suchy <msuchy@redhat.com> 0.5.22-1
- 484879 - warn if you are connection using ISS to parent which do not know ISS

* Wed Mar 11 2009 Miroslav Suchy <msuchy@redhat.com> 0.5.21-1
- 483802 - remove conflicts between spacewalk-proxy-common and spacewalk-config
- 209620 - satellite-debug creates world readable output
- 479439 - adding better message when trying to downgrade entitelments
- 481236 - making package downloads work for http
- 485875 - fixing missing man page options and removed deprecated ones for satsync

* Fri Mar 06 2009 Devan Goodwin <dgoodwin@redhat.com> 0.5.20-1
- Add missing dependency on PyPAM.

* Thu Mar 05 2009 Pradeep Kilambi <pkilambi@redhat.com> 0.5.19-1
- 488753 - Adding nevra support to satsync

* Tue Mar 03 2009 Dave Parker <dparker@redhat.com> 0.5.18-1
- 483802 - Directory /etc/rhn owned by two packages, group does not match

* Fri Feb 27 2009 jesus m. rodriguez <jesusr@redhat.com> 0.5.17-1
- rebuild

* Thu Feb 26 2009 Pradeep Kilambi <pkilambi@redhat.com> 0.5.15-1
- 430634 - fixing the profile sync code to include arch info

* Thu Feb 26 2009 jesus m. rodriguez <jesusr@redhat.com> 0.5.15-1
- 430634 - support kickstart profile to compare profiles by arch
- 487238 - spacewalk-debug not working, doesnt actually write the tar file

* Thu Feb 26 2009 jesus m. rodriguez <jesusr@redhat.com> 0.5.14-1
- 209620 - satellite-debug creates world readable output

* Sat Feb 21 2009 Devan Goodwin <dgoodwin@redhat.com> 0.5.13-1
- Fix rpm-python hdr installation error on Fedora 10.

* Fri Feb 20 2009 Miroslav Suchy <msuchy@redhat.com> 0.5.12-1
- fixing run time error of satsync

* Thu Feb 19 2009 Pradeep Kilambi <pkilambi@redhat.com> 0.5.11-1
- 480903 - fix for fcntl locking to use flock when IOError's
- 461672 - fixing satsync --no-rpms to only skip rpms

* Wed Feb 18 2009 Dave Parker <dparker@redhat.com> 0.5.9-1
- 486186 - Update spacewalk spec files to require cobbler >= 1.4.2

* Wed Feb 18 2009 Pradeep Kilambi <pkilambi@redhat.com> 0.5.8-1
- Resolves: bz#446289 - create the private channel family at
  org creation time

* Mon Feb 16 2009 Pradeep Kilambi <pkilambi@redhat.com> 0.5.7-1
- yum repodata regen support through taskomatic

* Thu Feb 12 2009 Miroslav Suchý <msuchy@redhat.com> 0.5.6-1
- move logs from /var/tmp to /var/log/nocpulse

* Tue Feb 10 2009 Pradeep Kilambi <pkilambi@redhat.com> 0.5.5-1
- bz#368711 bz#480063

* Mon Feb 09 2009 Pradeep Kilambi <pkilambi@redhat.com> 0.5.4-1
- bz475894:fixing the server code to filter out duplicate deps
  when pushing fedora-10+ packages to channels

* Thu Feb 05 2009 Pradeep Kilambi <pkilambi@redhat.com> 0.5.3-1
- fixing satsync warning.

* Wed Jan 28 2009 Pradeep Kilambi <pkilambi@redhat.com> 0.5.2-1
- removing rhel-instnum dep requires and associated unsed code

* Tue Jan 20 2009 Miroslav Suchý <msuchy@redhat.com> 0.5.1-1
- 480757 - fix filenames generation in repomd for custom channels
- change Source0 to point to fedorahosted.org

* Thu Jan 15 2009 Pradeep Kilambi 0.4.22-1
- include migrate-system-profile.8 file in the spec

* Thu Jan 15 2009 Milan Zazrivec 0.4.20-1
- include migrate-system-profile manual page

* Wed Jan 14 2009 Dave Parker <dparker@redhat.com> 0.4.18-1
- bz461162 added rule to redirect port 80 requests to /rpc/api to /rhn/rpc/api

* Tue Jan 13 2009 Mike McCune <mmccune@gmail.com> 0.4.15-1
- 461162 - for some reason with our new httpd rework this rewrite rule needs
  to be in both config files.  Filed space05 bug: 479911 to address this.

* Tue Jan 13 2009 Michael Mraka <michael.mraka@redhat.com> 0.4.13-1
- resolved #479826
- resolved #479825

* Mon Jan 12 2009 Mike McCune <mmccune@gmail.com> 0.4.12-1
- 461162 - get the virtualization provisioning tracking system to work with a :virt system record.
- 479640 - remove conflict with specspo; if it causes problems,
  it should be fixed properly, either in our code or in specspo

* Thu Jan  8 2009 Jan Pazdziora 0.4.10-1
- more changes for nvrea error handling
- changed all references of none to auto w.r.t
  rhnKickstartVirtualizationType
- 467115 - adding a switch so users can turn off same nvrea different
  vendor package uploads
- eliminate satellite-httpd daemon, migrate to 'stock' apache
- 461162 - adding support to push the cobbler profile name down to koan
- 461162 - adding some virt options and spiffifying the virt provisioning page
- 461162 - moving cobbler requirement down to the RPMs that actually use it
- changes are by multiple authors

* Mon Dec 22 2008 Mike McCune <mmccune@gmail.com>
- Adding proper cobbler requirement with version

* Fri Dec 19 2008 Dave Parker <dparker@redhat.com> 0.4.9-1
- Reconfigured backed to use stock apache server rather than satellite-httpd

* Thu Dec 18 2008 Pradeep Kilambi <pkilambi@redhat.com> 0.4.9-1
- 476055 - fixing sat activation to work by setting the right handler
- 457629 - multiarch support for errata updates

* Fri Dec 12 2008 Jan Pazdziora 0.4.8-1
- 476212 - adding Requires rhel-instnum
- 461162 - remove profile label parameter from the spacewalk-koan call chain
- 461162 - fix problem w/ backend/satellite_tools makefile
- 461162 - remove spacewalk-cobbler-sync as well
- set close-on-exec on log files

* Wed Dec 10 2008 Miroslav Suchy <msuchy@redhat.com> 0.4.7-1
- fix build errors and finish removing of cobbler-spacewalk-sync and
  spacewalk-cobbler-sync from tools subpackage

* Mon Dec  8 2008 Michael Mraka <michael.mraka@redhat.com> 0.4.6-1
- fixed Obsoletes: rhns-* < 5.3.0

* Thu Dec 5 2008 Partha Aji <paji@redhat.com>
- Removed spacewalk-cobbler-sync & cobbler-spacewalk-sync from tools package

* Wed Nov 18 2008 Partha Aji <paji@redhat.com>
- Added spacewalk-cobbler-sync to tools package

* Mon Nov 17 2008 Devan Goodwin <dgoodwin@redhat.com> 0.4.5-1
- Expand rhnSQL PostgreSQL support.
- Fix rhnSQL connection re-use for both Oracle and PostgreSQL.

* Tue Nov 11 2008 Dave Parker <dparker@redhat.com>
- Added cobbler-spacewalk-sync to tools package

* Thu Nov  6 2008 Devan Goodwin <dgoodwin@redhat.com> 0.4.4-1
- Adding initial support for PostgreSQL.

* Sun Nov  2 2008  Pradeep Kilambi <pkilambi@redhat.com> 0.3.3-1
- fixed the auth issue for registration and iss auth handlers

* Fri Oct 24 2008  Jesus M. Rodriguez <jesusr@redhat.com> 0.3.2-1
- renaming the local exporter

* Fri Oct 10 2008  Pradeep Kilambi <pkilambi@redhat.com>
- support for inter spacewalk sync

* Thu Oct  9 2008  Pradeep Kilambi <pkilambi@redhat.com>
- packaging iss-export dump hanlder

* Thu Oct  9 2008  Miroslav Suchy <msuchy@redhat.com>
- add -iss package for handling ISS

* Wed Sep 24 2008 Milan Zazrivec 0.3.1-1
- bumped version for spacewalk 0.3
- fixed package obsoletes

* Wed Sep  3 2008 jesus rodriguez <jesusr@redhat.com> 0.2.4-1
- rebuilding

* Wed Sep  3 2008 Pradeep Kilambi <pkilambi@redhat.com>
- fixing rhnpush to be able to push packages associating to channels

* Wed Sep  3 2008 Devan Goodwin <dgoodwin@redhat.com> 0.2.3-1
- Fixing bug with chown vs chmod.

* Tue Sep  2 2008 Milan Zazrivec 0.2.2-1
- bumped version for tag-release
- removed python-sgmlop, PyXML from spacewalk-backend-server requirements

* Tue Aug 19 2008 Mike McCune 0.1.2-1
- moving requirement for spacewalk-admin version to proper 0.1

* Mon Aug 04 2008  Miroslav Suchy <msuchy@redhat.com> 0.1.2-0
- rename package to spacewalk-server
- cleanup spec

* Mon Jun 30 2008 Pradeep Kilambi <pkilambi@redhat.com>
- including spacewalk-debug tool

* Thu Jun 12 2008 Pradeep Kilambi <pkilambi@redhat.com>
- clean up hosted specific handlers

* Thu Jun 12 2008 Pradeep Kilambi <pkilambi@redhat.com> 5.2.0-9
- updated to use default httpd from distribution

* Thu Sep  6 2007 Jan Pazdziora <jpazdziora@redhat.com>
- updated to use default httpd from distribution

* Thu May 17 2007 Clifford Perry <cperry@redhat.com>
- adding satComputePkgHeaders.py to rhns-satellite-tools. Needed for upgrades

* Wed Apr 11 2007 Pradeep Kilambi <pkilambi@redhat.com>
- removing rhns-soa from backend.spec
- removing hosted specific handlers

* Tue Dec 12 2006 Jesus Rodriguez <jesusr@redhat.com>
- Added rhns-soa package

* Thu Nov 30 2006 Ryan Newberry <rnewberr@redhat.com>
- Updated some files defs to handle the fact that .pyc and .pyo files
  are generated on RHEL5 for geniso.py and gentree.py

* Wed Nov 08 2006 Bret McMillan <bretm@redhat.com>
- remove the preun trigger that nukes the cache, too expensive an operation
  to happen each and every time

* Thu Nov 02 2006 James Bowes <jbowes@redhat.com>
- Remove rhnpush (it has its own spec file now).

* Fri Oct 20 2006 James Bowes <jbowes@redhat.com>
- Replace cheetah with hand-coded xml generation.

* Wed Oct 11 2006 James Bowes <jbowes@redhat.com>
- Include template file for other.xml

* Mon Jul 17 2006 James Bowes <jbowes@redhat.com>
- Add repository metadata generation files.

* Sun Feb 19 2006 Bret McMillan <bretm@redhat.com>
- make rhns-[xp/app/bugzilla] conflict with specspo

* Fri Jul  1 2005 Joel Martin <jmartin@redhat.com> 4.0.0-131
- Makefile.defs python compile searches PATH for python

* Mon Jun  6 2005 Mihai Ibanescu <misa@redhat.com> 4.0.0-106
- split rhns-sql out of rhns-server, to allow for this piece of functionality
  without needing mod_python etc.

* Mon Oct 11 2004 Todd Warner <taw@redhat.com>
- removed rmchannel

* Mon Aug 09 2004 Todd Warner <taw@redhat.com>
- send-satellite-debug executable and manpage pulled

* Tue Jul 06 2004 Todd Warner <taw@redhat.com>
- rhns-shared goes away. Code moves to rhns-certs-tools elsewhere.
- rhn-ssl-dbstore and associated files added.

* Tue Jun 15 2004 Todd Warner <taw@redhat.com>
- new RPM: rhns-shared

* Tue Jun 01 2004 Todd Warner <taw@redhat.com>
- rhn_satellite_activate.py added to spec file.

* Fri May 28 2004 Todd Warner <taw@redhat.com>
- rhn-charsets and manpage added to satellite-tools.
  Thanks to Cliff Perry <cperry@redhat.com> for the script.

* Tue Mar 30 2004 Mihai Ibanescu <misa@redhat.com>
- rhns-upload-server and rhns-package-push-server added to this tree

* Thu Dec 11 2003 Todd Warner <taw@redhat.com>
- rhn-satellite-activate and manpage added to satellite-tools.

* Thu Dec 11 2003 Todd Warner <taw@redhat.com>
- rhn-schema-version and manpage added to satellite-tools.

* Thu Oct 16 2003 Mihai Ibanescu <misa@redhat.com>
- action_error renamed to action_extra_data

* Mon Jul 28 2003 Todd Warner <taw@redhat.com>
- rhnpush.8 (man page) in the rhnpush RPM now instead of satellite-tools (oops)

* Fri Jun  6 2003 Todd Warner <taw@redhat.com>
- man pages added: satellite-debug.8, send-satellite-debug.8, & rhnpush.8

* Thu May  8 2003 Mihai Ibanescu <misa@redhat.com>
- rhns-xml-export-libs depends on python-iconv

* Tue Apr 15 2003 Todd Warner <taw@redhat.com>
- added a number of .py files to the satellite_tools lineup.
- added a number of .py files to the server/importLib lineup.

* Thu Apr  3 2003 Mihai Ibanescu <misa@redhat.com>
- xml-export-libs owns the satellite_tools dir (and therefore also needs
  __init__)

* Tue Mar 18 2003 Todd Warner <taw@redhat.com>
- added rhnLockfile.py. Used by various commandline tools (e.g. satellite-sync).
- rhnFlock.py is no longer used (previously used for locking down log files).

* Tue Mar 11 2003 Cristian Gafton <gafton@redhat.com>
- add hourly crons to rhns-tools

* Fri Feb 28 2003 Mihai Ibanescu <misa@redhat.com>
- Added server/action_error/*

* Fri Jan 31 2003 Mihai Ibanescu <misa@redhat.com>
- Attempt to sanitize the satellite_ttols dir: added xml-export-libs

* Mon Jan 27 2003 Mihai Ibanescu <misa@redhat.com>
- Requires PyXML

* Mon Jan 14 2003 Todd Warner <taw@redhat.com>
- moved ownership of the /var/cache/rhn directory to the rhns-server rpm.
  It's really a server/satellite thang.
- blow away the cache upon uninstallation.

* Mon Jan 13 2003 Mihai Ibanescu <misa@redhat.com>
- Added rmchannel

* Thu Nov  7 2002 Mihai Ibanescu <misa@redhat.com>
- Fixed bug 77463

* Tue Nov  5 2002 Mihai Ibanescu <misa@redhat.com>
- rhnpush should not require rhns-server. rhnpush doesn't even need rhns.
  Bug 77371

* Tue Oct 29 2002 Todd Warner <taw@redhat.com>
- satellite-import goes away.

* Mon Oct  7 2002 Cristian Gafton <gafton@redhat.com>
- updated the tools subpackage

* Wed Oct  2 2002 Mihai Ibanescu <misa@redhat.com>
- added rhns-applet
- removed the requirements imposed by the build system

* Thu Sep 19 2002 Todd Warner <taw@redhat.com>
- rhns shouldn't require DCOracle.
- rhnDefines.py is no longer a part of rhns.

* Wed Sep 11 2002 Todd Warner <taw@redhat.com>
- s/python-clap/python-optik
- appearantly we forgot to require python-optik for satellite-tools as well.

* Tue Aug 20 2002 Cristian Gafton <gafton@redhat.com>
- add satellite-tools back; my split efforts are failing one by one...

* Mon Aug 19 2002 Cristian Gafton <gafton@redhat.com>
- add rhnpush to the mix

* Wed Aug  7 2002 Cristian Gafton <gafton@redhat.com>
- merged the former rhns-notification spec file in too (now as rhns-tools)
- fix post, which should not be tagged to the server package
- renamed some conig files to math their package names better
- merged the spec files for rhns-common and rhns-server into a single
  one. Now the rhns-common package is called simply rhns

* Thu Jul 25 2002 Cristian Gafton <gafton@redhat.com>
- renaming of the default config files
- add per subpackage logrotate files

* Mon Jun 17 2002 Mihai Ibanescu <misa@redhat.com>
- bugzilla component name changed

* Tue Jun 11 2002 Todd Warner <taw@redhat.com>
- bugzilla specific code pulled out of the app_internal RPM and given its own.

* Fri May 31 2002 Todd Warner <taw@redhat.com>
- adding server/rhnPackage.py

* Tue May 21 2002 Cristian Gafton <gafton@redhat.com>
- fix location of config files
- get rid of the RHNS usage
- fix the license fields
- moved rhn_server_satellite.conf back in the rhns-server-sat package
- add defattr to all subpackages
- fix default permissions for config files (apache should be able to
  read them, but not change them)

* Thu May 16 2002 Todd Warner <taw@redhat.com>
- rhn_server_satellite.conf was double serviced in the main server and in sat.
  It is used by satellite-tools as well so needs to reside in rhns-server.

* Wed May 15 2002 Todd Warner <taw@redhat.com>
- httpd.conf.sample file should be a real conf file (..._xmlrpc.httpd.conf).

* Tue May 14 2002 Cristian Gafton <gafton@redhat.com>
- add support for multiple release building

* Tue Apr 23 2002 Cristian Gafton <gafton@redhat.com>
- add rhnHandler

* Thu Apr 18 2002 Todd Warner <taw@redhat.com>
- took out references to rhnslib
- fixed sat stuff.
- added *.httpd.conf files.
- added *.httpd.conf.sample file.
- rhnImport.py* was missing.
- server/handlers/__init__.py* was missing.

* Wed Apr 17 2002 Cristian Gafton <gafton@redhat.com>
- add rhnMapping, apacheHandler and rhnServer
- minor reorg to the files section - still need to figure out if we
  need to ship the whole importlib to all subpackages....

* Wed Apr 17 2002 Mihai Ibanescu <misa@redhat.com>
- /var/up2date/ no longer needed: replaced with /var/cache/rhn
- split rhns-server-{xmlrpc,sat,app,xp}

* Tue Apr 16 2002 Cristian Gafton <gafton@redhat.com>
- add rhnChannel, rhnRPM, rhnUser

* Fri Mar 15 2002 Todd Warner <taw@redhat.com>
- rhnServerLogRotate --> rhn_server in the logrotate directory.

* Thu Mar 14 2002 Todd Warner <taw@redhat.com>
- preun's added that rpmsave the rhn.conf file upon rpm -e.
  This was chosen in opposition to making rhn.conf a config'ed
  file... which has its own side-effects.

* Wed Mar 13 2002 Cristian Gafton <gafton@redhat.com>
- update for the new bs

* Sun Mar 10 2002 Todd Warner <taw@redhat.com>
- removed old obsoletes that simply don't matter.

* Fri Mar  8 2002 Mihai Ibanescu <misa@redhat.com>
- defined rhnconf
- added {rhnroot}/server/conf/rhn.conf

* Thu Mar 07 2002 Todd Warner <taw@redhat.com>
- new common/rhnConfig.py methodology
- server/rhnConfig.py gone
- rhnConfigCheck.py gone
- siteConfig.py no longer relevant
- /etc/rhn/rhn.conf stuff added.
- give ownership of /etc/rhn/rhn.conf to apache
- added log rotation crap.
- fixed a couple of install section errors.

* Wed Oct 17 2001 Todd Warner <taw@redhat.com>
- change location of server specific en/ and ro/ directories.
- small comment/description changes.
- changelog has consistent spacing now.

* Fri Aug 10 2001 Cristian Gafton <gafton@redhat.com>
- track rhnSecret.py as a ghost file

* Mon Jul 30 2001 Mihai Ibanescu <misa@redhat.com>
- Added server/action/*

* Mon Jul 23 2001 Mihai Ibanescu <misa@redhat.com>
- Added a requires for a specific version of rpm-python, since we are sending
  the headers with a digest attached.

* Thu Jul 12 2001 Mihai Ibanescu <misa@redhat.com>
- siteConfig.py is now config(noreplace) since it was screwing up the
  already-installed siteConfig.py

* Mon Jul 10 2001 Todd Warner <taw@redhat.com>
- /var/log/rhns --> /var/log/rhn to match rhnConfig.py

* Mon Jul  9 2001 Cristian Gafton <gafton@redhat.com>
- get rid of the -head package and integrate everything in the rhns-server

* Mon Jul  9 2001 Mihai Ibanescu <misa@redhat.com>
- Added an explicit dependency on python-xmlrpc >= 1.4.4
- Added /var/log/rhns

* Sun Jul 08 2001 Todd Warner <taw@redhat.com>
- unified and now install config files properly

* Tue Jul  3 2001 Cristian Gafton <gafton@redhat.com>
- no more webapp

* Fri Jun 29 2001 Mihai Ibanescu <misa@redhat.com>
- Added /var/up2date/list as a dir

* Tue Jun 19 2001 Cristian Gafton <gafton@redhat.com>
- rename the base package to rhns-server
- import the version and release from the version file

* Mon Jun 18 2001 Mihai Ibanescu <misa@rehdat.com>
- Rebuild

* Fri Jun 15 2001 Mihai Ibanescu <misa@redhat.com>
- Built packages as noarch
- Added a postinstall script to generate the secret
- RPM_BUILD_ROOT is created by the install stage

* Thu Jun 14 2001 Cristian Gafton <gafton@redhat.com>
- siteConfig is now nstalled by Makefile; no need to touch it
- make siteConfig common with the proxy package

* Thu Jun 14 2001 Mihai Ibanescu <misa@redhat.com>
- Added some files
- Fixed the install stage
- Added dependency on rhns-common

* Tue Jun 12 2001 Cristian Gafton <gafton@redhat.com>
- rework for the new layout

* Fri Mar 16 2001 Cristian Gafton <gafton@redhat.com>
- deploy the new code layout
- ship a compiled version of config as well
- don't ship default config files that open holes to the world

* Fri Mar 16 2001 Adrian Likins <alikins@redhat.com>
- add the bugzilla_errata stuff to app packages

* Mon Mar 12 2001 Cristian Gafton <gafton@redhat.com>
- get rid of the bsddbmodule source code (unused in the live site)

