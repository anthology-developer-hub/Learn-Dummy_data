import random
import token_handler as token
# import call_handler as call
# import dsk_handler as dsk

class DummyDataGenerator(token.Token):
    '''
        This class is used to create random data, organize it and help count available and used data on each dummy files, also it helps assigning the DSK to the data. 
    '''
    def __init__(self):
        super().__init__()
        self.type_of_dummy_data = ""
        self.dummy_data_location = ""
        self.type_of_data = ['courses','users','memberships', 'dsk']
        self.dummy_data_deployed = self.read_file_return_json(self.dummy_data_stored)

    def find_instance(self):
        for i in self.dummy_data_deployed:
            if i.get(self.learn_instance):
                return i[self.learn_instance]
        return False

    def used_ids(self, type_of_dummy_data: str):
        instance = self.find_instance()
        if instance:
            return instance[type_of_dummy_data]
        return []

    # Here I want to remove the used ids from the list of available ids
    def data_filter(self, used_ids, requested_data: int):
        dummy_data = self.read_file_return_json(self.dummy_data_location)
        if len(dummy_data) < requested_data + len(used_ids):
            print("The requested data is greater than the available data")
            return False
        elif used_ids:
            dummy_data = [item for i, item in enumerate(dummy_data) if i not in used_ids]

        return self.random_data_generator(requested_data, dummy_data)

    # Generate actual random data based on the requested data after filtering the used ids
    def random_data_generator(self, requested_data: int, data: list):
        new_list = []
        for _ in range(requested_data):
            random_value = random.choice(data)
            new_list.append(random_value)
        
        return new_list
    
    def has_dummy_data_been_deployed(self):
        data_deployed = False
        for deployed_instance in self.dummy_data_deployed:
            if deployed_instance.get(self.learn_instance) is not None:
                    data_deployed = True
                    return data_deployed

    def first_time(self):
        # This function will be used to create the first time the data is deployed to the server
        first_time_dummy_data = {
                self.learn_instance: {
                    "dsk": "",
                    "users": [],
                    "courses": [],
                    "memberships_course_user": []
                }
            }
        self.dummy_data_deployed.append(first_time_dummy_data)
        self.write_file_json(self.dummy_data_stored, self.dummy_data_deployed)
        print("first time data deployed to the server.")
        return True

    # Assign a value to a key in the dummy data and extends the list
    def assign_value_to_key_in_dummy(self, dummy_data ,key:str, value):
        updated_dummy = []
        for index, dummy in enumerate(dummy_data):
            if isinstance(value, list):
                dummy['values'][key] = value[index]
            elif isinstance(value, str):
                dummy['values'][key] = value
            
            updated_dummy.append(dummy)
            
        return updated_dummy

    # Main function
    def dummy_data_generator_main(self, requested_data: int, dummy_data_metadata:dict):
        # setting variables based on metadata dictionary
        self.type_of_dummy_data = dummy_data_metadata.get('type')
        self.dummy_data_location = dummy_data_metadata.get('location')

        # Validate the type of dummy data is supported and valid
        if self.type_of_dummy_data not in self.type_of_data:
            print(f"'{self.type_of_dummy_data}' is not a valid type of dummy data, please use one of the following: {self.type_of_data}")
            return False
        
        # Check if the dummy data has ever been deployed
        if self.find_instance() in [None, False, ""]:
            self.first_time()

        # Validate the url exists first
        used_ids = self.used_ids(self.type_of_dummy_data)

        new_random_data = self.data_filter(used_ids, requested_data)
        print(f"{self.type_of_dummy_data} dummy data created")
        return new_random_data
    

if __name__ == "__main__":
    new_dummy = DummyDataGenerator()
    user_handler_metadata = {
                'type': 'users',
                'location': "/Users/davey.herrera/Documents/dummy_data_real/local_deployment/learn_api_explorer/dummy_users.json",
                'fields_to_update':['dataSourceId','password']
    }
    data = new_dummy.dummy_data_generator_main(5, user_handler_metadata)
    print(data)