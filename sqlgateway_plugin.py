'''
Created on Sep 27, 2017

@author: lauthjo
'''
import requests
import json
import logging
from ruxit.api.base_plugin import BasePlugin
from ruxit.api.snapshot import pgi_name
from bs4 import BeautifulSoup


        
class MonitorAppPlugin(BasePlugin):
    
    
            
    def query(self, **kwargs):
        pgi = self.find_single_process_group(pgi_name('apache-tomcat-*'))
        pgi_id = pgi.group_instance_id
       
        url = "http://localhost:8080/SQL%20GateWay/SQLGatewayServlet"
        
        payload = "sqlStatement=select%20count%20(*)%20from%20test"
        headers = {
            'content-type': "application/x-www-form-urlencoded",
            'cache-control': "no-cache"
        }

        response = requests.request("POST", url, data=payload, headers=headers)
        doc = BeautifulSoup(response.text,"html.parser")
        #print(doc.prettify())
        #print(doc.table.get_text())

        #print("\n-----------")

        #for line in doc.table:
        #        print(line)
        
        cnt = -1
            
        for row in doc.table.findAll("tr"):
            if not row.find("b"):
                cells = row.find("td")
                cnt = int(cells.get_text()) 
                
        #self.results_builder.absolute(key='random', value=doc.table.line['random'], entity_id=pgi_id)
        print(cnt)
        self.results_builder.relative(key='record_diff', value=cnt, entity_id=pgi_id)                       
                

                                                            