import xml.etree.ElementTree as ET
import requests
import time

class OAIHarvester:
    def __init__(self, base_url):
        self.base_url = base_url

    def make_request(self, verb, **kwargs):
        params = {'verb': verb}
        params.update(kwargs)
        response = requests.get(self.base_url, params=params)
        return response


    def list_records(self, metadata_prefix,**kwargs):
        #all_records = []
        #print("list_records")
  
        resumption_token = None
        count = 1
        while True:
            if resumption_token:
                response = self.make_request('ListRecords', resumptionToken=resumption_token)
            else:
                response = self.make_request('ListRecords', metadataPrefix=metadata_prefix, **kwargs)

            try:
                root = ET.fromstring(response.content)
                # all_records.extend(root.findall('.//{http://www.openarchives.org/OAI/2.0/}record'))
                
                file = "xml/page"+str(count)+".xml"
                
                root = ET.ElementTree(root)
                root.write(file)
                count += 1
                
                resumption_token_element = root.find('.//{http://www.openarchives.org/OAI/2.0/}resumptionToken')
                if resumption_token_element is not None and resumption_token_element.text:
                    resumption_token = resumption_token_element.text
                    #print("resumption_token", resumption_token)
                else:
                    break
            except ET.ParseError:
                break
            
            
if __name__=="__main__":
    start_wall_time = time.time()  # Capture the start wall time
    start_cpu_time = time.process_time()  # Capture the start CPU time
    
    
    test_url = "https://bibsys.alma.exlibrisgroup.com/view/oai/47BIBSYS_NETWORK/request"
    harvester = OAIHarvester(test_url)
    harvester.list_records('marc21', 
                                 set='norart')
    
    end_wall_time = time.time()  # Capture the end wall time
    end_cpu_time = time.process_time()  # Capture the end CPU time

    # Calculate elapsed times
    elapsed_wall_time = end_wall_time - start_wall_time
    elapsed_cpu_time = end_cpu_time - start_cpu_time

    print(f"Elapsed wall clock time: {elapsed_wall_time:.2f} seconds")
    print(f"Elapsed CPU time: {elapsed_cpu_time:.2f} seconds")  
    print("Done!")