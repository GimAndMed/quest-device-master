import Pyro.naming, Pyro.core
from Pyro.errors import NamingError

# locate the NS
locator = Pyro.naming.NameServerLocator()
print('Searching Name Server...'),
ns = locator.getNS()

# resolve the Pyro object
print('finding object')
try:
        URI=ns.resolve('DEVICE_MASTER')
        print 'URI:',URI
except NamingError,x:
        print 'Couldn\'t find object, nameserver says:',x
        raise SystemExit

# create a proxy for the Pyro object, and return that
test = Pyro.core.getProxyForURI(URI)

CB_SLAVE_1="CB_SLAVE_1"

from time import sleep
while True:
    print("Client say")
    # test.getButtons(CB_SLAVE_1).printResource()
    # test.setButtons(CB_SLAVE_1, [1]*18)
    # sleep(5)
    # test.setButtons(CB_SLAVE_1, [0]*18)
    buttons = test.getButtons(CB_SLAVE_1,"value")
    print(buttons)
    sleep(5)

