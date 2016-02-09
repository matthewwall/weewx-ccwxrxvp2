# Copyright 2014 Chris Matteri
# Copyright 2015 Fergus Duncan
# Released under the MIT License (http://opensource.org/licenses/mit-license.php)

from setup import ExtensionInstaller

def loader():
    return MeteostickInstaller()

class MeteostickInstaller(ExtensionInstaller):
    def __init__(self):
        super(MeteostickInstaller, self).__init__(
            version="1.0mw",
            name='meteostick',
            description='Driver for the Smartbedded Meteostick',
            author="Fergus Duncan",
            author_email="fergus@ziplockk.com",
            config={
                'Station': {
                    'station_type': 'Meteostick'},
                'Meteostick': {
                    'poll_interval': '2.5',
                    'driver': 'user.meteostick'}},
            files=[('bin/user', ['bin/user/meteostick.py'])]
            )
