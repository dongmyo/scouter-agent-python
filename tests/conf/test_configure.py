import unittest

import javaproperties
import io

from scouterx.conf.configure import Configure


class TestProperties:
    @staticmethod
    def test_config_load():
        conf = Configure()
        print(conf.net_collector_ip)

    @staticmethod
    def test_properties():
        s = '''
a=1
b=2=3
c=4
empty=
e=hollo,:ok=312/323/<pp>
empty_no=
b1=true
b2=false
b3=
'''
        p = javaproperties.load(io.StringIO(s))

        print(int(p.get('a')))
        print(p.get('b'))
        print(int(p.get('c')))

        str_empty = p.get('empty', 'default')
        print('strEmpty=' + str_empty)
        str_no_key = p.get('nokey', 'default')
        print('strNoKey=' + str_no_key)
        print(p.get('e', 'default'))

        empty_no = p.get('empty_no', '10')
        if empty_no == '':
            empty_no = '10'

        print(int(empty_no))

        # Boolean properties
        print(p.get('b1', 'false').lower() == 'true')
        print(p.get('b2', 'true').lower() == 'true')
        print(p.get('b3', 'true').lower() == 'true')


if __name__ == '__main__':
    unittest.main()
