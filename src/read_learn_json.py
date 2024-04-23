import create_learn_json as swagger_creator


class SwaggerReader(swagger_creator.LearnJsonApiGenerator):
    '''
    This class is used to read the generated swagger and return the method and path for a call, the call is considered to be the summary of the call. The summary of the call is a short name given to each endpoint.
    '''
    
    def __init__(self) -> None:
        super().__init__()
        
    def __str__(self) -> str:
        return "Swagger reader class for the learn api explorer"
    
    def obtain_method_and_url(self, summary_str):
        print(f"Returning method and path for: '{summary_str}'")
        self.swagger_generator_main()
        path_swagger = self.read_file_return_json(self.path_swagger_json)
        return path_swagger[summary_str]


# read_swagger_json will receive the summary name and return the method and path for the call
# if possible, it should also return required parameters and handle the optional parameters on the url. (This is a big one!)

if __name__ == "__main__":
    swagger_reader = SwaggerReader()
    print(swagger_reader.obtain_method_and_url("Create Course"))