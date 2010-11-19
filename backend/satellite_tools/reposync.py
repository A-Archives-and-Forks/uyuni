# -*- coding: utf-8 -*-
#
# Copyright (c) 2008--2010 Red Hat, Inc.
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
#
import sys, os, time, grp
import hashlib
from datetime import datetime
from optparse import OptionParser
from spacewalk.server import rhnPackage, rhnSQL, rhnChannel, rhnPackageUpload
from spacewalk.common import CFG, initCFG, rhnLog, fetchTraceback, rhn_rpm
from spacewalk.common.checksum import getFileChecksum
from spacewalk.common.rhn_mpm import InvalidPackageError
from spacewalk.server.importlib.importLib import IncompletePackage, Erratum
from spacewalk.server.importlib.backendOracle import OracleBackend
from spacewalk.server.importlib.packageImport import ChannelPackageSubscription
from spacewalk.server.importlib.errataImport import ErrataImport
from spacewalk.server import taskomatic

from spacewalk.server.rhnSQL.const import ORACLE, POSTGRESQL

default_log_location = '/var/log/rhn/reposync/'
default_hash = 'sha256'

class RepoSync:
   
    parser = None
    type = None
    urls = None
    channel_label = None
    channel = None
    fail = False
    quiet = False
    regen = False

    def main(self):
        initCFG('server')
        db_string = CFG.DEFAULT_DB #"rhnsat/rhnsat@rhnsat"
        rhnSQL.initDB(db_string)
        (options, args) = self.process_args()

        log_filename = 'reposync.log'
        if options.channel_label:
            date = time.localtime()
            datestr = '%d.%02d.%02d-%02d:%02d:%02d' % (date.tm_year, date.tm_mon, date.tm_mday, date.tm_hour, date.tm_min, date.tm_sec)
            log_filename = options.channel_label + '-' +  datestr + '.log'
           
        rhnLog.initLOG(default_log_location + log_filename)
        #os.fchown isn't in 2.4 :/
        os.system("chgrp www " + default_log_location + log_filename)


        quit = False
        if not options.url:
            if options.channel_label:
                # TODO:need to look at user security across orgs
                h = rhnSQL.prepare("""select s.source_url
                                      from rhnContentSource s,
                                           rhnChannelContentSource cs,
                                           rhnChannel c
                                     where s.id = cs.source_id
                                       and cs.channel_id = c.id
                                       and c.label = :label""")
                h.execute(label=options.channel_label)
                source_urls = h.fetchall_dict() or []
                if source_urls:
                    self.urls = [row['source_url'] for row in source_urls]
                else:
                    quit = True
                    self.error_msg("Channel has no URL associated")
        else:
            self.urls = [options.url]
        if not options.channel_label:
            quit = True
            self.error_msg("--channel must be specified")

        self.log_msg("\nSync started: %s" % (time.asctime(time.localtime())))
        self.log_msg(str(sys.argv))


        if quit:
            sys.exit(1)

        self.type = options.type
        self.channel_label = options.channel_label
        self.fail = options.fail
        self.quiet = options.quiet
        self.channel = self.load_channel()

        if not self.channel or not rhnChannel.isCustomChannel(self.channel['id']):
            print "Channel does not exist or is not custom"
            sys.exit(1)

        for url in self.urls:
            plugin = self.load_plugin()(url, self.channel_label)
            self.import_packages(plugin, url)
            self.import_updates(plugin, url)
        if self.regen:
            taskomatic.add_to_repodata_queue_for_channel_package_subscription(
                [self.channel_label], [], "server.app.yumreposync")
        self.update_date()
        rhnSQL.commit()        
        self.print_msg("Sync complete")


    def update_date(self):
        """ Updates the last sync time"""
        h = rhnSQL.prepare( """update rhnChannel set LAST_SYNCED = current_timestamp
                             where label = :channel""")
        h.execute(channel=self.channel['label'])

    def process_args(self):
        self.parser = OptionParser()
        self.parser.add_option('-u', '--url', action='store', dest='url', help='The url to sync')
        self.parser.add_option('-c', '--channel', action='store', dest='channel_label', help='The label of the channel to sync packages to')
        self.parser.add_option('-t', '--type', action='store', dest='type', help='The type of repo, currently only "yum" is supported', default='yum')
        self.parser.add_option('-f', '--fail', action='store_true', dest='fail', default=False , help="If a package import fails, fail the entire operation")
        self.parser.add_option('-q', '--quiet', action='store_true', dest='quiet', default=False, help="Print no output, still logs output")
        return self.parser.parse_args()

    def load_plugin(self):
        name = self.type + "_src"
        mod = __import__('spacewalk.satellite_tools.repo_plugins', globals(), locals(), [name])
        submod = getattr(mod, name)
        return getattr(submod, "ContentSource")
        
    def import_updates(self, plug, url):
      notices = plug.get_updates()
      self.print_msg("Repo " + url + " has " + str(len(notices)) + " patches.")
      
      for notice in notices:
        self.print_msg( str(notice) )
        
      self.upload_updates(notices)
      
    def upload_updates(self, notices):
      batch = []
      typemap = { 
                  'security'    : 'Security Advisory',
                  'recommended' : 'Bug Fix Advisory',
                  'optional'    : 'Product Enhancement Advisory'
                }
      for notice in notices:
        e = Erratum()
        e['advisory'] = notice['update_id'] + "-" + notice['version']
        e['advisory_name'] = notice['update_id']
        e['advisory_rel'] = notice['version']
        e['advisory_type'] = typemap[notice['type']]
        e['product'] =  notice['release']
        e['description'] = notice['description']
        e['synopsis'] = notice['title']
        e['topic'] = ' '
        e['solution'] = ' '
        e['issue_date'] = datetime.fromtimestamp(float(notice['issued'])).isoformat(' ')
        if notice['updated'] is not None:
          e['update_date'] = notice['updated']
        else:
          e['update_date'] = e['issue_date']
        #e['last_modified'] = notice['']
        e['notes'] = ''
        e['org_id'] = self.channel['org_id']
        e['refers_to'] = ''
        e['channels'] = [{'label':self.channel_label}]
        e['packages'] = []
        e['files'] = []
        
        self.print_msg( notice['pkglist'] )
        for pkg in notice['pkglist'][0]['packages']:
          
          h = rhnSQL.prepare("""select p.id, pevr.epoch, c.checksum, c.checksum_type
          from rhnPackage p,
          rhnPackagename pn,
          rhnpackageevr  pevr,
          rhnpackagearch pa,
          rhnChecksumView c
          where pn.name = :name
          and p.org_id = :org_id
          and pevr.version = :version
          and pevr.release = :release
          and pa.label = :arch
          and pa.arch_type_id = 1
          and p.checksum_id = c.id
          and p.name_id = pn.id
          and p.evr_id = pevr.id
          and p.package_arch_id = pa.id
          """)
          h.execute(name=pkg['name'], version=pkg['version'], release=pkg['release'], 
                    arch=pkg['arch'], org_id=self.channel['org_id'])
          cs = h.fetchall_dict() or []
          sums = cs[0]
          package = IncompletePackage()
          for k in pkg.keys():
            package[k] = pkg[k]
          package['epoch'] = pkg.get('epoch', '')
          package['org_id'] = self.channel['org_id']
          
          package['checksums'] = {sums['checksum_type'] : sums['checksum']}
          package['checksum_type'] = sums['checksum_type']
          package['checksum'] = sums['checksum']
          
          package['package_id'] = sums['id']
          self.print_msg( package )
          e['packages'].append(package)
          
        e['keywords'] = []
        if notice['reboot_suggested']:
          e['keywords'].append({'keyword':'reboot_suggested'})
        if notice['restart_suggested']:
          e['keywords'].append({'keyword':'restart_suggested'})
        e['bugs'] = []
        bzs = filter(lambda r: r['type'] == 'bugzilla', notice['references'])
        if len(bzs):
          tmp = {}
          for bz in bzs:
            if bz['id'] not in tmp:
              e['bugs'].append({'bug_id' : bz['id'], 'summary' : bz['title']})
              tmp[bz['id']] = None
        e['cve'] = []
        cves = filter(lambda r: r['type'] == 'cve', notice['references'])
        if len(cves):
          tmp = {}
          for cve in cves:
            if cve['id'] not in tmp:
              e['cve'].append(cve['id'])
              tmp[cve['id']] = None
        e['locally_modified'] = None
        batch.append(e)

      backend = OracleBackend()
      backend.init()
      importer = ErrataImport(batch, backend)
      importer.run()
      
    def import_packages(self, plug, url):
        packages = plug.list_packages()
        to_link = []
        to_download = []
        self.print_msg("Repo " + url + " has " + str(len(packages)) + " packages.")
        for pack in packages:
                 # we have a few scenarios here:
                 # 1.  package is not on the server (link and download)
                 # 2.  package is in the server, but not in the channel (just link if we can)
                 # 3.  package is in the server and channel, but not on the file system (just download)
                 path = rhnPackage.get_path_for_package([pack.name, pack.version, pack.release,\
                        pack.epoch, pack.arch], self.channel_label)
                 if not path:
                     path = rhnPackage.get_path_for_package([pack.name, pack.version, pack.release,\
                        '', pack.arch], self.channel_label)

                 if path:
                     if os.path.exists(os.path.join(CFG.MOUNT_POINT, path)):
                         continue
                     else:
                         to_download.append(pack)
                         continue

                 # we know that it's not in the channel, lets try to check the server by checksum!
                 #for some repos (sha256), we can check to see if we have them by
                 #  checksum and not bother downloading.  For older repos, we only
                 #  have sha1, which satellite doesn't track
                 # regardless we have to link the package
                 to_link.append(pack)

                 found = False
                 for type,sum  in pack.checksums.items():
                     if type == 'sha': #we use sha1 (instead of sha)
                         type = 'sha1'
                     path = rhnPackage.get_path_for_checksum(self.channel['org_id'],\
                                type, sum)
                     if path and os.path.exists(os.path.join(CFG.MOUNT_POINT, path)):
                             found = True
                             break
                 if not found:
                     to_download.append(pack)


        if len(to_download) == 0:
            self.print_msg("No new packages to download.")
        else:
            self.regen=True
        is_non_local_repo = (url.find("file://") < 0)
        for (index, pack) in enumerate(to_download):
            """download each package"""
            # try/except/finally doesn't work in python 2.4 (RHEL5), so here's a hack
            try:
                try:
                    self.print_msg(str(index+1) + "/" + str(len(to_download)) + " : "+ \
                          pack.getNVREA())
                    path = plug.get_package(pack)
                    self.upload_package(pack, path)
                    if pack in to_link:
                        self.associate_package(pack)
                except KeyboardInterrupt:
                    raise
                except Exception, e:
                   self.error_msg(e)
                   if self.fail:
                       raise
                   continue
            finally:
                if is_non_local_repo:
                    os.remove(path)

        for (index, pack) in enumerate(to_link):
            """Link each package that wasn't already linked in the previous step"""
            try:
                if pack not in to_download:
                    self.associate_package(pack)
            except KeyboardInterrupt:
                raise
            except Exception, e:
                self.error_msg(e)
                if self.fail:
                    raise
                continue

    
    def upload_package(self, package, path):
        temp_file = open(path, 'rb')
        header, payload_stream, header_start, header_end = \
                rhnPackageUpload.load_package(temp_file)
        package.checksum_type = header.checksum_type()
        package.checksum = getFileChecksum(package.checksum_type, file=temp_file)

        rel_package_path = rhnPackageUpload.relative_path_from_header(
                header, self.channel['org_id'],
                package.checksum_type, package.checksum)
        package_path = os.path.join(CFG.MOUNT_POINT,
                rel_package_path)
        package_dict, diff_level = rhnPackageUpload.push_package(header,
                payload_stream, package.checksum_type, package.checksum,
                force=False,
                header_start=header_start, header_end=header_end,
                relative_path=rel_package_path,
                org_id=self.channel['org_id'])
        temp_file.close()

    def associate_package(self, pack):
        caller = "server.app.yumreposync"
        if CFG.DB_BACKEND == ORACLE:
            from spacewalk.server.importlib.backendOracle import OracleBackend
            backend = OracleBackend()
        elif CFG.DB_BACKEND == POSTGRESQL:
            from spacewalk.server.importlib.backendOracle import PostgresqlBackend
            backend = PostgresqlBackend()
        backend.init()
        package = {}
        package['name'] = pack.name
        package['version'] = pack.version
        package['release'] = pack.release
        package['epoch'] = pack.epoch
        package['arch'] = pack.arch
        package['checksum'] = pack.checksum
        package['checksum_type'] = pack.checksum_type
        package['channels']  = [{'label':self.channel_label, 
                                 'id':self.channel['id']}]
        package['org_id'] = self.channel['org_id']
        try:
           self._importer_run(package, caller, backend)
        except:
            package['epoch'] = ''
            self._importer_run(package, caller, backend)

        backend.commit()

    def _importer_run(self, package, caller, backend):
            importer = ChannelPackageSubscription(
                       [IncompletePackage().populate(package)],
                       backend, caller=caller, repogen=False)
            importer.run()


    def load_channel(self):
        return rhnChannel.channel_info(self.channel_label)


    def print_msg(self, message):
        rhnLog.log_clean(0, message)
        if not self.quiet:
            print message


    def error_msg(self, message):
        rhnLog.log_clean(0, message)
        if not self.quiet:
            sys.stderr.write(str(message) + "\n")

    def log_msg(self, message):
        rhnLog.log_clean(0, message)

    def short_hash(self, str):
        return hashlib.new(default_hash, str).hexdigest()[0:8]

class ContentPackage:

    def __init__(self):
        # map of checksums
        self.checksums = {}
        self.checksum_type = None
        self.checksum = None

        #unique ID that can be used by plugin
        self.unique_id = None

        self.name = None
        self.version = None
        self.release = None
        self.epoch = None
        self.arch = None

    def setNVREA(self, name, version, release, epoch, arch):
        self.name = name
        self.version = version
        self.release = release
        self.arch = arch
        self.epoch = epoch

    def getNVREA(self):
        if self.epoch:
            return self.name + '-' + self.version + '-' + self.release + '-' + self.epoch + '.' + self.arch
        else:
            return self.name + '-' + self.version + '-' + self.release + '.' + self.arch

