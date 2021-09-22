# Globals
GREETING = 'Здравствуйте! Я - помощник по проблемам с ЖКХ в вашем доме. \
Хотите оформить заявку или проверить статус?'

def handler(event, context):
    if 'request' in event and \
            'original_utterance' in event['request'] \
            and len(event['request']['original_utterance']) > 0:
        text = event['request']['original_utterance']
    elif event['session']['new'] == True:
        text = GREETING

    return {
        'version': event['version'],
        'session': event['session'],
        'response': {
            # Respond with the original request or welcome the user if this \
            # is the beginning of the dialog and the request has not yet been made.
            'text': text,
            # Don't finish the session after this response.
            'end_session': 'false'
        },
    }
