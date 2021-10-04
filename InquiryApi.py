class InquiryApi:
    @classmethod
    def InquiryMake(cls, problem):
        print('Collected Inquiry' + str(problem))
        # problem -> to back

    def InquiryReceive(self, id):
        print('Fetched from back with id' + str(id))
        # from back -> problem(id)
