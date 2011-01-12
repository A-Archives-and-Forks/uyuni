# -*- coding: utf-8 -*-
#
# Copyright (c) 2010 Novell
#
# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.
#

import string

from spacewalk.common import UserDictCase, log_debug, log_error, rhnFault, Traceback
from spacewalk.server import rhnSQL

class SuseData:
  def __init__(self):
    log_debug(4, "SuseData initialized")

  def create_update_suse_products(self, sysid, guid, secret, ostarget, products):
    log_debug(4, sysid, guid, ostarget, products)

    # search, if a suseServer with this guid exists which is not this server
    # this would indicate a re-registration and we need to remove the old rhnServer
    h = rhnSQL.prepare("""
    SELECT
           rhn_server_id as id
      FROM suseServer
     WHERE guid = :guid
       AND rhn_server_id != :sysid
    """)
    h.execute(sysid = sysid, guid=guid)
    d = h.fetchone_dict()
    if d:
      old_sysid = d['id']
      log_debug(1, "Found duplicate server:", old_sysid)
      delete_server = rhnSQL.Procedure("delete_server")
      try:
        if old_sysid != None:
          delete_server(old_sysid)
      except rhnSQL.SQLError:
        log_error("Error deleting server: %s" % old_sysid)
      # IF we delete rhnServer all reference are deleted too
      #
      # now switch suseServer to new id
      #h = rhnSQL.prepare("""
      #  UPDATE suseServer
      #     SET rhn_server_id = :sysid
      #  WHERE rhn_server_id = :oldsysid
      #""")
      #h.execute(sysid=sysid, oldsysid=old_sysid);

    # remove this guid from suseDelServer list
    h = rhnSQL.prepare("""
      DELETE FROM suseDelServer
      WHERE guid = :guid
    """)
    h.execute(guid=guid)
    rhnSQL.commit()

    # search if suseServer with ID sysid exists
    h = rhnSQL.prepare("""
      SELECT
        rhn_server_id as id,
        guid,
        secret,
        ostarget,
        ncc_sync_required
      FROM suseServer
      WHERE rhn_server_id = :sysid
    """)
    h.execute(sysid = sysid)
    t = h.fetchone_dict()
    ncc_sync_required = False

    # if not; create new suseServer
    if not t:
      ncc_sync_required = True
      h = rhnSQL.prepare("""
        INSERT INTO suseServer
          (rhn_server_id, guid, secret, ostarget)
          values (:sysid, :guid, :secret, :ostarget)
      """)
      h.execute(sysid=sysid, guid=guid, secret=secret, ostarget=ostarget)
    else:
    # if yes, read values and compare them with the provided data
    # update if needed
      data = {
        'rhn_server_id' : sysid,
        'guid' : guid,
        'secret' : secret,
        'ostarget' : ostarget
      }

      if t['guid'] != guid or t['secret'] != secret or t['ostarget'] != ostarget:
        ncc_sync_required = True
        h = rhnSQL.prepare("""
          UPDATE suseServer
             SET guid = :guid,
                 secret = :secret,
                 ostarget = :ostarget
           WHERE rhn_server_id = :rhn_server_id
        """)
        apply(h.execute, (), data)
    # check products
    h = rhnSQL.prepare("""
      SELECT
          suse_installed_product_id as id
        FROM suseServerInstalledProduct
       WHERE rhn_server_id = :sysid
    """)
    h.execute(sysid=sysid)
    existing_products = map(lambda x: x['id'], h.fetchall_dict() or [])

    for product in products:
      sipid = self.get_installed_product_id(product)
      if sipid in existing_products:
        existing_products.remove(sipid)
        continue
      h = rhnSQL.prepare("""
        INSERT INTO suseServerInstalledProduct
        (rhn_server_id, suse_installed_product_id)
        VALUES(:sysid, :sipid)
      """)
      h.execute(sysid=sysid, sipid=sipid)
      ncc_sync_required = True

    for pid in existing_products:
      h = rhnSQL.prepare("""
        DELETE from suseServerInstalledProduct
         WHERE rhn_server_id = :sysid
           AND suse_installed_product_id = :pid
      """)
      h.execute(sysid=sysid, pid=pid)
      ncc_sync_required = True

    if ncc_sync_required:
      # If the data have changed, we set the
      # sync_required flag and reset the errors
      # flag to give the registration another try
      h = rhnSQL.prepare("""
        UPDATE suseServer
           SET ncc_sync_required = 'Y',
               ncc_reg_error = 'N'
        WHERE rhn_server_id = :sysid
      """)
      h.execute(sysid=sysid)
    rhnSQL.commit()


  def get_installed_product_id(self, product):
    h = rhnSQL.prepare("""
      SELECT sip.id
        FROM suseInstalledProduct sip
         JOIN rhnPackageArch rpa ON sip.arch_type_id = rpa.id
       WHERE sip.name = :name
         AND sip.version = :version
         AND rpa.label = :arch
         AND sip.release = :release
         AND sip.is_baseproduct = :baseproduct
    """)
    apply(h.execute, (), product)
    d = h.fetchone_dict()
    if not d:
      # not available yet, so let's create one
      n = rhnSQL.prepare("""
        INSERT INTO suseInstalledProduct
        (id, name, version, arch_type_id, release, is_baseproduct)
        VALUES (sequence_nextval('suse_inst_pr_id_seq'), :name, :version,
               (SELECT id FROM rhnPackageArch WHERE label = :arch),
               :release, :baseproduct)
      """)
      apply(n.execute, (), product)
      apply(h.execute, (), product)
      d = h.fetchone_dict()
      if not d:
        # should never happen
        log_error("Unable to create installed product item %s-%s-%s-%s" % (
          product['name'], product['version'], product['release'], product['arch']))
        return None

    return d['id']
