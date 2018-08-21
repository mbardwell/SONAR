import time

mylist = []; hydroA = []; hydroB = []; hydroC = []
def intoHydrophones(filename):
    with open(filename, 'r') as f:
        for line in f:
            # print line #debug
            line = line.strip('\n')
            line = line.strip('\xef\xbb\xbf') # comes with .csv for some reason
            mylist = line.split(",")
            hydroA.append(int(mylist[0]))
            hydroB.append(int(mylist[1]))
            hydroC.append(int(mylist[2]))
        # print(hydroA, hydroB, hydroC) # debug
    f.close()

def nopingIndices(hydrophone):
    list = []
    pinglist = []
    nopinglist = [] # list of indices where there is no ping
    j = 0; resetflag = 1
    for i in hydrophone:
        if (1500 < i < 2500):
            nopinglist.append(j)
        j = j + 1
    # print (nopinglist, pinglist)
    lastvalue = 0
    for i in nopinglist:
        if (i - lastvalue > 5):
            list.append(i)
        lastvalue = i
    for i in list:
        nopinglist.remove(i)
    # print(nopinglist) #debug
    lastvalue = -6
    for i in nopinglist:
        if (i - lastvalue > 100):
            pinglist.append(lastvalue)
            pinglist.append(i)
        lastvalue = i
    # print(list) #debug
    return pinglist

def findPingsSeparated(pinglist, hydrophone):
    pingseperated = []
    for i in range(0,len(pinglist),2):
        pingseperated.append(hydrophone[pinglist[i]:pinglist[i+1]])
    return pingseperated

def interleavePings(A, B, C):
    list = []
    for i in range(0,min(len(A), min(len(B), len(C)))):
        list.append("Ping Detected")
        for j in A[i]:
            list.append(j)
        list.append('')
        for j in B[i]:
            list.append(j)
        list.append('')
        for j in C[i]:
            list.append(j)
        list.append('')
    return list


def printtoFile(fs, pings, filename):
    with open(filename, 'w') as file:
        file.write(str(fs)); file.write('\n')
        for i in pings:
            file.write(str(i))
            file.write('\n')
    file.close()

# def findPings(pinglist, hydrophone):
#     pings = []
#     for i in range(0,len(pinglist),2):
#         for j in hydrophone[pinglist[i]:pinglist[i+1]]:
#             pings.append(j)
#             pings.append('') # splits pings
#             # print(pings) #debug
#             return pings

def main():
    samplingrate = 500000
    intoHydrophones('C:/Users/Michael/Documents/au_sonar/scripts/tofile_class/rawdata1.csv')
    listA = nopingIndices(hydroA)
    listB = nopingIndices(hydroB)
    listC = nopingIndices(hydroC)
    A = findPingsSeparated(listA, hydroA)
    B = findPingsSeparated(listB, hydroB)
    C = findPingsSeparated(listB, hydroC)
    final = interleavePings(A, B, C)
    printtoFile(samplingrate, final, 'C:/Users/Michael/Documents/au_sonar/scripts/tofile_class/processeddata.txt')

main()
