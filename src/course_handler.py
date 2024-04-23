import dsk_handler


class DummyCoursesHandler(dsk_handler.DSK):
    def __init__(self):
        super().__init__()
        self.create_course_endpoint_summary = "Create Course"
        self.course_view_types = ['Classic', 'Ultra', 'Undecided', 'UltraPreview']
        self.course_handler_metadata = {
                'type': 'courses',
                'location': self.curr_path + "/database/dummy_courses.json",
                'fields_to_update':['dataSourceId','ultraStatus']
        }
        self.dsk = self.return_dsk()
        self.courses_dummy_data = []

    # Most files should follow this logic!!
    # First, we create the random data based on our dummy file.
    def create_course_payload(self, requested_data:int):
        dummy_data_gen = self.dummy_data_generator_main(requested_data=requested_data, dummy_data_metadata=self.course_handler_metadata)
        self.courses_dummy_data = dummy_data_gen
        return self.courses_dummy_data
    


    # Creates a list of course types based on the requested data
    def create_course_view_list(self, course_view_type:str, requested_data:int):
        course_view_options = {
            'random_all': self.course_view_types,
            'random': [self.course_view_types[0], self.course_view_types[1]],
            'original': [self.course_view_types[0]],
            'ultra': [self.course_view_types[1]]
        }

        course_view = course_view_options.get(course_view_type)

        if course_view is None:
            print('The course view type is not valid')
            return False
        else:
            course_view_list = self.random_data_generator(requested_data,course_view_options.get(course_view_type))
            return course_view_list

    def post_course(self, requested_data:int):
        request = self.caller_main(method_summary=self.create_course_endpoint_summary, dummy_data=self.courses_dummy_data, type_of_dummy_data=self.course_handler_metadata['type'], requested_data=requested_data)

        return request
    
    def create_dummy_courses_main(self, type_of_course_view:str, requested_data:int):
        # create the dummy data
        self.create_course_payload(requested_data)
        # Assign DSK
        self.courses_dummy_data = self.assign_value_to_key_in_dummy(dummy_data=self.courses_dummy_data, key='dataSourceId', value=self.dsk)
        # create course view list
        course_view_list = self.create_course_view_list(course_view_type=type_of_course_view, requested_data=requested_data)
        # update the dummy list with the course view list
        self.courses_dummy_data = self.assign_value_to_key_in_dummy(dummy_data=self.courses_dummy_data, key='ultraStatus', value=course_view_list)
        # post the course
        self.post_course(requested_data)
        # return data
        return self.courses_dummy_data
    



if __name__ == "__main__":
    new_dummy_courses = DummyCoursesHandler()
    print(new_dummy_courses.create_dummy_courses_main("original", requested_data=2))
