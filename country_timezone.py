from pytz import country_timezones


timezone_country = {}

def myFunction():
    for countrycode in country_timezones:
        timezones = country_timezones[countrycode]
        for timezone in timezones:
            timezone_country[timezone] = countrycode
            print("countrycode " + countrycode)
            print("timezone " + timezone)
            
myFunction()

print(timezone_country['Europe/Zurich'])