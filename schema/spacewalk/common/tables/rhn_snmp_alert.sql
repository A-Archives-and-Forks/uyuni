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


CREATE TABLE rhn_snmp_alert
(
    recid              NUMBER(12) NOT NULL
                           CONSTRAINT rhn_snmpa_recid_pk PRIMARY KEY
                           USING INDEX TABLESPACE [[2m_tbs]],
    sender_cluster_id  NUMBER(12) NOT NULL,
    dest_ip            VARCHAR2(255) NOT NULL,
    dest_port          NUMBER(5) NOT NULL,
    date_generated     timestamp with local time zone,
    date_submitted     timestamp with local time zone,
    command_name       VARCHAR2(255),
    notif_type         NUMBER(5),
    op_center          VARCHAR2(255),
    notif_url          VARCHAR2(255),
    os_name            VARCHAR2(128),
    message            VARCHAR2(2000),
    probe_id           NUMBER(12),
    host_ip            VARCHAR2(255),
    severity           NUMBER(5),
    command_id         NUMBER(12),
    probe_class        NUMBER(5),
    host_name          VARCHAR2(255),
    support_center     VARCHAR2(255)
)
ENABLE ROW MOVEMENT
;

COMMENT ON TABLE rhn_snmp_alert IS 'snmpa  snmp alerts';

CREATE INDEX rhn_snmp_alrt_scid_idx
    ON rhn_snmp_alert (sender_cluster_id)
    TABLESPACE [[64k_tbs]]
    NOLOGGING;

CREATE SEQUENCE rhn_snmp_alert_recid_seq;

ALTER TABLE rhn_snmp_alert
    ADD CONSTRAINT rhn_snmp_alert_sat_cluster_fk FOREIGN KEY (sender_cluster_id)
    REFERENCES rhn_sat_cluster (recid);

