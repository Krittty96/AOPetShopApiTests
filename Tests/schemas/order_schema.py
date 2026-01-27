ORDER_SCHEMA = {
    'type': 'object',
    'properties': {
        'id': {
            'type': 'integer',
            'minimum': 1
        },
        'petId': {
            'type': 'integer',
            'minimum': 1
        },
        'quantity': {
            'type': 'integer',
            'minimum': 1
        },
        'shipDate': {
            'type': 'string',

            'format': 'date-time'
        },
        'status': {
            'type': 'string',

            'enum': ['placed', 'approved', 'delivered']
        },
        'complete': {
            'type': 'boolean'
        }
    },
    'required': ['id', 'petId', 'quantity', 'status', 'complete'],
    'additionalProperties': False
}