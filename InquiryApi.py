class InquiryApi:
    @classmethod
    def inquiry_make(cls, problem):
        print('Collected Inquiry' + str(problem))
        # problem -> to back
        return 1  # id

    @classmethod
    def inquiry_receive(cls, inquiry_id):
        print('Fetched from back with id' + str(inquiry_id))
        # from back -> problem(id)
        return 4  # Issue solved
