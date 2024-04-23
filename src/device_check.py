import requests
import global_util as util

# We call utilities as the parent class

class Device(util.Utilities):
    '''
    In order to avoid having issues related to internet connection, we have defined that every time a call is made to the learn instance, we will first check if the device complies with the minimal requirements
    '''

    def __init__(self) -> None:
        # The constructor super() is required to access the parent class, we need to first call it in order to have access to the init values of the inherited class
        super().__init__()
        self.health_check_path = "/webapps/portal/healthCheck"
        # The learn url should not have a / at the end
        self.learn_healthcheck_url = self.learn_instance + self.health_check_path
        self.test_url = "http://www.google.com"
        self.test_url_timeout = 5
        self.test_file_name = self.curr_path + "/" + "test.txt"

    def has_internet(self):
        try:
            result = requests.get(self.test_url, timeout=self.test_url_timeout)
            result = result.status_code
            if result == 200:
                print("The device has internet connection")
                return True
        except requests.ConnectionError:
            print("There is a problem with the internet connection, please check your internet connection and try again.")
            return False

    def is_learn_instance_available(self):
        try:
            result = requests.get(self.learn_healthcheck_url, timeout=self.test_url_timeout)
            if result.status_code == 200:
                print("Learn instance is available")
                return True
        except requests.ConnectionError:
            print("Unavailable learn instance. Please check the config file has the url written correctly.")
            print(self.learn_healthcheck_url)
            print("if the url is correct, please check that the learn instance is up and running.")
            return False
    
    def has_permissions_to_create_file(self):
        try:
            with open(self.test_file_name, "w") as f:
                f.write("testing if it is possible to write a file")
                f.close()
            print("The device has permissions to create files")
            self.remove_file(self.test_file_name)
            print("The test file was created and removed")
            return True
        except PermissionError:
            print("The device does not have permissions to create files")
            return False
    
    def is_config_file_present(self):
        if self.file_exists(self.config_location):
            print("The config file is present")
            return True
        else:
            print("The config file is not present")
            return False
    
    def does_config_file_have_data(self):
            for key in self.config_json_file.keys():
                if self.config_json_file[key] == "":
                    print(f"There seems to be missing information your config.json file please review {key}")
                    return False
                
            print("The config file is not empty, however, we cannot validate the content of the file")
            return True
    
    def validate_device(self):
        if self.has_internet() and self.is_learn_instance_available() and self.has_permissions_to_create_file() and self.is_config_file_present() and self.does_config_file_have_data():
            return True
        return False

if __name__ == "__main__":
    # instantiate new object
    new_device = Device()
    # call the method
    new_device.validate_device()