from flask import Flask, request, redirect
from twilio.rest import TwilioRestClient
import twilio.twiml

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])

def hello_monkey():
    """Respond to incoming calls with a simple text message."""
    body = request.values.get('Body', None)
    resp = twilio.twiml.Response()
    if body == 'Reorder':
        resp.message('Order Placed. Thanks, you brilliant human being!')
    elif body != 'Reorder':
        resp.message("Order not placed. If you meant to reorder, type 'Reorder' again.")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
    hello_monkey()
