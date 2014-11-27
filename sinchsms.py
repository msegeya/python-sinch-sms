"""
sinchsms - a module to send sms using the Sinch REST apis, www.sinch.com
"""

import requests

class SinchSMS(object):
    """ A class for handling communication with the Sinch REST apis. """
    def __init__(self, app_key, app_secret):
        """Create a SinchSMS client with the provided app_key and app_secret.

           Visit your dashboard at sinch.com to locate your application key and secret.
           These can be found under apps/credentials section.
        """
        self._auth = ('application:' + app_key, app_secret)

    def _request(self, url, values=None):
        """ Send a request and read response. """
        if values:
            response = requests.post(url, json=values, auth=self._auth)
        else:
            response = requests.get(url, auth=self._auth)

        try:
            result = response.json()
        except ValueError as exception:
            return {'errorCode':1, 'message':str(exception)}

        return result

    def send_message(self, to_number, message, from_number=None):
        """ Send a message to the specified number and return a response dictionary.

            The numbers must be specified in international format starting with a '+'.
            Returns a dictionary that contains a 'MessageId' key with the sent message id value or
            contains 'errorCode' and 'message' on error.

            Possible error codes:
                 40001 - Parameter validation
                 40002 - Missing parameter
                 40003 - Invalid request
                 40100 - Illegal authorization header
                 40200 - There is not enough funds to send the message
                 40300 - Forbidden request
                 40301 - Invalid authorization scheme for calling the method
                 50000 - Internal error
        """

        values = {'Message': message}
        if from_number is not None:
            values['From'] = from_number

        url = 'https://messagingApi.sinch.com/v1/sms/' + to_number

        return self._request(url, values)

    def check_status(self, message_id):
        """ Request the status of a message with the provided id and return a response dictionary.

            Returns a dictionary that contains a 'Status' key with the status value string or
            contains 'errorCode' and 'message' on error.

            Status may have one of four values:
                Pending - The message is in the process of being delivered.
                Successful - The message has been delivered to the recipient.
                Unknown - The status of the provided message id is not known.
                Faulted - The message has not been delivered, this can be due to an
                          invalid number for instance.
        """

        url = 'https://messagingApi.sinch.com/v1/message/status/' + str(message_id)

        return self._request(url)

