import json
import os
from datetime import datetime, date

class Utilities():
    '''
    These are normal functions that can be used in any class, they are not related to any specific class.
    '''
    def __init__(self) -> None:
        self.now = datetime.now()
        self.today = date.today()
        self.time = self.now.strftime('%Y-%m-%d %H:%M:%S')
        self.curr_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.config_location = self.curr_path + "/config/config.json"
        self.dummy_data_stored = self.curr_path + "/database/dummy_data_stored.json"
        self.dummy_dsk_location = self.curr_path + "/database/dummy_dsk.json"
        self.id_pattern = r'^_[0-9]+_1$'
        self.application_key = self.read_file_return_json(self.config_location)["application_key"]
        self.secret = self.read_file_return_json(self.config_location)["secret"]
        self.learn_instance = self.read_file_return_json(self.config_location)["url"]
        self.config_json_file = self.read_file_return_json(self.config_location)
    
    def __str__(self) -> str:
        return "Utilities class for the learn api explorer"
    
    def file_exists(self, file_name):
        try:
            if os.path.isfile(file_name):
                print(os.path.isfile(file_name))
                return True
        except FileNotFoundError:
            return False

    def read_file(self, file_name):
        raw_data = open(file_name, "r")
        data = raw_data.read()
        raw_data.close()
        return data

    def write_file(self, file_name, data):
        file_name = open(file_name, "w")
        file_name.write(data)
        file_name.close()
        return data

    def read_file_return_json(self, file_location):
        config = self.read_file(file_location)
        config = json.loads(config)
        return config

    def write_file_json(self,file_name, data):
        file_name = open(file_name, "w")
        data_json = json.dumps(data, indent=4, sort_keys=True)
        file_name.write(data_json)
        file_name.close()
        return data_json
    
    def remove_file(self, file_name):
        os.remove(file_name)
        return file_name
    
    def date_converter(self, date, format:['date','datetime']):
        if format == 'date':
            return datetime.strptime(date, "%Y-%m-%d").date()
        elif format == 'datetime':
            return datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")
    
    def update_value_for_one_key_in_dummy_data_stored(self, key_to_be_updated:str, value:list):
        dummy_data_stored = self.read_file_return_json(self.dummy_data_stored)
        for instance in dummy_data_stored:
            if instance.get(self.learn_instance):
                try:
                    if key_to_be_updated =="dsk":
                        instance[self.learn_instance][key_to_be_updated] = value
                    else:
                        instance[self.learn_instance][key_to_be_updated].extend(value)

                    self.write_file_json(self.dummy_data_stored, dummy_data_stored)
                    return dummy_data_stored
                
                except KeyError:
                    print('The key does not exist in the dummy_data_stored.json file')
                    return False

if __name__ == "__main__":
    util = Utilities()
    print(util.curr_path)