import urllib.request
import json
import device_check as device
from time import sleep

# device calls utilites and api gen calls device

class LearnJsonApiGenerator(device.Device):
    def __init__(self) -> None:
        # The constructor super() is required to access the parent class, we need to first call it in order to have access to the init values of the inherited class
        super().__init__()
        # I really do hope this swagger url is never updated, if it is, here is where the new swagger url json file should be placed
        self.learn_swagger_url = "http://devportal-docstore.s3.amazonaws.com/learn-swagger.json"
        self.swagger_file_name = "swagger.json"
        self.path_to_swagger_file = self.curr_path + "/database/" + self.swagger_file_name
        self.path_swagger_json = self.curr_path + "/database/" + "path_swagger.json"
        self.swagger_last_update_file_name = self.curr_path + "/database/" + "swagger_last_update.json"
        self.minimal_requirements = self.validate_device()
        if not self.minimal_requirements:
            raise Exception("The device does not meet the minimal requirements to run this script")
    
    def does_swagger_exist(self):
        print("Checking if swagger exists")
        if self.file_exists(self.path_to_swagger_file) in [None,False, ""]:
            print("Swagger does not exist")
            return False
        else:
            print("Swagger exists")
            return True
        
    def download_learn_swagger(self):
        try:
            urllib.request.urlretrieve(self.learn_swagger_url, self.path_to_swagger_file)
            self.last_time_learn_swagger_was_downloaded()
        except urllib.error.URLError:
            print("There was an error downloading the swagger file")
            return False
        
    # This exists to avoid having an old version of the swagger.
    def last_time_learn_swagger_was_downloaded(self):
        self.write_file(self.swagger_last_update_file_name, json.dumps({"date": str(self.today)}))
        print("Swagger file that controls the last time swagger was downloaded has been created")
        return {"date used": str(self.today)}

    def is_swagger_file_old(self):
        swagger_last_update = self.date_converter(self.read_file_return_json(self.swagger_last_update_file_name)['date'], 'date')
        if self.today > swagger_last_update:
            print("Swagger file is old")
            return True
        else:
            print("Swagger is up to date")
            return False
        
    def remove_files(self):
        self.remove_file(self.path_to_swagger_file)
        self.remove_file(self.path_swagger_json)
        self.remove_file(self.swagger_last_update_file_name)
        print("Files removed")
        return True


    def create_new_summary_based_swagger(self):
        try:
            summary_to_endpoint = {}
            swagger = self.read_file_return_json(self.path_to_swagger_file)
            for endpoint in swagger['paths']:
                for method in swagger['paths'][endpoint]:
                        summary_to_endpoint.update({
                            swagger["paths"][endpoint][method]["summary"]:{
                                "endpoint": endpoint,
                                "method": method
                            }
                        })
            self.write_file_json(self.path_swagger_json , summary_to_endpoint)
            sleep(2)
            return True
        except KeyError:
            print("There was an error creating the new summary based swagger")
            return False 
        
    # Main function
    def swagger_generator_main(self):
        if self.does_swagger_exist():
            if self.is_swagger_file_old():
                self.remove_files()
                self.download_learn_swagger()
                self.create_new_summary_based_swagger()
        else:
            self.download_learn_swagger()
            self.create_new_summary_based_swagger()

        return True
            
                        
if __name__ == "__main__":
    new_swagger = LearnJsonApiGenerator()
    print(new_swagger.swagger_generator_main())