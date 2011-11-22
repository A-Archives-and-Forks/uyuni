#!/bin/bash

DO_MIGRATION=0
DO_SETUP=0
LOGFILE=0
WAIT_BETWEEN_STEPS=0

MIGRATION_ENV="/root/migration_env.sh"
SETUP_ENV="/root/setup_env.sh"

SATELLITE_HOST=""
SATELLITE_DOMAIN=""
SATELLITE_DB_USER=""
SATELLITE_DB_PASS=""
SATELLITE_DB_SID=""

SATELLITE_FQDN=""
SATELLITE_IP=""

ORACLE_VERSION="XE"

RSYNC_PASSWORD=""

# setup_hostname()
# setup_db_xe()
# setup_db_full()
# setup_spacewalk()
# drop_manager_db()
# dump_remote_db()
# import_db()
# upgrade_schema()
# copy_remote_files()

function help() {
    echo "
Usage: $0 [OPTION]
helper script to do migration or setup of SUSE Manager

  -l LOGFILE     write a log to LOGFILE
  -m             full migration of an existing RHN Satellite
  -s             fresh setup of the SUSE Manager installation
  -r             only sync remote files (useful for migration only)
  -w             wait between steps (in case you do -r -m)
  -h             this help screen

"
}

setup_swap() {

SWAP=`LANG=C free | grep Swap: | sed -e "s/ \+/\t/g" | cut -f 2`
FREESPACE=`LANG=C df / | tail -1 | sed -e "s/ \+/\t/g" | cut -f 4`

if [ $SWAP -eq 0 ]; then
    echo "No swap found; trying to setup additional swap space..."
    if [ $FREESPACE -le 3000000 ]; then
        echo "Not enough space on /. Not adding swap space. Good luck..."
    else
        dd if=/dev/zero of=/SWAPFILE bs=1M count=2000
        sync
        mkswap -f /SWAPFILE
        echo "/SWAPFILE swap swap defaults 0 0" >> /etc/fstab
        swapon -a
    fi
fi
}

setup_mail () {

# fix hostname for postfix
REALHOSTNAME=`hostname -f`
if [ -z "$REALHOSTNAME" ]; then
        for i in `ip -f inet -o addr show scope global | awk '{print $4}' | awk -F \/ '{print $1}'`; do
                for j in `dig +noall +answer +time=2 +tries=1 -x $i | awk '{print $5}' | sed 's/\.$//'`; do
                        if [ -n "$j" ]; then
                                REALHOSTNAME=$j
                                break 2
                        fi
                done
        done
fi
if [ -n "$REALHOSTNAME" ]; then
        echo "$REALHOSTNAME" > /etc/HOSTNAME
fi
SuSEconfig --module postfix
}

setup_hostname() {
    # The SUSE Manager server needs to have the same hostname as the·
    # old satellite server.·

    cp /etc/hosts /etc/hosts.backup.suse.manager

    # change the hostname to the satellite hostname
    hostname $SATELLITE_HOST

    # modify /etc/hosts to fake the own hostname
    #
    # add line·
    # <ip>  <fqdn> <shortname>
    #
    echo -e "\n$MANAGER_IP $SATELLITE_FQDN $SATELLITE_HOST" >> /etc/hosts

    # test if the output of "hostname -f" is equal to $SATELLITE_FQDN
    # test if "ping $SATELLITE_HOST" ping the own host
}

cleanup_hostname() {
    if [ -f /etc/hosts.backup.suse.manager ]; then
        mv /etc/hosts.backup.suse.manager /etc/hosts
    fi;
}

