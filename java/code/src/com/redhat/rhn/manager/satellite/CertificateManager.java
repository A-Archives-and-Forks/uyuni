/**
 * Copyright (c) 2009--2012 Red Hat, Inc.
 *
 * This software is licensed to you under the GNU General Public License,
 * version 2 (GPLv2). There is NO WARRANTY for this software, express or
 * implied, including the implied warranties of MERCHANTABILITY or FITNESS
 * FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
 * along with this software; if not, see
 * http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.
 *
 * Red Hat trademarks are not licensed under GPLv2. No permission is
 * granted to use or replicate Red Hat trademarks that are incorporated
 * in this software or its documentation.
 */
package com.redhat.rhn.manager.satellite;

import com.redhat.rhn.domain.satellite.CertificateFactory;
import com.redhat.rhn.domain.satellite.SatelliteCertificate;
import com.redhat.rhn.manager.BaseManager;

import java.util.Calendar;
import java.util.Date;

/**
 * SatelliteManager
 * @version $Rev$
 */
public class CertificateManager extends BaseManager {

    private static CertificateManager instance = new CertificateManager();

    public static final int GRACE_PERIOD_IN_DAYS = 7;
    public static final int RESTRICTED_PERIOD_IN_DAYS = 24;
    private static final long MILLISECONDS_IN_DAY =  86400000;

    // ALWAYS_VALID means no grace period either
    public static final boolean CERT_ALWAYS_VALID = true;

    /**
     * Default constructor
     */
    public CertificateManager() {

    }

    /**
     * Get the instance of the SatelliteManager
     * @return SatelliteManager instance
     */
    public static CertificateManager getInstance() {
        return instance;
    }

    /**
     * Return whether the satellite certificate has expired or not. True signifies
     * that the grace period is over and that we need to lock the satellite down
     * @return true if cert has expired, false otherwise
     */
    public boolean isSatelliteCertExpired() {
        Date now = Calendar.getInstance().getTime();
        boolean ret = false;
        if (!CERT_ALWAYS_VALID) {
            ret = now.after(getGracePeriodEndDate());
        }
        return ret;
    }

    /**
     * Return whether the satellite certificate is in a grace period or not.
     * False will be returned if the grace period is over or if it has not
     * begun.
     * @return true if in grace period, false otherwise
     */
    public boolean isSatelliteCertInGracePeriod() {
        Date now = Calendar.getInstance().getTime();
        boolean ret = false;
        if (!CERT_ALWAYS_VALID) {
            ret = now.after(getGracePeriodBeginDate()) &&
                    now.before(getGracePeriodEndDate());
        }
        return ret;
    }

    /**
     * Return whether the satellite certificate is in a restricted period or not.
     * False will be returned if the restricted period is over or if it has not
     * begun.
     * @return true if in restricted period, false otherwise
     */
    public boolean isSatelliteCertInRestrictedPeriod() {
        Date now = Calendar.getInstance().getTime();
        return now.after(getGracePeriodEndDate()) &&
               now.before(getRestrictedPeriodEndDate());
    }

    protected Date getGracePeriodBeginDate() {
        SatelliteCertificate sc = CertificateFactory.lookupNewestCertificate();
        Calendar cal = Calendar.getInstance();
        cal.setTime(sc.getExpires());
        cal.set(Calendar.HOUR, 0);
        cal.set(Calendar.MINUTE, 0);
        cal.set(Calendar.SECOND, 0);
        cal.set(Calendar.MILLISECOND, 0);
        cal.set(Calendar.AM_PM, Calendar.AM);
        return cal.getTime();
    }

    /**
     * @return Date that represent the end of the satellite's certificate's grace period
     */
    public Date getGracePeriodEndDate() {
        SatelliteCertificate sc = CertificateFactory.lookupNewestCertificate();
        Calendar cal = Calendar.getInstance();
        cal.setTime(sc.getExpires());
        cal.set(Calendar.HOUR, 0);
        cal.set(Calendar.MINUTE, 0);
        cal.set(Calendar.SECOND, 0);
        cal.set(Calendar.MILLISECOND, 0);
        cal.set(Calendar.AM_PM, Calendar.AM);
        cal.add(Calendar.DATE, GRACE_PERIOD_IN_DAYS);
        return cal.getTime();
    }

    /**
     * @return Date that represent the end of the satellite's certificate's
     * restricted period
     */
    public Date getRestrictedPeriodEndDate() {
        SatelliteCertificate sc = CertificateFactory.lookupNewestCertificate();
        Calendar cal = Calendar.getInstance();
        cal.setTime(sc.getExpires());
        cal.set(Calendar.HOUR, 0);
        cal.set(Calendar.MINUTE, 0);
        cal.set(Calendar.SECOND, 0);
        cal.set(Calendar.MILLISECOND, 0);
        cal.set(Calendar.AM_PM, Calendar.AM);
        cal.add(Calendar.DATE, GRACE_PERIOD_IN_DAYS);
        cal.add(Calendar.DATE, RESTRICTED_PERIOD_IN_DAYS);
        return cal.getTime();
    }

    /**
     * @return the number of the days left before the Sat certificate will expire.
     *                   (including the  grace period)
     *
     */
    public long getDaysLeftBeforeCertExpiration() {
        return getDaysLeftBefore(getGracePeriodEndDate().getTime());
    }

    private long getDaysLeftBefore(long endTime) {
        Calendar cal = Calendar.getInstance();
        cal.set(Calendar.HOUR, 0);
        cal.set(Calendar.MINUTE, 0);
        cal.set(Calendar.SECOND, 0);
        cal.set(Calendar.MILLISECOND, 0);
        cal.set(Calendar.AM_PM, Calendar.AM);
        return (endTime - cal.getTime().getTime()) / MILLISECONDS_IN_DAY;
    }

    /**
     * @return the number of the days left before the restricted period finishes
     */
    public String[] getDayProgressInRestrictedPeriod() {
        String[] progress = new String[2];
        progress[0] = new Long(RESTRICTED_PERIOD_IN_DAYS -
                getDaysLeftBefore(getRestrictedPeriodEndDate().getTime()) + 1).toString();
        progress[1] = new Long(RESTRICTED_PERIOD_IN_DAYS).toString();
        return progress;
    }
}
