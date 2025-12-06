def importFolder(folderName: str):
    # TODO: implement this
    pass

def insertAgentClient(**kwargs):
    # TODO: implement this
    uid = kwargs['uid']
    username = kwargs['username']
    email = kwargs['email']
    card_number = kwargs['card_number']
    card_holder = kwargs['card_holder']
    expiration_date = kwargs['expiration_date']
    cvv = kwargs['cvv']
    zip = kwargs['zip']
    interests = kwargs['interests']
    pass

def addCustomizedModel(**kwargs):
    # TODO: implement this
    mid = kwargs['mid']
    bmid = kwargs['bmid']
    pass

def deleteBaseModel(**kwargs):
    # TODO: implement this
    bmid = kwargs['bmid']
    pass

def listInternetService(**kwargs):
    # TODO: implement this
    bmid = kwargs['bmid']
    pass

def countCustomizedModel(**kwargs):
    # TODO: implement this
    bmids = kwargs['bmids']
    bmid1, bmid2, bmid3 = bmids
    pass

def topNDurationConfig(**kwargs):
    # TODO: implement this
    uid = kwargs['uid']
    N = kwargs['N']
    pass

def listBaseModelKeyWord(**kwargs):
    # TODO: implement this
    keyword = kwargs['keyword']
    pass

def printNL2SQLresult(**kwargs):
    # TODO: implement this
    # OPTIONAL
    pass
