
# TBD
# TBD
# TBD

class CourseMemberships(Data):
    def __init__(self):
        self.type_of_data = "memberships"
        super().__init__("", "", True, "")

    def __str__(self) -> str:
        return super().__str__()
    

read_users = CourseMemberships()
print(read_users.dummy_users_created)


