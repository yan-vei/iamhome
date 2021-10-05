class Request:
    def __init__(self, request_body):
        self.request_body = request_body

    def __getitem__(self, key):
        return self.request_body[key]

    @property
    def intents(self):
        return self.request_body['request'].get('nlu', {}).get('intents', {})

    @property
    def report_state(self):
        state = self.request_body['state']
        if state.get('user').get('report_id') is not None:
            return state.get('user', {}).get('report_id')
        else:
            return state.get('application', {}).get('report_id')

    @property
    def problem_state(self):
        state = self.request_body['state']
        return state.get('session', {}).get('problem', {})

    @property
    def intent_name(self):
        state = self.request_body['state']
        return state.get('session', {}).get('problem', {}).get('intent_name')

    @property
    def address_floor(self):
        state = self.request_body['state']
        return state.get('session', {}).get('problem', {}).get('floor')

    @property
    def problem_location(self):
        state = self.request_body['state']
        return state.get('session', {}).get('problem', {}).get('location')

    @property
    def problem_address(self):
        state = self.request_body['state']
        return state.get('session', {}).get('problem', {}).get('address', {})

    @property
    def entities(self):
        return self.request_body['request'].get('nlu', {}).get('entities', {})

    @property
    def type(self):
        return self.request_body.get('request', {}).get('type')