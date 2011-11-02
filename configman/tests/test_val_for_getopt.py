import unittest
import getopt

import configman.config_manager as config_manager
from configman.config_exceptions import NotAnOptionError
from ..value_sources.for_getopt import ValueSource


class TestCase(unittest.TestCase):

    def test_for_getopt_basics(self):
        source = ['a', 'b', 'c']
        o = ValueSource(source)
        self.assertEqual(o.argv_source, source)

    def test_for_getopt_get_values(self):
        c = config_manager.ConfigurationManager(
          manager_controls=False,
          #use_config_files=False,
          use_auto_help=False,
          argv_source=[]
        )

        source = ['--limit', '10']
        o = ValueSource(source)
        self.assertEqual(o.get_values(c, True), {})
        self.assertRaises(NotAnOptionError,
                          o.get_values, c, False)

        c.option_definitions.add_option('limit', default=0)
        self.assertEqual(o.get_values(c, False), {'limit': '10'})
        self.assertEqual(o.get_values(c, True), {'limit': '10'})

    def test_for_getopt_with_ignore(self):
        function = ValueSource.getopt_with_ignore
        args = ['a', 'b', 'c']
        o, a = function(args, '', [])
        self.assertEqual(o, [])
        self.assertEqual(a, args)
        args = ['-a', '14', '--fred', 'sally', 'ethel', 'dwight']
        o, a = function(args, '', [])
        self.assertEqual([], o)
        self.assertEqual(a, args)
        args = ['-a', '14', '--fred', 'sally', 'ethel', 'dwight']
        o, a = function(args, 'a:', [])
        self.assertEqual(o, [('-a', '14')])
        self.assertEqual(a, ['--fred', 'sally', 'ethel', 'dwight'])
        args = ['-a', '14', '--fred', 'sally', 'ethel', 'dwight']
        o, a = function(args, 'a', ['fred='])
        self.assertEqual(o, [('-a', ''), ('--fred', 'sally')])
        self.assertEqual(a, ['14', 'ethel', 'dwight'])

    def test_overlay_config_5(self):
        """test namespace definition w/getopt"""
        n = config_manager.Namespace()
        n.add_option('a', 1, doc='the a')
        n.b = 17
        n.add_option('c', False, doc='the c')
        c = config_manager.ConfigurationManager([n], [['--a', '2', '--c']],
                                    manager_controls=False,
                                    use_auto_help=False,
                                    argv_source=[])
        self.assertEqual(c.option_definitions.a, n.a)
        self.assertTrue(isinstance(c.option_definitions.b,
                                   config_manager.Option))
        self.assertEqual(c.option_definitions.a.value, 2)
        self.assertEqual(c.option_definitions.b.value, 17)
        self.assertEqual(c.option_definitions.b.default, 17)
        self.assertEqual(c.option_definitions.b.name, 'b')
        self.assertEqual(c.option_definitions.c.name, 'c')
        self.assertEqual(c.option_definitions.c.value, True)

    def test_overlay_config_6(self):
        """test namespace definition w/getopt"""
        n = config_manager.Namespace()
        n.add_option('a', doc='the a', default=1)
        n.b = 17
        n.c = config_manager.Namespace()
        n.c.add_option('extra', doc='the x', default=3.14159, short_form='e')
        c = config_manager.ConfigurationManager([n],
                                                [['--a', '2', '--c.extra',
                                                  '11.0']],
                                                manager_controls=False,
                                                use_auto_help=False)
        self.assertEqual(c.option_definitions.a, n.a)
        self.assertEqual(type(c.option_definitions.b), config_manager.Option)
        self.assertEqual(c.option_definitions.a.value, 2)
        self.assertEqual(c.option_definitions.b.value, 17)
        self.assertEqual(c.option_definitions.b.default, 17)
        self.assertEqual(c.option_definitions.b.name, 'b')
        self.assertEqual(c.option_definitions.c.extra.name, 'extra')
        self.assertEqual(c.option_definitions.c.extra.doc, 'the x')
        self.assertEqual(c.option_definitions.c.extra.default, 3.14159)
        self.assertEqual(c.option_definitions.c.extra.value, 11.0)

    def test_overlay_config_6a(self):
        """test namespace w/getopt w/short form"""
        n = config_manager.Namespace()
        n.add_option('a', 1, doc='the a')
        n.b = 17
        n.c = config_manager.Namespace()
        n.c.add_option('extra', 3.14159, 'the x', short_form='e')
        c = config_manager.ConfigurationManager([n], [getopt],
                                    manager_controls=False,
                                    argv_source=['--a', '2', '-e', '11.0'],
                                    use_auto_help=False)
        self.assertEqual(c.option_definitions.a, n.a)
        self.assertEqual(type(c.option_definitions.b), config_manager.Option)
        self.assertEqual(c.option_definitions.a.value, 2)
        self.assertEqual(c.option_definitions.b.value, 17)
        self.assertEqual(c.option_definitions.b.default, 17)
        self.assertEqual(c.option_definitions.b.name, 'b')
        self.assertEqual(c.option_definitions.c.extra.name, 'extra')
        self.assertEqual(c.option_definitions.c.extra.doc, 'the x')
        self.assertEqual(c.option_definitions.c.extra.default, 3.14159)
        self.assertEqual(c.option_definitions.c.extra.value, 11.0)