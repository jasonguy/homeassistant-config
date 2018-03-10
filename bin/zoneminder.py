import json, logging, requests
import cookielib, urllib2

class ZoneMinder:
    def __init__(self, ip, username, password):
        self.ip = ip
        self.username = username
        self.password = password
        self.logger = logging.getLogger()
        self.session = requests.Session()
        self.__login()

    def __login(self):
        url = "http://{}/zm/index.php".format(self.ip)
        params = {
            "username": self.username,
            "password": self.password,
            "action": "login",
            "view": "console"
        }
        result = self.session.post(url, data=params)

    def getAllStates(self):
        url = "http://{}/zm/api/states.json".format(self.ip)
        result = self.session.get(url).json()
        self.logger.debug(result)
        return result['states']

    def getCurrentState(self):
        url = "http://{}/zm/api/states.json".format(self.ip)
        result = self.session.get(url).json()
        self.logger.debug(result)
        for state in result['states']:
            if int(state['State']['IsActive']):
                return state['State']['Name']

    def setState(self, state):
        url = "http://{}/zm/api/states/change/{}.json".format(self.ip, state)
        result = self.session.post(url)
        self.logger.debug("NMITCHELL: {}".format(result))

    def clearAlarm(self, mid):
        url = "http://{}/zm/api/monitors/alarm/id:{}/command:off.json".format(self.ip, mid)
        result = self.session.get(url)
        self.logger.debug(result)
        return result

    def triggerAlarm(self, mid):
        url = "http://{}/zm/api/monitors/alarm/id:{}/command:on.json".format(self.ip, mid)
        result = self.session.get(url)
        self.logger.debug(result)
        return result
