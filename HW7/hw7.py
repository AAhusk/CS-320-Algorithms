import pdb
# See assignment sheet for an explanation of finding the silhouette of a
#  set of buildings...
def silhouette(Buildings):
    return silhouetteAux(Buildings, 0, len(Buildings)-1)

#  Find the silhouette of Buildings[i..k]  using a divide-and-conquer algorithm
def silhouetteAux(Buildings, i, k):
    if (i == k):
        point1 = (Buildings[i][0], Buildings[i][1])
        point2 = (Buildings[i][2], 0)
        return [point1, point2]
    else:
        S1 = silhouetteAux(Buildings, i, k//2)
        S2 = silhouetteAux(Buildings, k//2+1, k)
        return mergeSilhouettes(S1, S2)

# Merge two silhouettes to get their joint silhouette
def mergeSilhouettes(S1, S2):
    count1, count2 = 0,0                               #this keeps track of which element we are at in the silhouette array
    lenS1 = len(S1); lenS2 = len(S2)
    i,j = 0,0                                          #this is the x-coordinate where the height changes for the element we are at in the silhouette array 
    top1, top2 = 0,0
    top = 0                                            #current top of the merged silhouette
    S = []
    while(count1<lenS1 and count2<lenS2):
        i = S1[count1][0]; j = S2[count2][0]; 
        if(i < j):                                      #top1 is changing
            oldTop1 = top1
            top1 = S1[count1][1]
            if(oldTop1 > top2):                         #if top1 was the higher than top2, the silhouette must change with a change in top1
                top = max(top1, top2)
                S.append((i, top))
                count1 += 1; continue
            else:                                       #else top1 was lower than top2
                if(top1 > top2):                        #the silhouette only changes if top1 rises above top2
                    top = top1
                    S.append((i, top))
                count1 += 1; continue
        elif(j < i):                                    #top2 is changing
            oldTop2 = top2
            top2 = S2[count2][1]
            if(oldTop2 > top1):                          #if top2 was the higher than top1, the silhouette must change
                top = max(top1, top2)
                S.append((j, top))
                count2 += 1; continue
            else:                                        #else top2 was lower than top1
                if(top2 > top1):                         #the silhouette only changes if top2 rises above top1
                    top = top2
                    S.append((j, top))
                count2 += 1; continue
        elif(i == j):                                    #top1 and top2 are changing in the same x-coordinate
            top1 = S1[count1][1]
            top2 = S2[count2][1]
            top = max(top1, top2)                        #the new top is the higher value between top1 and top2
            S.append(i, top)
            count1 += 1; count2 += 1; continue

    if(count1 == lenS1 and count2 == lenS2):
        return S
    
    else:
        countFinal = count1; topFinal = top1                 #assume silhouette 2 finished, and silhouette 1 still has points left
        SFinal = S1; lenFinal = lenS1
        if(count1 == lenS1):                                 #then silhouette 1 finished first, and there are still points left in silhouette 2
            countFinal = count2; topFinal = count2
            SFinal = S2; lenFinal = lenS2
        while(countFinal < lenFinal):
            i = SFinal[countFinal][0]
            topFinal = SFinal[countFinal][1]
            S.append((i, topFinal))
            countFinal+=1
            
        return S


#  See assignment sheet for an explanation of this problem about
#  typesetting text.  You may assume as a precondition that no
#  element of list 'W' is greater than 'pagesize'.
def typecost(Wordlengths, pagesize):
    WL = Wordlengths + [0]  # add a sentinal to end of Wordlengths
    T = [0] * len(WL)  # Base case of 0 words on end of T

    for i in range(len(T)-2, -1, -1):      #start at the second to last element
        lineSum = 0
        curLineCost = 0
        prevLineCosts = 0
        bestCost = 1000000                  #initialize bestCost as a very large number
        for w in range(i, len(T)-1):        #go from the current element through the second to last element
            wordLen = WL[w]
            if (lineSum + wordLen <= pagesize):
                lineSum += wordLen
                curLineCost = (pagesize - lineSum)**2 
            else:
                prevLineCosts += curLineCost
                curLineCost = (pagesize-wordLen)**2
                lineSum = wordLen

            curTotalCost = curLineCost + prevLineCosts + T[w+1]
            if (curTotalCost < bestCost):
                bestCost = curTotalCost
        T[i] = bestCost
    return T

#  This is the method that needs to reconstruct the typesetting from
#  the word lengths and the annotations S[], where S[i] gives the
#  index of the first word of the second line in an optimum typesetting
#  of Wordlengths[i, ..., len(Wordlengths[i]-1)]
def typeset(Wordlengths, T, pagesize):
    WL = Wordlengths + [0]
    Lines = []
    S = [0]*(len(T)-1)
    wordIndex = len(T)-1
    remainingChars = pagesize
    for t in range(len(T)-2, -1, -1):
        wordLength = WL[t]
        cost = T[t]
        if cost > T[t+1]:                     #a new line has been added
            charRemaining = pagesize
            for i in range(t, len(T)-1):       #find the index of the first word of the second line
                charRemaining -= WL[i]         #add a word to the current line to find out where the first line breaks to the second line
                if (charRemaining**2 + T[i+1] == cost):     #if the cost of the current line + the best cost of the previous lines = the best cost of the current subset of words
                    wordIndex = i+1                         #then the first word of the second line is the next word
                    remainingChars = charRemaining
                    break
        else:                                 #no new line is added
            lineCost = (remainingChars-wordLength)**2
            if(remainingChars < wordLength or (lineCost+T[wordIndex] != cost)):     #other words must change lines
                for prevWordIndex in range(wordIndex-1, t, -1):
                    remainingChars += WL[prevWordIndex]
                    if((remainingChars-wordLength)**2 + T[prevWordIndex] == T[t]):
                        wordIndex = prevWordIndex
                        break
            else:
                remainingChars -= wordLength
        S[t] = wordIndex

    currentIndex = 0
    while(currentIndex < len(S)):
        currentLine = []
        linebreak = S[currentIndex]
        while(currentIndex < linebreak):
            currentLine.append(WL[currentIndex])
            currentIndex += 1
        Lines.append(currentLine)    

    return Lines

#  This reads in a file of buildings for the silhouette problem ...
def readBuildings(filename):
    buildingList = []
    fp = open(filename, 'r')
    for line in fp:
        left, top, right = [int(x) for x in line.split(' ')]
        buildingList.append((left, top, right))
    fp.close()
    return buildingList


if __name__ == '__main__':

    Buildings = [(3,3,9), (4,4,5), (6,5,11)]
    
    Silhouette = silhouette(Buildings)
    print ('\nFor these buildings: ', Buildings)
    print('\nThe silhouette is:  ', Silhouette)

    print ('\n-------------------------')

    W = [10,3,2,10,12,3,5,4,4]
    p = 15
    T = typecost(W,p)
    print ('\nFor typesetting with wordlengths ', W, ' and page size ', p,)
    print ('\nTypecost returns dynamic programming array:  ', T)
    Lines = typeset(W, T, p)
    print ('\nOptimal typesetting of these lines: ', Lines)
    
