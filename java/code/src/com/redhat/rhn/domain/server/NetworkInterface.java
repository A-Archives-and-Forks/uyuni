/**
 * Copyright (c) 2009--2010 Red Hat, Inc.
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
package com.redhat.rhn.domain.server;

import com.redhat.rhn.common.hibernate.HibernateFactory;
import com.redhat.rhn.domain.BaseDomainHelper;
import com.redhat.rhn.manager.kickstart.IpAddress;

import org.apache.commons.lang.StringUtils;
import org.apache.commons.lang.builder.EqualsBuilder;
import org.apache.commons.lang.builder.HashCodeBuilder;

import org.hibernate.Session;

import java.io.Serializable;
import java.util.ArrayList;

/**
 * NetworkInterface
 * @version $Rev$
 */
public class NetworkInterface extends BaseDomainHelper implements
    Serializable {

    private Long interfaceId;
    private Server server;
    private String name;
    private String hwaddr;
    private String module;
    private ServerNetAddress4 sa4 = null;
    private ArrayList<ServerNetAddress6> sa6 = null;

    /**
     * @return Returns the interfaceid.
     */
    public Long getInterfaceId() {
        return interfaceId;
    }

    /**
     * @param id The interfaceId to set.
     */
    public void setInterfaceId(Long id) {
        this.interfaceId = id;
    }

    /**
     * @return Returns the hwaddr.
     */
    public String getHwaddr() {
        return hwaddr;
    }

    /**
     * @param h The hwaddr to set.
     */
    public void setHwaddr(String h) {
        this.hwaddr = h;
    }

    /**
     * @return Returns the module.
     */
    public String getModule() {
        return module;
    }

    /**
     * @param m The module to set.
     */
    public void setModule(String m) {
        this.module = m;
    }

    /**
     * @return Returns the name.
     */
    public String getName() {
        return name;
    }

    /**
     * @param n The name to set.
     */
    public void setName(String n) {
        this.name = n;
    }

    /**
     * @return Returns the server.
     */
    public Server getServer() {
        return server;
    }

    /**
     * @param s The server to set.
     */
    public void setServer(Server s) {
        this.server = s;
    }

    /**
     * {@inheritDoc}
     */
    public boolean equals(final Object other) {
        if (!(other instanceof NetworkInterface)) {
            return false;
        }
        NetworkInterface castOther = (NetworkInterface) other;
        return new EqualsBuilder().append(this.getServer(), castOther.getServer())
                                  .append(this.getName(), castOther.getName())
                                  .append(this.getHwaddr(), castOther.getHwaddr())
                                  .append(this.getModule(), castOther.getModule())
                                  .isEquals();
    }

    /**
     * {@inheritDoc}
     */
    public int hashCode() {
        return new HashCodeBuilder().append(this.getServer())
                                    .append(this.getName())
                                    .append(this.getHwaddr())
                                    .append(this.getModule())
                                    .toHashCode();
    }

    /**
     * {@inheritDoc}
     */
    public String toString() {
        return "NetworkInterface - name: " + this.getName();
    }


    /**
     * findServerNetAddress4
     * @param id Id of the network interface to search on.
     */
    private void findServerNetAddress4(Long id) {
        if (sa4 != null) {
            return;
        }

        Session session = HibernateFactory.getSession();
        sa4 = (ServerNetAddress4) session.getNamedQuery("ServerNetAddress4.lookup")
                                         .setParameter("interface_id", this.interfaceId)
                                         .uniqueResult();
    }

    /**
     * @return Returns the IP address (IPv4 compatibility).
     */
    public String getIpaddr() {
        findServerNetAddress4(this.getInterfaceId());

        if (sa4 == null) {
            return null;
        }

        return sa4.getAddress();
    }

    /**
     * @return Returns the netmask (IPv4 compatibility).
     */
    public String getNetmask() {
        findServerNetAddress4(this.getInterfaceId());

        if (sa4 == null) {
            return null;
        }

        return sa4.getNetmask();
   }

    /**
     * @return Returns the broadcast (IPv4 compatibility).
     */
    public String getBroadcast() {
        findServerNetAddress4(this.getInterfaceId());

        if (sa4 == null) {
            return null;
        }

        return sa4.getBroadcast();
    }

    /**
     * findServerNetAddress6ByScope
     * @param scope Address scope to search for.
     * @return Returns IPv6 address of the given scope for the given interface.
     */
    private String findServerNetAddress6ByScope(String scope) {
        Session session = HibernateFactory.getSession();
        ServerNetAddress6 ad6 = (ServerNetAddress6)
            session.getNamedQuery("ServerNetAddress6.lookup_by_scope_and_id")
            .setParameter("interface_id", this.interfaceId)
            .setParameter("scope", scope)
            .uniqueResult();

        if (ad6 == null) {
            return null;
        }
        else {
            return ad6.getAddress();
        }
    }

    /**
     * @return If available, returns a global IPv6 address.
     */
    public String getIp6Addr() {
        return findServerNetAddress6ByScope("universe");
    }

    /**
     * returns true if the NetworkInterface is disabled
     * @return if it's empty or not
     */
    public boolean isDisabled() {
        return (this.getIpaddr() == null ||
                this.getIpaddr().equals("0") ||
                this.getIpaddr().equals("")) &&
               (this.getIp6Addr() == null ||
                this.getIp6Addr().equals("") ||
                this.getIp6Addr().equals("0"));
    }


    public boolean isIpValid() {
        try {
            IpAddress ip = new IpAddress(this.getIpaddr());
            return true;
        }
        catch (Exception e) {
            return false;
        }
    }

    public boolean isMacValid() {
        return !(StringUtils.isEmpty(this.getHwaddr()) ||
                this.getHwaddr().equals("00:00:00:00:00:00") ||
                this.getHwaddr().equals("fe:ff:ff:ff:ff:ff"));
    }

    /**
     * Returns if this network interface is valid and should be used
     * @return true if valid, else false
     */
    public boolean isValid() {
        return isIpValid() && isMacValid();
    }

    /**
     * true if the network card has a public ip address
     * and can thus useful in the cases of KSing
     * via ip address
     * @return true if the NIC has a public ip address.
     */
    public boolean isPublic() {
        return isValid() && !(getIpaddr().equals("127.0.0.1") ||
                                        getIpaddr().equals("0.0.0.0"));
    }

    /**
     * Retrieve list of IPv6 addresses
     * @return List of ServerNetAddress6 objects
     */
    public ArrayList<ServerNetAddress6> getIPv6Addresses() {
        if (sa6 == null) {
            Session session = HibernateFactory.getSession();
            sa6 = (ArrayList<ServerNetAddress6>)
                session.getNamedQuery("ServerNetAddress6.lookup_by_id")
                .setParameter("interface_id", this.interfaceId).list();
        }

        return sa6;
    }

}
