class Request:
    def __init__(self, request_body):
        self.request_body = request_body

    def __getitem__(self, key):
        return self.request_body[key]

    @property
    def intents(self):
        return self.request_body['request'].get('nlu', {}).get('intents', {})

    @property
    def session_state(self):
        state = self.request_body['state']
        if state.get('user'):
            return state.get('user', {})
        else:
            return state.get('application', {})

    @property
    def type(self):
        return self.request_body.get('request', {}).get('type')