from robot.api import logger
import random,string

from _global import _GloableKeywords,_globalVariables


class _USERKeywords(object):
    '''apex user module keywords'''

    def __init__(self):
        pass

    def getOrganiztionIDByName(self,organizationName):
        '''
        get organizationID by organizationName
        :param organizationName:
        :return: organizationID
        '''

        path='/ITAS/apexOrganization.rootlist.do'
        apexOrganizationURL=_globalVariables.BASEURL+path
        apexOrganizationData = {
            'menuType': 2
        }
        apexOrganizationResp=_globalVariables.SESSION.post(apexOrganizationURL,apexOrganizationData)

        str=apexOrganizationResp.text
        midleIndex=str.index(organizationName)
        startIndex=str.rindex('{',0,midleIndex)
        endIndex=str.index('}',midleIndex)

        organizationInfo=str[startIndex:endIndex+1]
        organizationInfo = organizationInfo.replace('false', "False")
        organizationInfo = organizationInfo.replace('null', "''")
        organizationInfo= eval(organizationInfo)
        return organizationInfo['id']

    def createUserByAdmin(self,userName,loginName,organizationName):
        '''
        create a new user keyword
        :param userName:
        :param loginName:
        :return:string createUserByAdmin response
        '''
        path='/ITAS/apexUserLogin.insert.do'
        apexUserLoginInsertURL=_globalVariables.BASEURL+path

        identityCard=''.join(random.sample(string.digits, 8))
        apexUserLoginInsertData={
            'actionStatus': '',
            'description': '',
            'email': userName+'@qq.com',
            'enableDate': '',
            'expiryDate': '',
            'firstName': '',
            'fontSize': '',
            'fullName': userName,
            'gender': '',
            'hidActionName': 'insert',
            'lastLoginIp': '',
            'lastLoginTime': '',
            'lastName': '',
            'loginFailedNumber': '',
            'loginName': loginName,
            'middleName': '',
            'mobile': ''.join(random.sample(string.digits, 8)),
            'organization.sysGuid': self.getOrganiztionIDByName(organizationName),
            'orgUserStatus': '1',
            'otherName': ',,',
            'passwordAnswer': '',
            'passwordQuestion': '',
            'sysCreateDate': '',
            'sysCreateUser': '',
            'sysGuid': '',
            'sysId': '',
            'sysOwner': '',
            'sysRecycle': '',
            'sysUpdateDate': '',
            'sysUpdateUser': '',
            'userClassification': '',
            'userInfo.cityOfBirth': '',
            'userInfo.dateOfBirth': '',
            'userInfo.employeeNumber': '',
            'userInfo.ethnic': '',
            'userInfo.homeFax': '',
            'userInfo.homeTel': '',
            'userInfo.identityCard': ''.join(random.sample(string.digits, 8)),
            'userInfo.job': '',
            'userInfo.maritalStatus': '',
            'userInfo.nationality': '',
            'userInfo.officeLocation': '',
            'userInfo.photo': '',
            'userInfo.postalAddress': '',
            'userInfo.residentialAddress': '',
            'userInfo.signatureImage': '',
            'userInfo.sysGuid': '',
            'userLanguage': '',
            'userOrder': '',
            'userThemeId': '',
            'userType': '0'
        }
        apexUserLoginInsertResp=_globalVariables.SESSION.post(apexUserLoginInsertURL,apexUserLoginInsertData)

        return apexUserLoginInsertResp.text

    def isCreateUserByAdminSuccess(self,creatUserByAdminResp):
        '''
        creatUserByAdmin response
        :param creatUserByAdminResp:
        :return: True|False
        '''
        if 'true' in creatUserByAdminResp:
            logger.info('create user by admin succuessfully:' + creatUserByAdminResp, also_console=True)
            return True
        else:
            logger.error('create user by admin failed:' + creatUserByAdminResp)
            return False

    def createUserBySysadmin(self,userName,loginName,organizationName):
        '''
        create user by system admin,should be approve
        :param userName:
        :param loginName:
        :param organizationName:
        :return: string createUserBySysadmin respoonse
        '''

        # region get business key request
        path='/ITAS/UserFlow/getBizKey.do'
        getBizKeyURL=_globalVariables.BASEURL+path

        getBizKeyData={
            'axBizTaskId': 'undefined',
            'axPrefix': '',
            'axType':'UUID',
            'r': random.random()
        }
        getBizKeyResp=_globalVariables.SESSION.post(getBizKeyURL,getBizKeyData)
        BizKey=getBizKeyResp.text
        # endregion

        # region insert user information
        path = '/ITAS/UserFlow/start.do'
        query='axBizProcDefiId=ApexUSMCreateUserProcess&axBizkey='+BizKey+'&r='+str(random.random())+\
              '&axBizIsNew=true&axBizIsFlow=true&axBizFlowAction=submit&axBizEntityType=com.cacss.apex.web.entity.ApexUserLogin'
        startURL = _globalVariables.BASEURL + path+'?'+query

        startData = {
            'actionStatus': 'submit',
            'description': '',
            'email': userName+'@qq.com',
            'enableDate': '',
            'expiryDate': '',
            'firstName': '',
            'fontSize': '',
            'fullName': userName,
            'gender': '',
            'hidActionName': '',
            'isReadOnly': 'true',
            'lastLoginIp': '',
            'lastLoginTime': '',
            'lastName': '',
            'loginFailedNumber': '',
            'loginName': loginName,
            'middleName': '',
            'mobile': ''.join(random.sample(string.digits, 8)),
            'organization.sysGuid': self.getOrganiztionIDByName(organizationName),
            'orgUserStatus[0].0': '1',
            'otherName': ',,',
            'passwordAnswer': '',
            'passwordQuestion': '',
            'sysCreateDate': '',
            'sysCreateUser': '',
            'sysGuid': '',
            'sysId': '',
            'sysOwner': '',
            'sysRecycle': '',
            'sysUpdateDate': '',
            'sysUpdateUser': '',
            'userClassification': '',
            'userInfo.cityOfBirth': '',
            'userInfo.dateOfBirth': '',
            'userInfo.employeeNumber': '',
            'userInfo.ethnic': '',
            'userInfo.homeFax': '',
            'userInfo.homeTel': '',
            'userInfo.identityCard': ''.join(random.sample(string.digits, 8)),
            'userInfo.job': '',
            'userInfo.maritalStatus': '',
            'userInfo.nationality': '',
            'userInfo.officeLocation': '',
            'userInfo.photo': '',
            'userInfo.postalAddress': '',
            'userInfo.residentialAddress': '',
            'userInfo.signatureImage': '',
            'userInfo.sysGuid': '',
            'userLanguage': '',
            'userOrder': '',
            'userThemeId': '',
            'userType': '0',
        }
        startResp = _globalVariables.SESSION.post(startURL, startData)
        return startResp.text
        # endregion

    def iscreateUserBySysadminSucess(self, createUserBySysadminResp):
        '''
        creatUserByAdmin response
        :param creatUserByAdminResp:
        :return: True|False
        '''
        if 'true' in createUserBySysadminResp:
            logger.info('create user by system admin succuessfully:' + createUserBySysadminResp, also_console=True)
            return True
        else:
            logger.error('create user by system admin failed:' + createUserBySysadminResp)
            return False

    def createOrganization(self,organizationName):
        '''
        create new organization
        :param superOrganization: which organization you want to add in
        :param organizationName:  the add organization name
        :return: create organization name
        '''

        path='/ITAS/apexOrganization.insert.do'

        insertData={
            'address': '',
            'attendanceTel': '',
            'creatTime': '',
            'description': '',
            'email': 'ret@qq.com',
            'fax': '',
            'hidActionName': 'insert',
            'insideTel': '',
            'officeNo': '321',
            'organizationLevel': '',
            'organizationName': organizationName,
            'organizationStatus': '0',
            'otherName': '',
            'outsideTel': '',
            'parentId': '00000000-0000-0000-0000-000000000000',
            'post': '',
            'serialIndex': '',
            'sysGuid': '',
            'sysId': '',
            'sysRecycle': '0',
            'treeNodeExt': '',
            'treeNodePath': ''
        }


