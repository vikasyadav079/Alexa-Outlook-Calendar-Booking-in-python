
def tempVikas():
    cfg_dict = {}
    lst = []
    cfg_file = open('essconfig.cfg')
    for line in cfg_file:
        if '=' in line :
            cfg_dict[line.strip().split('=')[0]]=line.strip().split('=')[1]
        else :
            return ""
    cfg_file.close()
    
    allRoomNamesAlias = ["Room1Alias","Room2Alias","Room3Alias","Room4Alias","Room5Alias",]
    allRoomNamesAliasString=",".join(allRoomNamesAlias)
    print(allRoomNamesAliasString)
    
    
tempVikas()
