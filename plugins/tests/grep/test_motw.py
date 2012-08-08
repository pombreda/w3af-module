'''
test_motw.py

Copyright 2012 Andres Riancho

This file is part of w3af, w3af.sourceforge.net .

w3af is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

w3af is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with w3af; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
'''

from ..helper import PluginTest, PluginConfig
import core.data.constants.severity as severity


class TestMOTW(PluginTest):
    
    motw_url = 'https://moth/w3af/grep/motw/'
    
    _run_configs = {
        'cfg1': {
            'target': motw_url,
            'plugins': {
                'grep': (PluginConfig('motw'),),
                'discovery': (
                    PluginConfig('web_spider',
                                 ('onlyForward', True, PluginConfig.BOOL)),
                )         
                
            }
        }
    }
    
    def test_found_vuln(self):
        cfg = self._run_configs['cfg1']
        self._scan(cfg['target'], cfg['plugins'])
        infos = self.kb.getData('motw', 'motw')
        
        self.assertEquals(1, len(infos))
        
        self.assertEquals( set([severity.INFORMATION] * 2), 
                           set([v.getSeverity() for v in infos]))
        
        self.assertEqual( v.getName(), 'Mark of the web')
        
        