from robot.api import logger
import requests

class _GloableKeywords(object):
    '''global keywords'''

    def __init__(self):
        '''init function'''
        pass

    def setBaseUrl(self,baseUrl):
        '''set base url'''
        _globalVariables.BASEURL=baseUrl

    def login(self,username,password):
        '''login keyword'''

        _globalVariables.SESSION=requests.session()

        loginURL=_globalVariables.BASEURL+'/ITAS/login'

        loginData={}
        loginData['language'] = 'en_US'
        loginData['username'] = username

        import hashlib
        m = hashlib.md5()
        m.update(password+username+'8#d$Up2z')
        loginData['password'] = m.hexdigest()

        loginData['jcaptchaCode'] = ''
        loginData['_DATA'] = ''
        loginData['_FUNCTION'] = ''

        loginResponse=_globalVariables.SESSION.post(loginURL,loginData)
        return loginResponse.text

    def isLoginSuccess(self,loginResp):
        '''check whether login successfully'''

        if 'Hello' in loginResp:
            logger.info('login successfully',also_console=True)
            return True
        else:
            logger.error('login failed with response:'+loginResp)
            return False

    def loginOut(self):
        '''login out keywords'''

        loginOutURL = _globalVariables.BASEURL + '/ITAS/logout.do'

        _globalVariables.SESSION.get(loginOutURL)

    @staticmethod
    def parseRespToDictOrCuple(resp):
        '''cut string'''
        s = resp.index('[')
        e = resp.index(']')
        searchRegisterTmp1 = resp[s + 1:e]

        '''convert null to 'null' '''
        searchRegisterTmp2 = searchRegisterTmp1.replace('null', "''")

        '''convert string to dict or tuple'''
        searchRegisterTmp2 = eval(searchRegisterTmp2)
        return searchRegisterTmp2

    @staticmethod
    def subString(str,leftBoudary,rightBoudary):
        startIndex=str.index(leftBoudary)+len(leftBoudary)
        endIndex=str.index(rightBoudary,startIndex)
        return str[startIndex:endIndex]


    @staticmethod
    def rSubString(str, leftBoudary, rightBoudary):
        endIndex = str.index(rightBoudary)
        startIndex = str.rindex(leftBoudary,0,endIndex)
        return str[startIndex+len(leftBoudary):endIndex]

class _globalVariables:
    SESSION=''
    BASEURL=''