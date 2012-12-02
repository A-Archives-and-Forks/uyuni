--
-- Copyright (c) 2008--2012 Red Hat, Inc.
--
-- This software is licensed to you under the GNU General Public License,
-- version 2 (GPLv2). There is NO WARRANTY for this software, express or
-- implied, including the implied warranties of MERCHANTABILITY or FITNESS
-- FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
-- along with this software; if not, see
-- http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.
--
-- Red Hat trademarks are not licensed under GPLv2. No permission is
-- granted to use or replicate Red Hat trademarks that are incorporated
-- in this software or its documentation.
--


CREATE TABLE rhn_deployed_probe
(
    recid                          NUMBER(12) NOT NULL
                                       CONSTRAINT rhn_dprob_recid_pk PRIMARY KEY
                                       USING INDEX TABLESPACE [[8m_tbs]],
    probe_type                     VARCHAR2(15) NOT NULL,
    description                    VARCHAR2(255),
    customer_id                    NUMBER(12) NOT NULL,
    command_id                     NUMBER(16) NOT NULL,
    contact_group_id               NUMBER(12),
    os_id                          NUMBER(12),
    notify_critical                CHAR(1),
    notify_warning                 CHAR(1),
    notify_recovery                CHAR(1),
    notify_unknown                 CHAR(1),
    notification_interval_minutes  NUMBER(16) NOT NULL,
    check_interval_minutes         NUMBER(16) NOT NULL,
    retry_interval_minutes         NUMBER(16) NOT NULL,
    max_attempts                   NUMBER(16),
    sat_cluster_id                 NUMBER(12),
    parent_probe_id                NUMBER(12),
    last_update_user               VARCHAR2(40),
    last_update_date               timestamp with local time zone
)
ENABLE ROW MOVEMENT
;

COMMENT ON TABLE rhn_deployed_probe IS 'dprob  deployed_probe definitions';

CREATE INDEX rhn_dprob_check_command_id_idx
    ON rhn_deployed_probe (command_id)
    TABLESPACE [[8m_tbs]];

CREATE INDEX rhn_dprob_customer_id_idx
    ON rhn_deployed_probe (customer_id)
    TABLESPACE [[8m_tbs]];

CREATE INDEX rhn_dprob_sat_cluster_id_idx
    ON rhn_deployed_probe (sat_cluster_id)
    TABLESPACE [[8m_tbs]];

