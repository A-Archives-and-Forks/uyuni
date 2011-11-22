#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 SUSE LINUX Products GmbH, Nuernberg, Germany.
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

import sys
import unittest
from StringIO import StringIO
from datetime import datetime

from mock import Mock

import spacewalk.satellite_tools.reposync

RTYPE = 'yum' # a valid repotype

class RepoSyncTest(unittest.TestCase):

    def setUp(self):
        # kill logging
        reposync.rhnLog.initLOG = Mock()
        reposync.initLOG = Mock()
        reposync.log_clean = Mock()

        # don't read configs
        reposync.initCFG = Mock()
        reposync.CFG = Mock()

        # catching stdout
        # this could be assertRaisesRegexp in python>=2.7. just sayin'
        self.saved_stdout = sys.stdout
        self.stdout = StringIO()
        sys.stdout = self.stdout

        # catching stderr
        self.saved_stderr = sys.stderr
        self.stderr = StringIO()
        sys.stderr = self.stderr

        self.reposync.os = Mock()
        self.reposync.rhnSQL.initDB = Mock()
        self.reposync.rhnSQL.commit = Mock()

        _mock_rhnsql(self.reposync, 'Label')

    def tearDown(self):
        self.stdout.close()
        sys.stdout = self.saved_stdout

        self.stderr.close()
        sys.stderr = self.saved_stderr

        reload(spacewalk.satellite_tools.reposync)
        
    def test_init_succeeds_with_correct_attributes(self):
        rs = self.reposync.RepoSync('Label', RTYPE)

        self.assertEqual(rs.channel_label, 'Label')

        # these should have been set automatically
        self.assertEqual(rs.fail, False)
        self.assertEqual(rs.quiet, False)
        self.assertEqual(rs.interactive, True)

    def test_init_with_custom_url(self):
        rs = self.reposync.RepoSync('Label', RTYPE, url='http://example.com')

        self.assertEqual(rs.urls, [{'source_url': 'http://example.com',
                                    'metadata_signed': 'N'}])

    def test_init_with_custom_flags(self):
        rs = self.reposync.RepoSync('Label', RTYPE, fail=True, quiet=True,
                               noninteractive=True)

        self.assertEqual(rs.fail, True)
        self.assertEqual(rs.quiet, True)
        self.assertEqual(rs.interactive, False)

    def test_init_wrong_url(self):
        """Test generates empty metadata via taskomatic and quits"""
        # the channel shouldn't be found in the database
        _mock_rhnsql(self.reposync, False)
        self.reposync.taskomatic.add_to_repodata_queue_for_channel_package_subscription = Mock()

        self.assertRaises(SystemExit, self.reposync.RepoSync, 'WrongLabel', RTYPE)

        self.assertTrue(self.reposync.taskomatic.
                        add_to_repodata_queue_for_channel_package_subscription.
                        called)

    def test_init_rhnlog(self):
        """Init rhnLog successfully"""
        rs = reposync.RepoSync('Label', RTYPE)

        self.assertTrue(self.reposync.rhnLog.initLOG.called)

    def test_init_channel(self):
        self.reposync.rhnChannel.channel_info = Mock(return_value=
                                                {'name': 'mocked Channel'})

        rs = self.reposync.RepoSync('Label', RTYPE)

        self.assertEqual(rs.channel, {'name': 'mocked Channel'})
        
    def test_init_bad_channel(self):
        self.reposync.rhnChannel.channel_info = Mock(return_value=None)

        self.assertRaises(SystemExit, self.reposync.RepoSync, 'Label', RTYPE)

    def test_init_bad_repo_type(self):
        self.assertRaises(SystemExit, self.reposync.RepoSync, 'Label',
                          'bad-repo-type')
        self.assertEqual("Repository type bad-repo-type is not supported. "
                         "Could not import "
                         "spacewalk.satellite_tools."
                         "repo_plugins.bad-repo-type_src.\n",
                         self.stderr.getvalue())

    def test_sync_success_no_regen(self):
        rs = self.reposync.RepoSync("Label", RTYPE)

        rs.urls = [{"source_url": "bogus-url", "metadata_signed": "N"}]

        rs = self._mock_sync(rs)
        rs.sync()

        self.assertEqual(rs.repo_plugin.call_args,
                         (('bogus-url', rs.channel_label, True, False, True),
                          {'proxy_pass': rs.mocked_proxy_pass,
                           'proxy_user': rs.mocked_proxy_user,
                           'proxy': rs.mocked_proxy}))
        self.assertEqual(rs.print_msg.call_args, (("Sync complete",), {}))

        self.assertEqual(rs.import_packages.call_args,
                         ((rs.mocked_plugin, "bogus-url"), {}))
        self.assertEqual(rs.import_updates.call_args,
                         ((rs.mocked_plugin, "bogus-url"), {}))

        # for the rest just check if they were called or not
        self.assertTrue(rs.update_date.called)
        # these aren't supposed to be called unless self.regen is True
        self.assertFalse(self.reposync.taskomatic.add_to_repodata_queue_for_channel_package_subscription.called)
        self.assertFalse(self.reposync.taskomatic.add_to_erratacache_queue.called)

    def test_sync_success_regen(self):
        rs = self.reposync.RepoSync("Label", RTYPE)

        rs.urls = [{"source_url": "bogus-url", "metadata_signed": "N"}]

        rs = self._mock_sync(rs)
        rs.regen = True
        rs.sync()

        # don't test everything we already tested in sync_success_no_regen, just
        # see if the operation was successful
        self.assertEqual(rs.print_msg.call_args, (("Sync complete",), {}))

        self.assertEqual(self.reposync.taskomatic.add_to_repodata_queue_for_channel_package_subscription.call_args, ((["Label"], [], "server.app.yumreposync"), {}))
        self.assertEqual(self.reposync.taskomatic.add_to_erratacache_queue.call_args,
                         (("Label", ), {}))

    def test_sync_raises_channel_timeout(self):
        rs = self._create_mocked_reposync()

        exception = self.reposync.ChannelTimeoutException("anony-error")
        rs.repo_plugin = Mock(side_effect=exception)
        rs.sendErrorMail = Mock()

        self.assertRaises(SystemExit, rs.sync)
        self.assertEqual(rs.sendErrorMail.call_args,
                         (("anony-error", ), {}))
        self.assertEqual(rs.print_msg.call_args,
                         ((exception, ), {}))

    def test_sync_raises_unexpected_error(self):
        rs = self._create_mocked_reposync()

        rs.repo_plugin = Mock(side_effect=TypeError)
        rs.sendErrorMail = Mock()
        self.assertRaises(SystemExit, rs.sync)

        error_string = rs.print_msg.call_args[0][0]
        assert (error_string.startswith('Traceback') and
                'TypeError' in error_string), (
            "The error string does not contain the keywords "
            "'Traceback' and 'TypeError':\n %s\n---end of assert" % error_string)
        
    def test_update_bugs(self):
        notice = {'references': [{'type': 'bugzilla',
                                  'id': 'id1',
                                  'title': 'title1',
                                  'href': 'href1'},
                                 {'type': 'bugzilla',
                                  'id': 'id2',
                                  'title': 'title2',
                                  'href': 'href2'},
                                 {'type': 'bugzilla',
                                  'id': 'id2',
                                  'title': 'duplicate_id',
                                  'href': 'duplicate_id'},
                                 {'type': 'godzilla',
                                  'this': 'should be skipped'}]}
        bugs = self.reposync._update_bugs(notice)

        bug_values = [set(['id1', 'title1', 'href1']),
                      set(['id2', 'title2', 'href2'])]

        self.assertEqual(len(bugs), 2)
        for bug in bugs:
            self.assertEqual(bug.keys(), ['bug_id', 'href', 'summary'])
            assert set(bug.values()) in bug_values, (
                "Bug set(%s) not in %s" % (bug.values(), bug_values))

    def test_update_cves(self):
        notice = {'references': [{'type': 'cve',
                                  'id': 1},
                                 {'type': 'cve',
                                  'id': 2},
                                 {'type': 'cve',
                                  'id': 2},
                                 {'type': 'this should be skipped'}]}
        cves = self.reposync._update_cve(notice)

        self.assertEqual(cves, [1, 2])

    def test_update_keywords_reboot(self):
        notice = {'reboot_suggested': True,
                  'restart_suggested': False}

        keyword = self.reposync.Keyword()
        keyword.populate({'keyword': 'reboot_suggested'})
        self.assertEqual(self.reposync._update_keywords(notice),
                         [keyword])

    def test_update_keywords_restart(self):
        notice = {'reboot_suggested': False,
                  'restart_suggested': True}

        keyword = self.reposync.Keyword()
        keyword.populate({'keyword': 'restart_suggested'})
        self.assertEqual(self.reposync._update_keywords(notice),
                         [keyword])

    def test_update_keywords_restart_and_reboot(self):
        notice = {'reboot_suggested': True,
                  'restart_suggested': True}

        keyword_restart = self.reposync.Keyword()
        keyword_restart.populate({'keyword': 'restart_suggested'})
        keyword_reboot = self.reposync.Keyword()
        keyword_reboot.populate({'keyword': 'reboot_suggested'})
        self.assertEqual(self.reposync._update_keywords(notice),
                         [keyword_reboot, keyword_restart])

    def test_update_keywords_both_false(self):
        notice = {'reboot_suggested': False,
                  'restart_suggested': False}

        self.assertEqual(self.reposync._update_keywords(notice),
                         [])

    def test_send_error_mail(self):
        self.reposync.rhnMail.send = Mock()
        self.reposync.CFG.TRACEBACK_MAIL = 'recipient'
        self.reposync.HOSTNAME = 'testhost'
        rs = self._create_mocked_reposync()

        rs.sendErrorMail('email body')

        self.assertEqual(self.reposync.rhnMail.send.call_args, (
                ({'To': 'recipient',
                  'From': 'testhost <recipient>',
                  'Subject': "SUSE Manager repository sync failed (testhost)"},
                 "Syncing Channel 'Label' failed:\n\nemail body"), {}))

    def test_updates_process_packages_simple(self):
        rs = self._create_mocked_reposync()

        rs.channel = {'org_id': None}
        packages = [{'name': 'n1',
                     'version': 'v1',
                     'release': 'r1',
                     'arch': 'a1',
                     'channel_label': 'l1',
                     'epoch': []},
                    {'name': 'n2',
                     'version': 'v2',
                     'release': 'r2',
                     'arch': 'a2',
                     'channel_label': 'l2',
                     'epoch': 'e2'}]
        checksum = {'epoch': None,
                    'checksum_type': None,
                    'checksum': None,
                    'id': None}
        
        _mock_rhnsql(self.reposync, checksum)
        processed = rs._updates_process_packages(packages, 'a name')
        for p in processed:
            self.assertTrue(isinstance(p, self.reposync.IncompletePackage))

    def test_updates_process_packages_returns_the_right_values(self):
        rs = self._create_mocked_reposync()
        rs.channel = {'org_id': 'org'}
        packages = [{'name': 'n1',
                     'version': 'v1',
                     'release': 'r1',
                     'arch': 'a1',
                     'channel_label': 'l1',
                     'epoch': []},
                    {'name': 'n2',
                     'version': 'v2',
                     'release': 'r2',
                     'arch': 'a2',
                     'channel_label': 'l2',
                     'epoch': 'e2'}]

        checksum = {'epoch': 'cs_epoch',
                    'checksum_type': 'md5',
                    'checksum': '12345',
                    'id': 'cs_package_id'}

        _mock_rhnsql(self.reposync, checksum)
        processed = rs._updates_process_packages(packages, 'patchy')

        p1 = self.reposync.IncompletePackage()
        p1.populate({'package_size': None,
                     'channel_label': 'l1',
                     'name': 'n1',
                     'checksum_list': None,
                     'md5sum': None,
                     'org_id': 'org',
                     'epoch': 'cs_epoch',
                     'channels': None,
                     'package_id': 'cs_package_id',
                     'last_modified': None,
                     'version': 'v1',
                     'checksum_type': 'md5',
                     'release': 'r1',
                     'checksums': {'md5': '12345'},
                     'checksum': '12345',
                     'arch': 'a1'})
        p2 = self.reposync.IncompletePackage()
        p2.populate({'package_size': None,
                     'channel_label': 'l2',
                     'name': 'n2',
                     'checksum_list': None,
                     'md5sum': None,
                     'org_id': 'org',
                     'epoch': 'cs_epoch',
                     'channels': None,
                     'package_id': 'cs_package_id',
                     'last_modified': None,
                     'version': 'v2',
                     'checksum_type': 'md5',
                     'release': 'r2',
                     'checksums': {'md5': '12345'},
                     'checksum': '12345',
                     'arch': 'a2'})
        fixtures = [p1, p2]
        for pkg, fix in zip(processed, fixtures):
            self.assertEqual(pkg, fix)
        
    def test_updates_process_packages_checksum_not_found(self):
        rs = self._create_mocked_reposync()

        rs.channel = {'org_id': None}
        packages = [{'name': 'n2',
                     'version': 'v2',
                     'release': 'r2',
                     'arch': 'a2',
                     'channel_label': 'l2',
                     'epoch': 'e2'}]

        _mock_rhnsql(self.reposync, [])
        self.assertEqual(rs._updates_process_packages(packages, 'patchy'),
                         [])
        self.assertEqual(rs.print_msg.call_args,
                         (("No checksum found for n2-e2:v2-r2.a2. "
                           "Skipping Patch patchy", ),))

    def test_updates_process_packages_checksum_not_found_no_epoch(self):
        rs = self._create_mocked_reposync()

        rs.channel = {'org_id': None}
        packages = [{'name': 'n1',
                     'version': 'v1',
                     'release': 'r1',
                     'arch': 'a1',
                     'channel_label': 'l1',
                     'epoch': []}]

        _mock_rhnsql(self.reposync, [])
        self.assertEqual(rs._updates_process_packages(packages, 'patchy'),
                         [])
        self.assertEqual(rs.print_msg.call_args,
                         (("No checksum found for n1:v1-r1.a1. "
                           "Skipping Patch patchy", ),))

    def test_upload_updates_referenced_package_not_found(self):
        timestamp1 = datetime.now().isoformat(' ')
        notices = [{'from': 'from1',
                    'update_id': 'update_id1',
                    'version': 'version1',
                    'type': 'security',
                    'release': 'release1',
                    'description': 'description1',
                    'title': 'title1',
                    'issued': timestamp1, # we mock _to_db_date anyway
                    'updated': timestamp1,
                    'pkglist': [{'packages': []}],
                    'reboot_suggested': False
                    }]
        self.reposync._to_db_date = Mock(return_value=timestamp1)

        # no packages related to this errata makes the ErrataImport be called
        # with an empty list
        self.reposync.RepoSync._updates_process_packages = Mock(return_value=[])
        self.reposync.RepoSync.get_errata = Mock(return_value=None)

        mocked_backend = Mock()
        self.reposync.SQLBackend = Mock(return_value=mocked_backend)
        self.reposync.ErrataImport = Mock()
        rs = self._create_mocked_reposync()
        rs.channel = {'org_id': 'org',
                      'arch': 'arch'}

        rs.upload_updates(notices)

        self.assertEqual(self.reposync.ErrataImport.call_args,
                         (([], mocked_backend), {}))
        
    def test_associate_package(self):
        pack = self.reposync.ContentPackage()
        pack.setNVREA('name1', 'version1', 'release1', 'epoch1', 'arch1')
        pack.unique_id = 1
        pack.checksum = 'checksum1'
        pack.checksums[1] = 'checksum1'
        pack.checksum_type = 'c_type1'

        mocked_backend = Mock()
        self.reposync.SQLBackend = Mock(return_value=mocked_backend)
        rs = self._create_mocked_reposync()
        rs._importer_run = Mock()
        rs.channel_label = 'Label1'
        rs.channel = {'id': 'channel1', 'org_id': 'org1'}

        package = {'name': 'name1',
                   'version': 'version1',
                   'release': 'release1',
                   'epoch': 'epoch1',
                   'arch': 'arch1',
                   'checksum': 'checksum1',
                   'checksum_type': 'c_type1',
                   'org_id': 'org1',
                   'channels': [{'label': 'Label1', 'id': 'channel1'}]}

        rs.associate_package(pack)
        self.assertEqual(rs._importer_run.call_args,
                         ((package, 'server.app.yumreposync', mocked_backend),
                          {}))
    def test_best_checksum_item_unknown(self):
        checksums = {'no good checksum': None}

        self.assertEqual(self.reposync._best_checksum_item(checksums),
                         ('md5', None, None))

    def test_best_checksum_item_md5(self):
        checksums = {'md5': '12345'}
        self.assertEqual(self.reposync._best_checksum_item(checksums),
                         ('md5', 'md5', '12345'))

    def test_best_checksum_item_sha1(self):
        checksums = {'sha1': '12345'}
        self.assertEqual(self.reposync._best_checksum_item(checksums),
                         ('sha1', 'sha1', '12345'))

    def test_best_checksum_item_sha(self):
        checksums = {'sha': '12345'}
        self.assertEqual(self.reposync._best_checksum_item(checksums),
                         ('sha1', 'sha', '12345'))

    def test_best_checksum_item_sha256(self):
        checksums = {'sha256': '12345'}
        self.assertEqual(self.reposync._best_checksum_item(checksums),
                         ('sha256', 'sha256', '12345'))

    def test_best_checksum_item_all(self):
        checksums = {'sha1': 'xxx',
                     'sha': 'xxx',
                     'md5': 'xxx',
                     'sha256': '12345'}
        self.assertEqual(self.reposync._best_checksum_item(checksums),
                         ('sha256', 'sha256', '12345'))

    def test_import_packages_2download(self):
        p1 = self.reposync.ContentPackage()
        p1.setNVREA('name1', 'version1', 'release1', 'epoch1', 'arch1')
        p2 = self.reposync.ContentPackage()
        p2.setNVREA('name2', 'version2', 'release2', 'epoch2', 'arch2')

        # mock reposync methods
        self.reposync.suseLib = Mock()

        # this is how we mock getURL()
        url = Mock()
        url.getURL = Mock(return_value='http://some.url')
        self.reposync.suseLib.URL = Mock(return_value=url)

        self.reposync.rhnPackage.get_path_for_package = Mock(return_value=True)

        # all packages have already been downloaded
        self.reposync.os.path.exists = Mock(return_value = True)

        # mock RepoSync object methods (we can't use the usual
        # _mock_rhnsql method because that would mock the
        # import_packages method)
        rs = self.reposync.RepoSync("Label", RTYPE)
        rs.urls = [{"source_url": "bogus-url", "metadata_signed": "N"}]
        rs.compatiblePackageArchs = Mock(return_value=['arch1', 'arch2'])
        rs.print_msg = Mock()
        rs._download_packages = Mock()
        rs._link_packages = Mock()

        repo = Mock()
        repo.list_packages = Mock(return_value=[p1, p2])

        # run the method we're testing
        rs.import_packages(repo, "bogus-url")

        self.assertEqual(rs.print_msg.call_args_list,
                         [(("Repo http://some.url has 2 packages.",), {}),
                          (("No new packages to download.", ), {})])
        self.assertEqual(rs._link_packages.call_args,
                         (([], ), {}))
        self.assertEqual(rs._download_packages.call_args,
                         (([], 'bogus-url'), {}))

    def test_import_packages_2link(self):
        p1 = self.reposync.ContentPackage()
        p1.setNVREA('name1', 'version1', 'release1', 'epoch1', 'arch1')
        p2 = self.reposync.ContentPackage()
        p2.setNVREA('name2', 'version2', 'release2', 'epoch2', 'arch2')

        # mock reposync methods
        self.reposync.suseLib = Mock()

        # this is how we mock getURL()
        url = Mock()
        url.getURL = Mock(return_value='http://some.url')
        self.reposync.suseLib.URL = Mock(return_value=url)

        self.reposync.rhnPackage.get_path_for_package = Mock(return_value=True)

        # all packages have already been downloaded
        self.reposync.os.path.exists = Mock(return_value=False)

        # mock RepoSync object methods (we can't use the usual
        # _mock_rhnsql method because that would mock the
        # import_packages method)
        rs = self.reposync.RepoSync("Label", RTYPE)
        rs.urls = [{"source_url": "bogus-url", "metadata_signed": "N"}]
        rs.compatiblePackageArchs = Mock(return_value=['arch1', 'arch2'])
        rs.print_msg = Mock()
        rs._download_packages = Mock()
        rs._link_packages = Mock()

        repo = Mock()
        repo.list_packages = Mock(return_value=[p1, p2])

        # run the method we're testing
        rs.import_packages(repo, "bogus-url")

        self.assertEqual(rs.print_msg.call_args_list,
                         [(("Repo http://some.url has 2 packages.",), {})])
        self.assertEqual(rs._link_packages.call_args,
                         (([], ), {}))
        self.assertEqual(rs._download_packages.call_args,
                         (([p1, p2], 'bogus-url'), {}))
        
    def test_import_packages_2link_differently_and_download(self):
        p1 = self.reposync.ContentPackage()
        p1.setNVREA('name1', 'version1', 'release1', 'epoch1', 'arch1')
        p1.checksums = {'t1': 'c1'}
        p2 = self.reposync.ContentPackage()
        p2.setNVREA('name2', 'version2', 'release2', 'epoch2', 'arch2')

        # mock reposync methods
        self.reposync.suseLib = Mock()

        # this is how we mock getURL()
        url = Mock()
        url.getURL = Mock(return_value='http://some.url')
        self.reposync.suseLib.URL = Mock(return_value=url)

        self.reposync.rhnPackage.get_path_for_package = Mock(return_value=False)
        
        # all packages have already been downloaded
        self.reposync.rhnPackage.get_path_for_checksum = Mock(return_value=True)
        self.reposync.os.path.exists = Mock(return_value=True)

        # mock RepoSync object methods (we can't use the usual
        # _mock_rhnsql method because that would mock the
        # import_packages method)
        rs = self.reposync.RepoSync("Label", RTYPE)
        rs.channel = {'org_id': 'org'}
        rs.urls = [{"source_url": "bogus-url", "metadata_signed": "N"}]
        rs.compatiblePackageArchs = Mock(return_value=['arch1', 'arch2'])
        rs.print_msg = Mock()
        rs._download_packages = Mock()
        rs._link_packages = Mock()

        repo = Mock()
        repo.list_packages = Mock(return_value=[p1, p2])

        # run the method we're testing
        rs.import_packages(repo, "bogus-url")

        self.assertEqual(rs.print_msg.call_args_list,
                         [(("Repo http://some.url has 2 packages.",), {})])
        self.assertEqual(rs._link_packages.call_args,
                         (([p1, p2], ), {}))
        self.assertEqual(rs._download_packages.call_args,
                         (([p2], 'bogus-url'), {}))

    def test_import_packages_2link_differently_no_download(self):
        p1 = self.reposync.ContentPackage()
        p1.setNVREA('name1', 'version1', 'release1', 'epoch1', 'arch1')
        p2 = self.reposync.ContentPackage()
        p2.setNVREA('name2', 'version2', 'release2', 'epoch2', 'arch2')

        # mock reposync methods
        self.reposync.suseLib = Mock()

        # this is how we mock getURL()
        url = Mock()
        url.getURL = Mock(return_value='http://some.url')
        self.reposync.suseLib.URL = Mock(return_value=url)

        self.reposync.rhnPackage.get_path_for_package = Mock(return_value=False)

        # all packages have already been downloaded
        self.reposync.rhnPackage.get_path_for_checksum = Mock(return_value=True)
        self.reposync.os.path.exists = Mock(return_value=False)

        # mock RepoSync object methods (we can't use the usual
        # _mock_rhnsql method because that would mock the
        # import_packages method)
        rs = self.reposync.RepoSync("Label", RTYPE)
        rs.urls = [{"source_url": "bogus-url", "metadata_signed": "N"}]
        rs.compatiblePackageArchs = Mock(return_value=['arch1', 'arch2'])
        rs.print_msg = Mock()

        repo = Mock()
        repo.list_packages = Mock(return_value=[p1, p2])
        rs._download_packages = Mock()
        rs._link_packages = Mock()

        # run the method we're testing
        rs.import_packages(repo, "bogus-url")

        self.assertEqual(rs.print_msg.call_args_list,
                         [(("Repo http://some.url has 2 packages.",), {})])
        self.assertEqual(rs._link_packages.call_args,
                         (([p1, p2], ), {}))
        self.assertEqual(rs._download_packages.call_args,
                         (([p1, p2], 'bogus-url'), {}))

    def test_import_packages_2_skipped_bad_arches(self):
        p1 = self.reposync.ContentPackage()
        p1.setNVREA('name1', 'version1', 'release1', 'epoch1', 'src')
        p1.checksums = {'t1': 'c1'}
        p2 = self.reposync.ContentPackage()
        p2.setNVREA('name2', 'version2', 'release2', 'epoch2', 'weird_arch')

        # mock reposync methods
        self.reposync.suseLib = Mock()

        # this is how we mock getURL()
        url = Mock()
        url.getURL = Mock(return_value='http://some.url')
        self.reposync.suseLib.URL = Mock(return_value=url)

        # mock RepoSync object methods (we can't use the usual
        # _mock_rhnsql method because that would mock the
        # import_packages method)
        rs = self.reposync.RepoSync("Label", RTYPE)
        rs.channel = {'org_id': 'org'}
        rs.urls = [{"source_url": "bogus-url", "metadata_signed": "N"}]
        rs.compatiblePackageArchs = Mock(return_value=['arch1', 'arch2'])
        rs.print_msg = Mock()
        rs._download_packages = Mock()
        rs._link_packages = Mock()

        repo = Mock()
        repo.list_packages = Mock(return_value=[p1, p2])

        # run the method we're testing
        rs.import_packages(repo, "bogus-url")

        self.assertEqual(rs.print_msg.call_args_list,
                         [(("Repo http://some.url has 2 packages.",), {}),
                          (("Skip '2' incompatible packages.", ), {}),
                          (("No new packages to download.", ), {})])
        self.assertEqual(rs._link_packages.call_args,
                         (([], ), {}))
        self.assertEqual(rs._download_packages.call_args,
                         (([], 'bogus-url'), {}))

    def test_link_packages(self):
        p1 = self.reposync.ContentPackage()
        p1.checksums = {'md5': '12345'}
        p2 = self.reposync.ContentPackage()
        p2.checksums =  {'md5': 'asdfg'}
        
        rs = self._create_mocked_reposync()
        rs.associate_package = Mock()
        rs.error_msg = Mock()

        rs._link_packages([p1, p2])

        self.assertFalse(rs.error_msg.called)
        self.assertEqual(rs.associate_package.call_args_list,
                         [((p1, ), {}), ((p2, ), {})])

    def test_link_packages_logs_error_but_doesnt_die(self):
        p1 = self.reposync.ContentPackage()
        p1.checksums = {'md5': '12345'}

        rs = self._create_mocked_reposync()
        exc = Exception('error')
        rs.associate_package = Mock(side_effect=exc) # make it raise an Exception
        rs.error_msg = Mock()

        rs._link_packages([p1])

        self.assertTrue(rs.error_msg.called)
        self.assertEqual(rs.error_msg.call_args,
                         ((exc, ), {}))
        self.assertEqual(rs.associate_package.call_args,
                         ((p1, ), {}))

    def test_link_packages_logs_error_and_dies(self):
        p1 = self.reposync.ContentPackage()
        p1.checksums = {'md5': '12345'}

        rs = self._create_mocked_reposync()
        exc = Exception('error')
        rs.associate_package = Mock(side_effect=exc) # make it raise an Exception
        rs.fail = True # make it die on the above Exception
        rs.error_msg = Mock()

        self.assertRaises(Exception, rs._link_packages, [p1])

        self.assertTrue(rs.error_msg.called)
        self.assertEqual(rs.error_msg.call_args,
                         ((exc, ), {}))
        self.assertEqual(rs.associate_package.call_args,
                         ((p1, ), {}))

    def test_download_packages(self):
        p1 = self.reposync.ContentPackage()
        p1.setNVREA('name1', 'version1', 'release1', 'epoch1', 'arch1')
        p2 = self.reposync.ContentPackage()
        p2.setNVREA('name2', 'version2', 'release2', 'epoch2', 'arch2')

        rs = self._create_mocked_reposync()
        rs.upload_package = Mock()
        self.reposync.os.remove = Mock()
        repo = Mock()
        repo.get_package = Mock(return_value='pkg_path')

        rs._download_packages([p1, p2], repo, "file://local_repo")

        self.assertEqual(rs.upload_package.call_args_list,
                         [((p1, 'pkg_path'), {}), ((p2, 'pkg_path'), {})])
        self.assertFalse(self.reposync.os.remove.called)

    def test_download_packages_non_local(self):
        p1 = self.reposync.ContentPackage()
        p1.setNVREA('name1', 'version1', 'release1', 'epoch1', 'arch1')
        p2 = self.reposync.ContentPackage()
        p2.setNVREA('name2', 'version2', 'release2', 'epoch2', 'arch2')

        rs = self._create_mocked_reposync()
        rs.upload_package = Mock()
        self.reposync.os.remove = Mock()
        repo = Mock()
        repo.get_package = Mock(return_value='pkg_path')

        rs._download_packages([p1, p2], repo, "http://remote_repo") # non-local

        self.assertEqual(rs.upload_package.call_args_list,
                         [((p1, 'pkg_path'), {}), ((p2, 'pkg_path'), {})])
        self.assertEqual(self.reposync.os.remove.call_args,
                         (('pkg_path', ), {}))

    def test_download_packages_errors_and_dies(self):
        p1 = self.reposync.ContentPackage()
        p1.setNVREA('name1', 'version1', 'release1', 'epoch1', 'arch1')
        p2 = self.reposync.ContentPackage()
        p2.setNVREA('name2', 'version2', 'release2', 'epoch2', 'arch2')

        rs = self._create_mocked_reposync()
        rs.fail = True # make it die
        exc = Exception('error')
        rs.upload_package = Mock(side_effect=exc) # make it raise an exception
        rs.error_msg = Mock()
        repo = Mock()
        repo.get_package = Mock(return_value='pkg_path')

        self.assertRaises(Exception, rs._download_packages,
                          [p1, p2], repo, "file://remote_repo")

        self.assertEqual(rs.upload_package.call_args,
                         ((p1, 'pkg_path'), {}))
        self.assertEqual(rs.error_msg.call_args_list,
                         [((exc, ), {})])

    def test_download_packages_errors_and_continues(self):
        p1 = self.reposync.ContentPackage()
        p1.setNVREA('name1', 'version1', 'release1', 'epoch1', 'arch1')
        p2 = self.reposync.ContentPackage()
        p2.setNVREA('name2', 'version2', 'release2', 'epoch2', 'arch2')

        rs = self._create_mocked_reposync()
        exc = Exception('error')
        rs.upload_package = Mock(side_effect=exc) # make it raise an exception
        rs.error_msg = Mock()
        repo = Mock()
        repo.get_package = Mock(return_value='pkg_path')

        rs._download_packages([p1, p2], repo, "file://remote_repo")
        self.assertEqual(rs.upload_package.call_args_list,
                         [((p1, 'pkg_path'), {}), ((p2, 'pkg_path'), {})])
        self.assertEqual(rs.error_msg.call_args_list,
                         [((exc, ), {}), ((exc, ), {})])
        
    def _create_mocked_reposync(self):
        rs = self.reposync.RepoSync("Label", RTYPE)
        rs.urls = [{"source_url": "bogus-url", "metadata_signed": "N"}]
        rs = self._mock_sync(rs)

        return rs

    def _mock_sync(self, rs):
        """Mock a lot of the methods that are called during sync()

        erratum = reposync.Erratum()
        erratum.populate({'advisory_name': 'update_id1-version1-arch',
                          'advisory': 'update_id1-version1-arch',
                          'product': 'release1',
                          'description': 'description1',
                          'errata_from': 'from1',
                          'locally_modified': None,
                          'refers_to': '',
                          'solution': ' ',
                          'topic': ' ',
                          'last_modified': None,
                          'keywords': [],
                          'packages': [True],
                          'files': [],
                          'advisory_type': 'Security Advisory',
                          'issue_date': timestamp1,
                          'notes': '',
                          'org_id': 'org',
                          'bugs': [],
                          'advisory_rel': 'version1',
                          'synopsis': 'title1',
                          'cve': [],
                          'update_date': timestamp2,
                          'channels': [{'label': 'Label'}]})
        self.assertEqual(reposync.ErrataImport.call_args,
                         (([erratum], mocked_backend), {}))
        :rs: RepoSync object on which we're going to call sync() later

        """
        rs.import_packages = Mock()
        rs.import_updates = Mock()
        self.reposync.taskomatic.add_to_repodata_queue_for_channel_package_subscription = Mock()
        self.reposync.taskomatic.add_to_erratacache_queue = Mock()
        rs.print_msg = Mock()

        rs.mocked_plugin = Mock()
        rs.repo_plugin = Mock(return_value=rs.mocked_plugin)

        rs.update_date = Mock()
        self.reposync.initCFG = Mock()
        self.reposync.CFG.HTTP_PROXY = rs.mocked_proxy = Mock()
        self.reposync.CFG.HTTP_PROXY_USERNAME = rs.mocked_proxy_user = Mock()
        self.reposync.CFG.HTTP_PROXY_PASSWORD = rs.mocked_proxy_pass = Mock()
        return rs

