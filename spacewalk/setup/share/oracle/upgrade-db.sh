#!/bin/sh
# Upgrades RHN embedded database at mountpoint /rhnsat
#
# Copyright (c) 2008--2012 Red Hat, Inc.
#
# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.
#
# Red Hat trademarks are not licensed under GPLv2. No permission is
# granted to use or replicate Red Hat trademarks that are incorporated
# in this software or its documentation.

set -x

# exit if anything fails
set -e
set -o pipefail

DB_NAME="rhnsat"
DB_USER="rhnsat"

if [ ${#} -gt 0 ]; then
   while [ -n "$1" ] ; do
       case $1 in
       -d | --db | --database )
           shift
           DB_NAME=$1
           ;;
       -u | --user* )
           shift
           DB_USER=$1
           ;;
       * )
           exit -1
           ;;
       esac
       shift
   done
fi

if [ -r "$(dbhome embedded)/dbs/spfilerhnsat.ora" ]; then
	MAJOR_DB_UPGRADE=0
else
	MAJOR_DB_UPGRADE=1
fi

# set oracle environment to embedded server
ORAENV_ASK=NO
ORACLE_SID=embedded
ORACLE_BASE=/opt/apps/oracle
. oraenv

ORACLE_9I_HOME=$(echo $ORACLE_HOME | sed 's|10\.2\.0/db_1|9.2.0|')
ORACLE_ADMIN_DIR=$ORACLE_BASE/admin/10.2.0
ORACLE_ADMIN_9I_DIR=$ORACLE_BASE/admin/9.2.0
ORACLE_CONFIG_DIR=$ORACLE_BASE/config/10.2.0
ORACLE_CONFIG_9I_DIR=$ORACLE_BASE/config/9.2.0

# change env to rhnsat instance
export ORACLE_SID=$DB_NAME

# If the record for satellite database exists, substitute it with new value.
# Otherwise create a new record.
if grep -q "^$ORACLE_SID:.*$" /etc/oratab; then
	# We cannot do in-place edit, since we're running under oracle user and
	# do not have write access to /etc
	oratab=$(sed "s;^$ORACLE_SID:.*$;$ORACLE_SID:$ORACLE_HOME:Y;" /etc/oratab)
	echo "$oratab" > /etc/oratab
else
	echo "$ORACLE_SID:$ORACLE_HOME:Y" >> /etc/oratab
fi

. oraenv

# modify listener
LISTENER_ORA=network/admin/listener.ora
[ -f $ORACLE_HOME/$LISTENER_ORA ] || \
sed "s|\(ORACLE_HOME=.*\)|(ORACLE_HOME=$ORACLE_HOME)|" \
    $ORACLE_9I_HOME/$LISTENER_ORA >$ORACLE_HOME/$LISTENER_ORA

# for 9i -> 10g upgrades, modify db init files
if [ $MAJOR_DB_UPGRADE -gt 0 ]; then
	cp -a $ORACLE_CONFIG_9I_DIR/* $ORACLE_CONFIG_DIR/
	UPGRADE_PFILE=$ORACLE_CONFIG_DIR/upgrade-init$ORACLE_SID.ora
	cat $ORACLE_ADMIN_DIR/init-params.ora  >$UPGRADE_PFILE
	grep --text -E -f - $ORACLE_CONFIG_9I_DIR/spfile$ORACLE_SID.ora \
	    >>$UPGRADE_PFILE <<EOPATTERNS
audit_file_dest
background_dump_dest
control_files
core_dump_dest
db_domain
db_name
instance_name
user_dump_dest
EOPATTERNS
	echo "compatible=10.2.0.4.0" >>$UPGRADE_PFILE
        $ORACLE_ADMIN_DIR/oracle-compute-sga.sh >>$UPGRADE_PFILE
fi

# upgrade the database
if [ $MAJOR_DB_UPGRADE -gt 0 ]; then
	UPGRADE_TMPL=$ORACLE_ADMIN_DIR/embedded-upgradedb.tmpl
else
	UPGRADE_TMPL=$ORACLE_ADMIN_DIR/embedded-upgradedb-10g.tmpl
fi

# sqlplus ... | cat ... is here to fool selinux, since oracle_sqlplus_t
m4 -I$ORACLE_ADMIN_DIR \
   --define RHNORA_DBNAME=$ORACLE_SID \
   --define RHNORA_DATA_PATH=/rhnsat/data/rhnsat \
   --define RHNORA_DB_USER=$DB_USER \
   $UPGRADE_TMPL \
   | $ORACLE_HOME/bin/sqlplus /nolog \
   | cat -

set +x