setup_db_xe() {
    echo -e "9055\n\n$SYS_DB_PASS\n$SYS_DB_PASS\n" | /etc/init.d/oracle-xe configure
    #sed -i "s/:\/usr\/lib\/oracle\/10.2.0.4\/client.*:/:\/usr\/lib\/oracle\/xe\/app\/oracle\/product\/10.2.0\/server:/g" /etc/oratab
    . /etc/profile.d/oracle.sh
    cp /usr/lib/oracle/xe/app/oracle/product/10.2.0/server/network/admin/tnsnames.ora /etc
    restorecon -v /etc/tnsnames.ora
    /etc/init.d/oracle-xe start

    echo "create smallfile tablespace data_tbs datafile '/usr/lib/oracle/xe/oradata/XE/data_01.dbf' SIZE 3800M;
create user $MANAGER_USER identified by \"$MANAGER_PASS\" default tablespace data_tbs;
grant dba to $MANAGER_USER;
alter system set processes = 400 scope=spfile;
alter system set \"_optimizer_filter_pred_pullup\"=false scope=spfile;
alter system set \"_optimizer_cost_based_transformation\"=off scope=spfile;
quit
" > /tmp/dbsetup.sql

    su -s /bin/bash - oracle -c "ORACLE_SID=$MANAGER_DB_NAME sqlplus sys/\"$MANAGER_PASS\"@$MANAGER_DB_NAME as sysdba @/tmp/dbsetup.sql;"
    rm /tmp/dbsetup.sql
}

setup_db_full() {
    /opt/apps/oracle/setup "$SYS_DB_PASS"
    cp /opt/apps/oracle/product/11gR2/dbhome_1/network/admin/tnsnames.ora /etc
    echo "Create database user for SUSE Manager..."
    echo "create user $MANAGER_USER identified by \"$MANAGER_PASS\" default tablespace users;
grant dba to $MANAGER_USER;
alter system set processes = 400 scope=spfile;
quit
" > /tmp/dbsetup.sql

    su -s /bin/bash - oracle -c "ORACLE_SID=$MANAGER_DB_NAME sqlplus sys/\"$SYS_DB_PASS\"@$MANAGER_DB_NAME as sysdba @/tmp/dbsetup.sql;"
    rm /tmp/dbsetup.sql
}

setup_spacewalk() {
    CERT_COUNTRY=`echo -n $CERT_COUNTRY|tr [:lower:] [:upper:]`


    echo "admin-email = $MANAGER_ADMIN_EMAIL
ssl-set-org = $CERT_O
ssl-set-org-unit = $CERT_OU
ssl-set-city = $CERT_CITY
ssl-set-state = $CERT_STATE
ssl-set-country = $CERT_COUNTRY
ssl-password = $CERT_PASS
ssl-set-email = $CERT_EMAIL
ssl-config-sslvhost = Y
ssl-ca-cert-expiration = 10
ssl-server-cert-expiration = 10
db-backend=oracle
db-user=$MANAGER_USER
db-password=$MANAGER_PASS
db-name=$MANAGER_DB_NAME
db-host=$MANAGER_DB_HOST
db-port=$MANAGER_DB_PORT
db-protocol=$MANAGER_DB_PROTOCOL
enable-tftp=$MANAGER_ENABLE_TFTP
ncc-user = $NCC_USER
ncc-pass = $NCC_PASS
ncc-email = $NCC_EMAIL
" > /root/spacewalk-answers

    /etc/init.d/cobblerd start
    rcapache2 start
    /usr/bin/spacewalk-setup --ncc --answer-file=/root/spacewalk-answers
    if [ "x" = "x$MANAGER_MAIL_FROM" ]; then
        MY_DOMAIN=`hostname -d`
        MANAGER_MAIL_FROM="SUSE Manager <root@$MY_DOMAIN>"
    fi
    if ! grep "^web.default_mail_from" /etc/rhn/rhn.conf > /dev/null; then
        echo "web.default_mail_from = $MANAGER_MAIL_FROM" >> /etc/rhn/rhn.conf
    fi
    rm /root/spacewalk-answers
}

drop_manager_db() {
    /usr/sbin/spacewalk-service stop
    /etc/init.d/oracle-xe start
    echo "drop user $MANAGER_USER cascade;
create user $MANAGER_USER identified by \"$MANAGER_PASS\" default tablespace data_tbs;
grant dba to $MANAGER_USER;
quit
" > /tmp/dbnewspacewalkuser.sql

    su -s /bin/bash - oracle -c "ORACLE_SID=$MANAGER_DB_NAME sqlplus sys/\"${SYS_DB_PASS}\"@${MANAGER_DB_NAME} as sysdba @/tmp/dbnewspacewalkuser.sql;"
    rm /tmp/dbnewspacewalkuser.sql
}

