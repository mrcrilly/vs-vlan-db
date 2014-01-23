from vsvlandb.models import VLAN,Subnet,Site
from vsvlandb import dbo
site = Site('A9')
subnet = Subnet('10.8.1.0', '255.255.255.0', site)
vlan = VLAN('1024', subnet, site)
dbo.session.add(site)
dbo.session.add(subnet)
dbo.session.add(vlan)
dbo.session.commit()
