import data_handler
import requests
import re
import json

class Caller(data_handler.DummyDataGenerator):
    '''
    This class is used to make the calls to the API
    '''
    def __init__(self):
        super().__init__()
        self.returned_headers = {}
        # used to determine the variables on an endpoint
        self.regex = "\{(.*?)\}"
        self.remaining = {}
        self.expected_arguments = ""
        self.token = self.token_main()
        # required for DSK
        

    # Returns a list of variables within an endpoint
    def endpoint_arguments(self, endpoint):
        arguments = re.findall(self.regex, endpoint)
        self.expected_arguments = "Expecting arguments: " + str(arguments)
        return arguments

    # This function returns an url with the arguments passed
    # It organizes the values accordingly in same order they are received
    # Names in kwargs should match the same in the {argument} url format
    # eg: /learn/api/public/v1/courses/{courseId}/users/{userId} has two courseId and userId

    def validate_arguments(self, endpoint, arguments):
            args = self.endpoint_arguments(endpoint)
            # Assume all vales exist
            arguments_exist = True
            values_in_arguments = True

            # We make sure the arguments are correct an do have values
            for argument in args:
                # We check if the argument exists and matches the endpoint
                if argument not in arguments:
                    arguments_exist = False
                # Now we evaluate if the argument has a value
                if (arguments.get(argument) == "" or arguments.get(argument) == None):
                    values_in_arguments = False

            if arguments_exist and values_in_arguments:
                return True
            else:
                return False
            
    def build_url_with_arguments(self, endpoint, arguments):
        if self.endpoint_arguments(endpoint) == []:
            url = self.learn_instance + endpoint
            print(url)
            return url
        else:
            for key, value in arguments.items():
                endpoint = endpoint.replace("{" + key + "}", value)
            
            url = self.learn_instance + endpoint
            return url
                    
    def request(self, url, method, payload={}):
        headers = self.token_headers()
        match method:
            case "get":
                data = requests.get(url, headers=headers)
            case "post":
                data = requests.post(url, headers=headers, json=payload)
            case "delete":
                data = requests.delete(url, headers=self.token)
            case "patch":
                data = requests.patch(url, headers=self.token, json=payload)
            case "put":
                data = requests.put(url, headers=self.token, json=payload)

        return json.dumps({"status_code": data.status_code, "result": json.loads(data.text)})
    
    
    def caller_main(self, method_summary:str, dummy_data:list=[], requested_data:int=0, type_of_dummy_data:str="", arguments:dict={}):
        # First we need to get the method and the url
        method_and_url = self.obtain_method_and_url(method_summary)
        print(method_and_url)
        print(arguments)
                
        if type_of_dummy_data == "dsk":
            call_url = self.build_url_with_arguments(method_and_url["endpoint"], arguments)
            request = self.request(call_url, method_and_url["method"], payload=self.dsk_payload)
            return request

        if self.validate_arguments(method_and_url["endpoint"], arguments):
            call_url = self.build_url_with_arguments(method_and_url["endpoint"], arguments)
            print(self.expected_arguments)
        else:
            print("Arguments are not correct")
            return False


        succesfully_created_data = []
        failed_data = []
        
        # Then we need to make the call to the API when the dummy data is a list
        for dummy in dummy_data:
            dummy_id = dummy['id']
            dummy = dummy['values']
            request = self.request(call_url, method_and_url["method"],payload=dummy)
            request = json.loads(request)
            if request['status_code'] in [200, 201]:
                succesfully_created_data.append(dummy_id)
            else:
                failed_data.append(request)

        self.update_value_for_one_key_in_dummy_data_stored(key_to_be_updated=type_of_dummy_data, value=succesfully_created_data)
        
        string_to_return = f"Successfully created {len(succesfully_created_data)} out of {len(dummy_data)} and failed to create {len(failed_data)}"

        print(f"This data failed: {failed_data}")

        print(string_to_return)
        

        return succesfully_created_data

        # then we need to start storing the data on


if __name__ == "__main__":
    # this is test data
    # test_args = {"courseId": "_1111_1", "userId": "_2222_1"}
    #instance call
    new_caller = Caller()
    #print(new_caller.caller_main(method_summary="Get Resources"))
    # cannot be tested without a payload
    #print(new_caller.caller_main(method_summary="Create Course", requested_data=5, type_of_dummy_data="users"))