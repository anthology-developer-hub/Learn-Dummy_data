from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import global_util as util
from datetime import timedelta
import read_learn_json as swagger_reader
from time import sleep


class Token(swagger_reader.SwaggerReader, util.Utilities):
    def __init__(self):
        super().__init__()
        self.token_file_name = "token.json"
        self.token_method_and_url = self.obtain_method_and_url("Request Token")
        self.token_endpoint_path = self.token_method_and_url["endpoint"]
        self.token_endpoint_method = self.token_method_and_url['method']
        # This empty dictionary receives the token payload
        self.token_payload = {}
        self.token_file_location = self.curr_path + "/database/" + self.token_file_name
        

    # If the token exists, validate it, if not, generate a new one
    def token_file_exist(self):
        if self.file_exists(self.token_file_location):
            return True
        else:
            return False
        
    def return_token(self):
        return self.read_file_return_json(self.token_file_location)["authorization"]

    def token_main(self):
        if self.token_file_exist():
            if self.is_token_date_valid():
                print("Token exists and date is valid")
            else:
                print("removing token since it expired")
                self.remove_file(self.token_file_location)
                sleep(1)
                print("old token file removed")
        else:
            print("creating a new token")
            self.generate_token()
            sleep(1)
        
        return self.return_token()

    # Is the token date "valid"
    def is_token_date_valid(self):
        # a token date is valid when the date in the file is bigger than now()
        token_date = self.read_file_return_json(self.token_file_location)["token_expiration_date"]
        if self.date_converter(token_date, 'datetime') > self.now:
            return True
        else:
            return False

    # Generate a new token
    def generate_token(self):
        try:
            client = BackendApplicationClient(client_id=self.application_key)
            oauth = OAuth2Session(client=client)
            token_payload = oauth.fetch_token(token_url=self.learn_instance + self.token_endpoint_path, client_id=self.application_key, client_secret=self.secret)
            self.token_payload = token_payload
            self.create_token_tmp_file()
            print("Token Generated")
            return True
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        return False

    # Define the date on which the token will expire
    def set_token_expiration_date(self, token_expires_in):
        # token expt date has to be changed to str to be dumped in json to the external file
        token_expiration_date = self.now + \
            timedelta(seconds=int(token_expires_in))
        return str(token_expiration_date)

    # Generates the token temporary file
    def create_token_tmp_file(self):
        try:
            file_content = {
                "authorization": self.token_payload['access_token'],
                "token_expiration_date": self.set_token_expiration_date(self.token_payload['expires_in'])
                }
            self.write_file_json(self.token_file_location ,file_content)
            print("New token file created")
            return True
        except Exception as e:
            print(f"There was an error creating the token file {e}")
            return False

    # Creates the token authorization dictionary
    def token_headers(self):
        token_bearer = {
            "authorization": f"Bearer {self.return_token()}",
        }
        return token_bearer
    

# This file reale needs complete re-do!!!1
    
if __name__ == "__main__":
    # first instantiate the object
    new_token = Token()
    print(new_token.token_headers())