dump_remote_db() {

    if [ ! -f /tmp/sat.oracleXE.dmp ];then
        echo "rrxe =
  (DESCRIPTION =
    (ADDRESS_LIST =
      (ADDRESS = (PROTOCOL = TCP)(HOST = $SATELLITE_IP)(PORT = 1521))
    )
    (CONNECT_DATA =
      (SID = $SATELLITE_DB_SID)
    )
  )
" >> /etc/tnsnames.ora

        su - oracle -c "ORACLE_HOME=/usr/lib/oracle/xe/app/oracle/product/10.2.0/server/ /usr/lib/oracle/xe/app/oracle/product/10.2.0/server/bin/exp \"$SATELLITE_DB_USER\"/\"$SATELLITE_DB_PASS\"@rrxe owner=$SATELLITE_DB_USER compress=n consistent=y statistics=none file=/tmp/sat.oracleXE.dmp log=/tmp/rhn.oracleXE.log"
    else
        echo "database dump exists. Skipping dump of remote db"
    fi;
}

import_db() {
    MANAGER_DB_NAME=`echo -n $MANAGER_DB_NAME|tr [:lower:] [:upper:]`
    su - oracle -c "ORACLE_HOME=/usr/lib/oracle/xe/app/oracle/product/10.2.0/server PATH=$PATH:/usr/lib/oracle/xe/app/oracle/product/10.2.0/server/bin imp system/$SYS_DB_PASS@$MANAGER_DB_NAME fromuser=$SATELLITE_DB_USER touser=$MANAGER_USER file=/tmp/sat.oracleXE.dmp log=/tmp/spacewalk.oracleXE.imp.log ignore=y"
    # 'fix syntax HL
}

upgrade_schema() {
    spacewalk-schema-upgrade
    su -s /bin/bash - oracle -c "ORACLE_SID=$MANAGER_DB_NAME sqlplus sys/\"$SYS_DB_PASS\"@$MANAGER_DB_NAME as sysdba <<ENDPLUS @/usr/lib/oracle/xe/app/oracle/product/10.2.0/server/rdbms/admin/utlrp.sql; exit;ENDPLUS"
}

copy_remote_files() {
    echo -n "Files from the old satellite are copied now. You have to enter the Satellite root password multiple times. Press return now to start."; read dummy
    # maybe add -H for hardlinks?
    rsync -avz $SATELLITE_IP:/var/satellite/ /var/spacewalk/
    chown -R wwwrun.www /var/spacewalk
    # copy only new files (new kickstart profiles, snippets, trigger, etc.)
    rsync -a -v -z --ignore-existing $SATELLITE_IP:/var/lib/cobbler/ /var/lib/cobbler/
    # cobbler needs also running apache, so let's restart complete spacewalk
    /etc/init.d/cobblerd restart
    spacewalk-service restart
    # wait for cobblerd
    sleep 10
    cobbler sync

    mkdir -p /root/backup/pub
    mkdir -p /root/backup/ssl/jabberd
    mv /srv/www/htdocs/pub/RHN-ORG-TRUSTED-SSL-CERT /root/backup/pub/
    mv /srv/www/htdocs/pub/rhn-org-trusted-ssl-cert*.rpm /root/backup/pub/
    mv /root/ssl-build /root/backup/
    cp /etc/apache2/ssl.crt/spacewalk.crt /root/backup/ssl/
    cp /etc/apache2/ssl.key/spacewalk.key /root/backup/ssl/
    cp /etc/pki/spacewalk/jabberd/server.pem /root/backup/ssl/jabberd/

    rsync -avz --ignore-existing $SATELLITE_IP:/var/www/html/pub/ /srv/www/htdocs/pub/
    rsync -avz $SATELLITE_IP:/root/ssl-build /root/

    # Copy the webserver cert and key from satellite to Manager
    # On satellite look at /etc/httpd/conf.d/ssl.conf for the keys
    # SSLCertificateFile and SSLCertificateKeyFile

    # Copy the files given files to the Manager server to·
    # SSLCertificateFile => /etc/apache2/ssl.crt/spacewalk.crt
    # SSLCertificateFile => /etc/pki/spacewalk/jabberd/server.pem
    # SSLCertificateKeyFile => /etc/apache2/ssl.key/spacewalk.key

    scp root@$SATELLITE_IP:/etc/pki/tls/certs/spacewalk.crt /etc/apache2/ssl.crt/spacewalk.crt
    cp /etc/apache2/ssl.crt/spacewalk.crt /etc/pki/spacewalk/jabberd/server.pem
    scp root@$SATELLITE_IP:/etc/pki/tls/private/spacewalk.key /etc/apache2/ssl.key/spacewalk.key

    rsync -a -v -z $SATELLITE_IP:/var/lib/rhn/kickstarts /var/lib/rhn/
    chown -R tomcat.tomcat /var/lib/rhn/kickstarts

    rsync -a -v -z --exclude='libexec/*' $SATELLITE_IP:/var/lib/nocpulse/ /var/lib/nocpulse/
    chown -R nocpulse.nocpulse /var/lib/nocpulse

    # You need to remove the extra line from /etc/hosts added·
    # at the beginning.
}

