
def generate_message():
    CRLF="\r\n"
    generate_contents = ""
    generate_contents+="PRODID:-//Microsoft Corporation//Outlook 16.0 MIMEDIR//EN"+CRLF
    generate_contents+="VERSION:2.0"+CRLF
    generate_contents+="METHOD:REQUEST"+CRLF
    generate_contents+="X-MS-OLK-FORCEINSPECTOROPEN:TRUE"+CRLF
    generate_contents+="BEGIN:VTIMEZONE"+CRLF
    generate_contents+="TZID:India Standard Time"+CRLF
    generate_contents+="BEGIN:STANDARD"+CRLF
    generate_contents+="DTSTART:16010101T000000"+CRLF
    generate_contents+="TZOFFSETFROM:+0530"+CRLF
    generate_contents+="TZOFFSETTO:+0530"+CRLF
    generate_contents+="END:STANDARD"+CRLF
    generate_contents+="END:VTIMEZONE"+CRLF
    generate_contents+="BEGIN:VEVENT"+CRLF
    generate_contents+="ATTENDEE;CN=^Ind_Magarpatta_T6_AU_Senate House_Small_Meeting_Room;CUTYPE=RESOURCE;ROLE=NON-PARTICIPANT;RSVP=TRUE:mailto:towervi_au_senate@amdocs.com"+CRLF
    generate_contents+="ATTENDEE;CN=Pankaj Chaudhary;RSVP=TRUE:mailto:Pankaj.Chaudhary@amdocs.com"+CRLF
    generate_contents+="CLASS:PUBLIC"+CRLF
    generate_contents+="CREATED:20180531T053923Z"+CRLF
    generate_contents+="DESCRIPTION:Hi All\, Kindly join the meeting on time \n\n \n\nVikasYadavAgenda\n\n \n\nThanks \n\nVikas Yadav\n\n"+CRLF
    generate_contents+="DTEND;TZID=\"India Standard Time\":20180704T113000"+CRLF
    generate_contents+="DTSTAMP:20180531T053737Z"+CRLF
    generate_contents+="DTSTART;TZID=\"India Standard Time\":20180704T110000"+CRLF
    generate_contents+="LAST-MODIFIED:20180531T053923Z"+CRLF
    generate_contents+="LOCATION:^Ind_Magarpatta_T6_AU_Senate House_Small_Meeting_Room"+CRLF
    generate_contents+="ORGANIZER;CN=\"Vikas Yadav\":mailto:Vikas.Yadav@amdocs.com"+CRLF
    generate_contents+="PRIORITY:5"+CRLF
    generate_contents+="RESOURCES:^Ind_Magarpatta_T6_AU_ Colosseum_Big_Meeting_Room (VC),^Ind_Magarpatta_T6_BU_ Saphire_Big_Meeting_Room (VC),^Ind_Magarpatta_T6_Cafetaria,^Ind_Magarpatta_T6_Daffodil_Meeting_Room (VC),^Ind_Magarpatta_T6_Nirvana_Meeting Room (VC),^Ind_Magarpatta_T6_Tulip_Meeting_Room(VC)"+CRLF
    generate_contents+="SEQUENCE:0"+CRLF
    generate_contents+="SUMMARY;LANGUAGE=en-us:Alexa Test. Cancel in sometime"+CRLF
    generate_contents+="TRANSP:OPAQUE"+CRLF
    generate_contents+="UID:040000008200E00074C5B7101A82E00800000000703FC36ECDF8D301000000000000000010000000AB63908CFB151A4BB215A64723BAC267"+CRLF
    generate_contents+="X-ALT-DESC;FMTTYPE=text/html:"+CRLF
    generate_contents+="X-MICROSOFT-CDO-BUSYSTATUS:BUSY"+CRLF
    generate_contents+="X-MICROSOFT-CDO-IMPORTANCE:1"+CRLF
    generate_contents+="X-MICROSOFT-DISALLOW-COUNTER:FALSE"+CRLF
    generate_contents+="X-MS-OLK-APPTSEQTIME:20180531T053737Z"+CRLF
    generate_contents+="X-MS-OLK-AUTOFILLLOCATION:TRUE"+CRLF
    generate_contents+="X-MS-OLK-CONFTYPE:0"+CRLF
    generate_contents+="EGIN:VALARM"+CRLF
    generate_contents+="TRIGGER:-PT15M"+CRLF
    generate_contents+="ACTION:DISPLAY"+CRLF
    generate_contents+="DESCRIPTION:Reminder"+CRLF
    generate_contents+="END:VALARM"+CRLF
    generate_contents+="END:VEVENT"+CRLF
    generate_contents+="END:VCALENDAR"+CRLF
    
    print(generate_contents)
    
generate_message()