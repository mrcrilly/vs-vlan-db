from vsvlandb.models import VLAN,Subnet,Site
from vsvlandb import dbo

site_london = Site('London')
site_paris = Site('Paris')

subnet_1 = Subnet('10.8.0.0', '255.255.0.0', site_london.name)
subnet_2 = Subnet('10.8.0.0', '255.255.0.0', site_paris.name)
subnet_3 = Subnet('192.168.1.0', '255.255.255.0', site_london.name)

vlan_1 = VLAN('15', subnet_1, site_london)
vlan_2 = VLAN('99', subnet_2, site_london)
vlan_3 = VLAN('456', subnet_3, site_paris)

dbo.session.add(site_london)
dbo.session.add(site_paris)

dbo.session.add(subnet_1)
dbo.session.add(subnet_2)
dbo.session.add(subnet_3)

dbo.session.add(vlan_1)
dbo.session.add(vlan_2)
dbo.session.add(vlan_3)

dbo.session.commit()
