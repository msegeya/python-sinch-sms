import urllib2
import base64
import json

class SinchSMS:
    def __init__(self, appKey, appSecret):
        self.appKey = appKey
        self.appSecret = appSecret

    def post_request(self, url, values):
        jsonData = json.dumps(values)
        req = urllib2.Request(url, jsonData)
        req.add_header('content-type', 'application/json')
        req.add_header('authorization', b'basic ' + base64.b64encode('application:' + self.appKey + b':' + self.appSecret))
        connection = urllib2.urlopen(req)
        response = connection.read()
        connection.close()
        return response

    def get_request(self, url):
        req = urllib2.Request(url)
        req.add_header('authorization', b'basic ' + base64.b64encode('application:' + self.appKey + b':' + self.appSecret))
        connection = urllib2.urlopen(req)
        response = connection.read()
        connection.close()
        return response

    def send_message(self, to_number, message, from_number=None):
        """ Send a message to the specified number and an optional from number.
            Returns a tuple containing the sent messageId and error string.
        """
        values = { 'Message' : message }
        if from_number:
            values['From'] = from_number
        url = 'https://messagingApi.sinch.com/v1/sms/' + to_number
        response = [None, None]
        try:
            response[0] = json.loads(self.post_request(url, values))['MessageId']
        except urllib2.HTTPError as e:
            response[1] = e.reason
        except:
            pass
        return tuple(response)

    def check_status(self, message_id):
        """ Returns the status string of the message with the provided id.
            Status may have one of four values:

            Unknown - The status if the provided message id is not known
            Pending - The message is in the process of being delivered
            Successful - The message has been delivered to the recipient
            Faulted - The message has not been delivered, this can be due to an invalid number for instance.
        """
        url = 'https://messagingApi.Sinch.com/v1/message/status/' + str(message_id)
        responseData = self.get_request(url)
        response = json.loads(responseData)
        return response["Status"]

