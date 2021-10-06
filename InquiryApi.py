import random

class InquiryApi:
    @classmethod
    def inquiry_make(cls, problem):
        print('Inquiry has been sent')
        print('Collected Inquiry' + str(problem))
        # problem -> to back
        return random.randint(0, 3)  # id

    @classmethod
    def inquiry_receive(cls, inquiry_id):
        print('Inquiry has benn received')
        print('Fetched from back with id' + str(inquiry_id))
        # from back -> problem(id)
        if inquiry_id == 1: # Issue solved
            return 4
        return 3  # Issue in process
