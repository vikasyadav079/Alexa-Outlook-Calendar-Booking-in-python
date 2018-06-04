import os


def read_file():
    __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
    f= os.path.join(__location__, 'CalendarTemplate.cfg')   
    ics_content = open(f).read()
    replace_content = {}
    try :
        replace_content=ics_content.replace("TZID:" , "TZID:India Time Zone")
        replace_content=replace_content.replace("TZOFFSETFROM:" , "TZOFFSETFROM:+0530")
        replace_content=replace_content.replace("TZOFFSETTO:" , "TZOFFSETTo:+0530")
        replace_content=replace_content.replace("ATTENDEE;CN=" , "ATTENDEE;CN=\"^Ind_Magarpatta_T6_BU_ Saphire_Big_Meeting_Room (VC)\"")
        #append in string ATTENDEE;CN="^Ind_Magarpatta_T6_BU_ Saphire_Big_Meeting_Room (VC)";CUTYPE=RESOURCE;ROLE=NON-PARTICIPANT;RSVP=TRUE:mailto:TowerVIBUSaphire@Amdocs.com
        replace_content=replace_content.replace("CREATED:" , "CREATED:+0530")
        replace_content=replace_content.replace("DESCRIPTION:" , "DESCRIPTION:+0530")
        replace_content=replace_content.replace("DTSTAMP:" , "DTSTAMP:+0530")
        replace_content=replace_content.replace("LOCATION:" , "LOCATION:+0530")
        replace_content=replace_content.replace("RESOURCES:" , "RESOURCES:+0530")
        replace_content=replace_content.replace("X-MS-OLK-APPTSEQTIME:" , "X-MS-OLK-APPTSEQTIME:+0530")

    except Exception as e:
        print(e)
        
    f = open("Vikas.txt", "w+")
    f.write(replace_content)
    
    f.close()
        
read_file()