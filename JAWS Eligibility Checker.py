# Jstris Max APM Checker by HontNog. Designed for TAWS' temporary Jstris tournaments.
# WIP! NOT READY FOR USAGE IN TOURNAMENTS, SEEDING HAS NOT BEEN IMPLMENTED, THIS PROGRAM JUST CHECKS ELIGIBLITY.
# I suck at Python, if you have any way to improve this program or find bugs, send me a dm on Discord at @hontnog
try:
    import requests
except ImportError:
    print("The requests library is not installed. This is required for the program to run, please install it.")
    sys.exit(3)
import time # doing this as my dumbass doesnt know how to wait a response
import sys

# print (sys.argv)

def usage():
    print("Usage: JAWS Eligibility Checker.py <name> <apmCap>")
    print("APM cap will default to 50 if not specified.")
    sys.exit(1)

def getUserInfo(offset):
    url = "https://jstris.jezevec10.com/api/u/" + name + "/live/games?offset=" + str(offset)
    payload = {}
    headers= {}
    # print(url)

    userInformation = requests.request("GET", url, headers=headers, data = payload)
    return userInformation

def findAPM(damage, time): # Jstris' API does not contain API, so we've gotta do it the manual way
    return ((damage / time) * 60)

def createPlayerList(ign):
    apmList = []
    finished = False
    currentRequest = getUserInfo(0)
    count = 0
    while (len(apmList) % 50 == 0) and (not(finished)): # The API returns 50 results at a time
        if len(currentRequest.json()) == 0: # if the games list divides perfectly by 50
            break
        for i in range (min((len(currentRequest.json())), 50)):
            try:
                apmList.append(findAPM(currentRequest.json()[i]["attack"], currentRequest.json()[i]["gametime"]))
            except KeyError: # Appears to only get raised when the inputted name is invalid?
                print("Cannont find " + ign + ", have you entered their name correctly?")
                sys.exit(2)
        # print((count+1) * 50) debug line
        currentRequest = getUserInfo(((count+1)*50))
        count += 1
        time.sleep(0.5)
    # print(apmList) debug line
    return(apmList)

def getMaxAvg(attacksList):
    sumAPM = 0.0
    maxAPM = 0.0
    if len(attacksList) < 10:
        print(name + " is not eligible: They hasn't played 10 Jstris games so an average APM cannot be calculated.")
        sys.exit(0)
    for i in range (10): # Grab the first 10 games and sum them up.
        sumAPM += attacksList[i]
    for i in range (10, len(attacksList)):
        if (sumAPM / 10) >= apmCap:
            print (name + " is not eligible: They have exceeded a max APM of " + str(apmCap) + " at one point.")
            sys.exit(0)
        else:
            if (sumAPM / 10) > maxAPM:
                maxAPM = (sumAPM / 10)
            sumAPM -= attacksList[i - 10]
            sumAPM += attacksList[i]
    if (maxAPM) > ((apmCap * 9) /  10): # 90% close to the maxAPM req should be fine, though this may need tinkering
        print(name + " is eligble, however they have the following warning(s):")
        print(name + " has a max APM close to the APM cap (" + str(apmCap) + "APM), their max APM is " + str(maxAPM) + "APM")
        sys.exit(0)
    print(name + " is eligible.")
    sys.exit(0)
                
# main
if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()
    name = sys.argv[1]
    try:
        apmCap = float(sys.argv[2])
    except IndexError:
        apmCap = 50.0
    except ValueError:
        usage()
    apmStats = (createPlayerList(name))
    getMaxAvg(apmStats)
