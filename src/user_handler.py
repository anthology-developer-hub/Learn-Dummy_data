import dsk_handler
import uuid

class DummyUsersHandler(dsk_handler.DSK):
    def __init__(self):
        super().__init__()
        self.create_users_endpoint_summary = "Create User"
        self.user_handler_metadata = {
                'type': 'users',
                'location': self.curr_path + "/database/dummy_users.json",
                'fields_to_update': ['dataSourceId', 'password']
        }
        self.dsk = self.return_dsk()
        self.users_dummy_data = []

    def create_users_payload(self, requested_data:int):
        dummy_data_gen = self.dummy_data_generator_main(requested_data=requested_data, dummy_data_metadata=self.user_handler_metadata)
        self.users_dummy_data = dummy_data_gen
        return self.users_dummy_data
        
    
    def create_password_list(self, requested_data:int, type_of_password:str, custom_password:str=""):
        # got one for all, random for all, custom
        password_options = ['one_for_all','random_for_all','custom']
        password_list = []
        if type_of_password not in password_options:
            print('The password type is not valid')
            return False
        elif type_of_password == "one_for_all":
            password_list = [str(uuid.uuid4())] * requested_data
        elif type_of_password == "random_for_all":
            for _ in range(requested_data):
                password_list.append(str(uuid.uuid4()))
        elif type_of_password == "custom":
            if custom_password == "":
                print('When setting password custom it cannot be empty')
                return False
            else:
                password_list = [custom_password] * requested_data

        return password_list
    
    def post_users(self, requested_data:int):
        request = self.caller_main(method_summary=self.create_users_endpoint_summary, dummy_data=self.users_dummy_data, type_of_dummy_data=self.user_handler_metadata['type'], requested_data=requested_data)
        return request
    
    def create_dummy_users_main(self, requested_data:int, type_of_password:str, custom_password:str=""):
        # create the dummy data
        self.create_users_payload(requested_data)
        # Assign DSK
        self.users_dummy_data = self.assign_value_to_key_in_dummy(dummy_data=self.users_dummy_data, key='dataSourceId', value=self.dsk)
        # create Password list
        password_list = self.create_password_list(requested_data=requested_data, type_of_password=type_of_password, custom_password=custom_password)
        # update the dummy list with the course view list
        self.users_dummy_data = self.assign_value_to_key_in_dummy(dummy_data=self.users_dummy_data, key='password', value=password_list)
        # post the course
        self.post_users(requested_data)
        # return data
        return self.users_dummy_data


if __name__ == "__main__":
    new_dummy_users = DummyUsersHandler()
    print(new_dummy_users.create_dummy_users_main(2, "one_for_all"))