do_migration() {
    if [ "x" = "x$SATELLITE_HOST" ]; then
        echo -n "SATELLITE_HOST:";   read SATELLITE_HOST
        echo -n "SATELLITE_DOMAIN:"; read SATELLITE_DOMAIN
        echo -n "SATELLITE_DB_USER"; read SATELLITE_DB_USER
        echo -n "SATELLITE_DB_PASS"; read SATELLITE_DB_PASS
        echo -n "SATELLITE_DB_SID";  read SATELLITE_DB_SID
        echo -n "MANAGER_IP";        read MANAGER_IP
        echo -n "MANAGER_USER";      read MANAGER_USER
        echo -n "MANAGER_PASS";      read MANAGER_PASS
    fi;
    setup_hostname

    # those values will be overwritten by the copied certificate
    CERT_O="dummy"
    CERT_OU="dummy"
    CERT_CITY="dummy"
    CERT_STATE="dummy"
    CERT_COUNTRY="DE"
    CERT_PASS="dummy"
    CERT_EMAIL="dummy@example.net"
    MANAGER_ENABLE_TFTP="n"


    if [ ! -f "/usr/lib/oracle/xe/oradata/XE/data_01.dbf" ]; then
        do_setup
    fi;
    if [ $MANAGER_DB_NAME = "xe" -a $MANAGER_DB_HOST = "localhost" ]; then
        drop_manager_db
    fi;
    dump_remote_db
    import_db
    upgrade_schema
    copy_remote_files

    mv /var/spacewalk/redhat /var/spacewalk/packages
    cleanup_hostname
}

do_setup() {
    if [ -f $SETUP_ENV ]; then
        . $SETUP_ENV
        if [ -z $SYS_DB_PASS ]; then
            SYS_DB_PASS=$MANAGER_PASS
        fi
    else
        echo -n "MANAGER_IP=";          read MANAGER_IP
        echo -n "MANAGER_USER=";        read MANAGER_USER
        echo -n "MANAGER_PASS=";        read MANAGER_PASS
        echo -n "MANAGER_ADMIN_EMAIL="; read MANAGER_ADMIN_EMAIL
        echo -n "CERT_O="             ; read CERT_O
        echo -n "CERT_OU="            ; read CERT_OU
        echo -n "CERT_CITY="          ; read CERT_CITY
        echo -n "CERT_STATE="         ; read CERT_STATE
        echo -n "CERT_COUNTRY="       ; read CERT_COUNTRY
        echo -n "CERT_EMAIL="         ; read CERT_EMAIL
        echo -n "CERT_PASS="          ; read CERT_PASS
        echo -n "MANAGER_DB_NAME="    ; read MANAGER_DB_NAME
        echo -n "MANAGER_DB_HOST="    ; read MANAGER_DB_HOST
        echo -n "MANAGER_DB_PORT="    ; read MANAGER_DB_PORT
        echo -n "MANAGER_DB_PROTOCOL="; read MANAGER_DB_PROTOCOL
        echo -n "MANAGER_ENABLE_TFTP="; read MANAGER_ENABLE_TFTP
        echo -n "NCC_USER="           ; read NCC_USER
        echo -n "NCC_PASS="           ; read NCC_PASS
        echo -n "NCC_EMAIL="          ; read NCC_EMAIL
    fi;
    setup_swap
    setup_mail
    if [ $MANAGER_DB_HOST = "localhost" ]; then
        if [ $ORACLE_VERSION = "XE" ]; then
            if [ -f "/usr/lib/oracle/xe/oradata/XE/data_01.dbf" ]; then
                echo "Database already setup. Abort."
                exit 1
            fi
            setup_db_xe
        else
            MANAGER_DB_NAME="susemanager"
            SYS_DB_PASS=`dd if=/dev/urandom bs=16 count=4 2> /dev/null | md5sum | cut -b 1-8`
            setup_db_full
        fi
    fi

    # should be done by cobbler with "--sync" but we had a case where those
    # files were missing (bnc#668908)
    cp /usr/share/syslinux/menu.c32 /srv/tftpboot/
    cp /usr/share/syslinux/pxelinux.0 /srv/tftpboot/

    if [ ! -d "/var/spacewalk" ]; then
        setup_spacewalk
    else
        echo "SUSE Manager is already initialized. Skipping setup."
    fi;
}

