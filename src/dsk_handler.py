import call_handler
import json


class DSK(call_handler.Caller):
    def __init__(self):
        super().__init__()
        # This is the PayLoad to create the dummy data on Learn
        self.dsk_id = ""
        self.dsk_payload = self.read_file_return_json(self.dummy_dsk_location)
        self.dsk_stored_on_instance = self.find_instance()
        self.dsk_handler_metadata = {
                'type': 'dsk',
                'location': self.dummy_dsk_location,
                'fields_to_update': []
        }
    
    # 1. Read first the dummy_data_stored.json file to see if any dsk has been created.
    def does_dsk_exists_on_dummy_data_stored(self):
        print("Checking if the dsk exists on the dummy_data_stored.json file")
        if self.dsk_stored_on_instance in [None, False, ""] or self.dsk_stored_on_instance['dsk'] in [None, False, ""]:
                print("There is no dsk stored on the internal db")
                return False
        else:
            print("there is a dks stored on the internal db")
            self.dsk_id = self.dsk_stored_on_instance['dsk']
            return True
        
    # 2. If so, we need to VERIFY it does exist
    def does_stored_dsk_exists_on_learn(self):
        print("Verifying if the dsk on the file matches the one in Learn")
        data_source_id = {"dataSourceId": self.dsk_id}
        get_dsk_call = json.loads(self.caller_main("Get Data Source", arguments=data_source_id, type_of_dummy_data="dsk"))
        if get_dsk_call['status_code'] == 200:
            return True
        else:
            return False
        
    # 3. If the file dummy_data_stored.json does not have a dsk stored, we query for it
    def get_dsk(self):
        print("Getting the dsks available in Learn and verifying if one exists for Dummy data")
        # Getting the dataSources
        get_dsk_call = json.loads(self.caller_main("Get Data Sources",type_of_dummy_data="dsk", requested_data=1))
        # hard coded 1 for only one dsk
        print(get_dsk_call)
        for dsk in get_dsk_call['result']['results']:
            if dsk.get('externalId') == "dummy_data":
                self.dsk_id = dsk.get('id')
                
        if self.dsk_id == "":
            return False
        else:
            return True


    # 4. If it does not exist, we need to create a new one.
    def post_dsk(self):
        print("Creating a new dsk for dummy data")
        post_dsk_call = self.caller_main("Create Data Source", payload=self.dsk_payload, is_dsk=True)
        self.dsk_id = post_dsk_call['result']['id']
        return self.dsk_id
    
    # 5. We need to write the dsk on the dummy_data_stored.json file
    def write_dsk_on_db(self):
        updated_value = self.update_value_for_one_key_in_dummy_data_stored("dsk", self.dsk_id)
        print(f"Saved the dsk on the dummy_data_stored.json file. {updated_value}")
        return updated_value


    # 6. Return the dsk
    def return_dsk(self):
        #First we check if there is a value on the dummy_data_stored.json file
        if self.does_dsk_exists_on_dummy_data_stored():
            # if there is, we validate it
            print("There is a DSK stored on the dummy_data_stored.json file.")
            if self.does_stored_dsk_exists_on_learn():
                print("The DSK matches the one in Learn")
                # and return the dsk
        # Otherwise
        else:
            # We query learn to an existing dsk
            if self.get_dsk():
                # if it exists, we write it on the json file
                print("Writing the dsk on the dummy_data_stored.json file after looking for it")
                self.write_dsk_on_db()
            # otherwise
            else:
                # we create a new dsk
                self.post_dsk()
                # and write it on the json file
                print("Writing the dsk on the dummy_data_stored.json file after its creation")
                self.write_dsk_on_db()
                # and return the dsk id
            
        return self.dsk_id

                        
if __name__ == "__main__":
    dsk = DSK()
    print(dsk.return_dsk())