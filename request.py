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
        if state.get('user') is not None:
            print("fetch user_state " + state.get('user', {}).get('report_id'))
            return state.get('user', {}).get('report_id')
        else:
            print("fetch  application_state " + state.get('application', {}).get('report_id'))
            return state.get('application', {}).get('report_id')

    @property
    def type(self):
        return self.request_body.get('request', {}).get('type')