for p in $@; do
    if [ "$LOGFILE" = "1" ]; then
        LOGFILE=$p
        continue
    fi

    case "$p" in
    -m)
        DO_MIGRATION=1
        . $MIGRATION_ENV 2> /dev/null
        . $SETUP_ENV
        SATELLITE_FQDN="$SATELLITE_HOST.$SATELLITE_DOMAIN"
        SATELLITE_IP=`dig +short $SATELLITE_FQDN`
        sed -i 's/^DHCLIENT_SET_HOSTNAME.*/DHCLIENT_SET_HOSTNAME="no"/' /etc/sysconfig/network/dhcp 2> /dev/null
       ;;
    -s)
        DO_SETUP=1
        sed -i 's/^DHCLIENT_SET_HOSTNAME.*/DHCLIENT_SET_HOSTNAME="no"/' /etc/sysconfig/network/dhcp 2> /dev/null
       ;;
    -r)
        . $MIGRATION_ENV 2> /dev/null
        . $SETUP_ENV
        SATELLITE_FQDN="$SATELLITE_HOST.$SATELLITE_DOMAIN"
        SATELLITE_IP=`dig +short $SATELLITE_FQDN`
        copy_remote_files
       ;;
    -h)
        help
       ;;
    -l)
        LOGFILE="1"
        ;;
    -w)
        WAIT_BETWEEN_STEPS=1
        ;;
    *)
       echo "That option is not recognized"
       ;;
    esac
done

rpm -q oracle-xe-univ > /dev/null
if [ $? -eq "0" ]; then
    ORACLE_VERSION="XE"
else
    ORACLE_VERSION="FULL"
fi

if [ "$LOGFILE" != "0" ]; then
    #set -x
    exec >> >(tee $LOGFILE | sed 's/^/  /' ) 2>&1
fi

if [ $WAIT_BETWEEN_STEPS = "1" ];then
    echo "Press Return to continue"
    read
fi;
if [ "$DO_SETUP" = "1" ]; then
    do_setup
    # rename the default org
    echo "UPDATE $MANAGER_USER.web_customer SET name = '$CERT_O' WHERE id = 1;
quit
" > /tmp/changeorg.sql

    su -s /bin/bash - oracle -c "ORACLE_SID=$MANAGER_DB_NAME sqlplus $MANAGER_USER/\"$MANAGER_PASS\"@$MANAGER_DB_NAME @/tmp/changeorg.sql;"
    rm /tmp/changeorg.sql

    if [ $ORACLE_VERSION = "FULL" ]; then
        echo "# Oracle sys password: $SYS_DB_PASS" >> /etc/rhn/rhn.conf
    fi

    # Finaly call mgr-ncc-sync
    /usr/sbin/mgr-ncc-sync
fi
if [ $WAIT_BETWEEN_STEPS = "1" ];then
    echo "Press Return to continue"
    read
fi;
if [ "$DO_MIGRATION" = "1" ]; then
    do_migration
    # Finaly call mgr-ncc-sync
    /usr/sbin/mgr-ncc-sync
fi


# vim: set expandtab:
