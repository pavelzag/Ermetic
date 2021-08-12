import json
import logging

from flask import Flask, request

app = Flask(__name__)

global requests_log
requests_log = {}

global somethig_something
OK_MESSAGE = 'OK'
ERROR_MESSAGE = 'Service Unavailable'

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


@app.route('/', methods=['GET'])
def index():
    client_id = request.args.get('clientId', '')
    print(f'Incoming client_id is {client_id}')
    if len(requests_log) == 0:
        requests_log.update({client_id: {"requests_amt": 1}})
    elif len(requests_log) != 0 and str(client_id) not in requests_log.keys():
        requests_log.update({client_id: {"requests_amt": 1}})

    elif len(requests_log) != 0 and str(client_id) in requests_log.keys():
        current_requests_amt = requests_log[client_id]['requests_amt']
        current_requests_amt += 1
        if current_requests_amt >= 5:
            requests_log.update({client_id: {"requests_amt": current_requests_amt}})
            error_response = app.response_class(
                response=json.dumps(ERROR_MESSAGE),
                status=503,
                mimetype='application/json'
            )
            return error_response
        else:
            requests_log.update({client_id: {"requests_amt": current_requests_amt}})
            ok_response = app.response_class(
                response=json.dumps(OK_MESSAGE),
                status=200,
                mimetype='application/json'
            )
            return ok_response

    return json.dumps(requests_log)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', use_reloader=True, port=80)

