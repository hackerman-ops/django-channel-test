from datetime import timedelta

BEAT_SCHEDULE = {
    'testing-print': {
        'type': 'test.print',
        'message': {'message': 'UUUU'},
        'schedule': timedelta(seconds=5)
    },
}