def test_channel_exceptions():
    """Test rasising all the different exceptions when syncing"""
    # the only way to write a test generator with nose is if we put it
    # outside the class, so we have to repeat all the Mocks
    repoSync = spacewalk.satellite_tools.reposync
    repoSync.rhnLog.initLOG = Mock()
    repoSync.CFG = repoSync.initCFG = Mock()
    backup_os = repoSync.os
    repoSync.os = Mock()
    rs = repoSync.RepoSync("Label", RTYPE)
    rs.urls = [{"source_url": "bogus-url", "metadata_signed": "N"}]
    rs.import_packages = Mock()
    rs.import_updates = Mock()
    rs.print_msg = Mock()
    rs.mocked_plugin = Mock()
    rs.repo_plugin = Mock(return_value=rs.mocked_plugin)
    rs.update_date = Mock()
    rs.sendErrorMail = Mock()
    repoSync.os = backup_os

    for exc_class, exc_name in [
        (repoSync.ChannelException, "ChannelException"),
        (repoSync.Errors.YumGPGCheckError, "YumGPGCheckError"),
        (repoSync.Errors.RepoError, "RepoError"),
        (repoSync.Errors.RepoMDError, "RepoMDError")]:
        yield check_channel_exceptions, rs, exc_class, exc_name

def check_channel_exceptions(rs, exc_class, exc_name):
    # since this isn't a subclass of unittest.TestCase we can't use
    # unittest's assertions
    from nose.tools import assert_raises, assert_equal
    rs.repo_plugin = Mock(side_effect=exc_class("error msg"))

    assert_raises(SystemExit, rs.sync)
    assert_equal(rs.sendErrorMail.call_args,
                 (("%s: %s" % (exc_name, "error msg"), ), {}))
    assert_equal(rs.print_msg.call_args,
                 (("%s: %s" % (exc_name, "error msg"), ), {}))

        
def _mock_rhnsql(module, return_value):
    """Method to mock the rhnSQL to return something for us

    :module: the module where rhnSQL is called from
    :return_value: the value or object that rhnSQL's fetches should return

    rhnSQL's calls are a often a bit more complex. It usually goes
    like this: first an sql statement is prepared, then it is
    executed and then the result is fetched. We need to mock all
    that.

    Here's an example usage:

    query = rhnSQL.prepare('some sql statement')
    query.execute()
    result = query.fetchall_dict()

    """
    # we're making prepare() return an object with methods that
    # return our desired return value
    query = Mock()
    returned_obj = Mock(return_value=return_value)
    query.fetchall_dict = query.fetchone_dict = returned_obj

    module.rhnSQL.prepare = Mock(return_value=query)
