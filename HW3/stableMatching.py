# Programming assignment 1: Gale-Shapley algorithm
# coding=utf-8
import numpy as np


def generate_rand_data(n, file_name):
    """
    The function will generate n men and n women with names 1 to n. 
    It assignes a random preference list to each of the men;
    of all the men in order and stores them in the file with the
    given filename in the format described in comments to read_from_file().
    """

    Men_pref_list = []
    Women_pref_list = []

    for i in range(n):
        Ordered_list = [i+1 for i in range(n)]
        np.random.shuffle(Ordered_list)
        Men_pref_list.append(Ordered_list)
        Ordered_list = [i+1 for i in range(n)]
        np.random.shuffle(Ordered_list)
        Women_pref_list.append(Ordered_list)    
    with open(file_name, "w") as f: 
        f.write(str(n)+'\n')
        for Lst in Men_pref_list:
            new_line = ""
            for elem in Lst:
                new_line += str(elem)+' '
            f.write(new_line[:-1]+'\n')
        f.write(' \n')
        for Lst in Women_pref_list:
            new_line = ""
            for elem in Lst:
                new_line += str(elem)+' '
            f.write(new_line[:-1]+'\n')


def read_from_file(filename):
    """
    This function reads the input from a file that is easy to create with
      a text editor.

    The men and women are each denoted with an integer from 1 to n.

    The format of the file is as follows:
    The first line has a single integer, giving the number n of men and women
    On each of the next n lines is the preference list of a man, separated by
       spaces.  The first of these lines gives the preference list of man 1,
       the second for man 2, etc.
    The next line is empty
    One each of the next n lines is the preference list of a woman, separated
       by spaces.  The first of these gives the preference list of woman 1, etc.

    Example for n = 4:
    4
    3 1 4 2
    3 2 1 4
    1 4 2 3
    1 4 3 2
 
    1 4 3 2
    2 4 3 1
    3 2 1 4
    1 4 3 2
    """

    Men_pref_list = []
    Women_pref_list = []
    number = 0
    with open(filename) as f:
        Lines = f.readlines()
        number = int(Lines[0][:-1])
        for i in range(number):
            New_list = [int(elem) for elem in str(Lines[i+1][:-1]).split(" ")]
            Men_pref_list.append(New_list)
        for i in range(number+1,2*number+1,1):
            New_list = [int(elem) for elem in str(Lines[i+1][:-1]).split(" ")]
            Women_pref_list.append(New_list)

    return Men_pref_list, Women_pref_list
             

def compute_inv_pref_list(Pref_list): #CONFIRMED
    """
    The input is a list such that Pref_list[i-1][j-1] is the jth man
    in woman i's preference list.  That is, Pref_list[i-1] gives the
    obvious format for the preference list of woman i.

    The disadvantage of having each woman carry a preference list
    giving the men in descending order of preference is that it takes
    Theta(n) time in the worst case to determine whether a new suitor
    is higher in her preference list than her current fiance.  It is
    required to search her list to find the positions of the fiance
    and the new suitor to see who is higher.

    Since there are Theta(n^2) proposals in the worst case, that would cause 
    the stable matching algorithm to run in Theta(n^3) time.

    A better representation is Inv_pref_list, where Inv_pref_list[i-1][j-1]
    holds the position of man j in woman i's preference list.  This is
    the "inverse function" of the on mapping positions in the list to men.  
    It maps men to positions in the list.  To compare two men, j and k, to 
    see who is higher in i's list, just compare Inv_pref_list[i-1][j-1]
    and Inv_pref_list[i-1][k-1] to see which is a lower number.

    For this method, fill in code that computes Inv_pref_list from
    Pref_list in O(n^2) time.  There are Theta(n^2) elements in Pref_list,
    so this requires that you spend only constant time per entry.
    """
    Inv_pref_list = []
    Woman = 0
    for WomanList in Pref_list:
        Woman_inv_pref_list = [None]*len(WomanList)
        ManRank = 1
        for Man in Pref_list[Woman]:
            Woman_inv_pref_list[Man-1] = ManRank
            ManRank+=1
        Inv_pref_list.append(Woman_inv_pref_list)
        Woman+=1
    return Inv_pref_list


def propose(new_man, woman, Inv_women_pref_list, Fiance):
    """
    This function simulates the proposal of a man to a woman.
    The new_man proposes to woman and if the woman is single
    or new_man ranks higher than her current match, he gets
    paired. This function has to return a tuple where the first
    element is the response of the proposal and the second 
    element is the man that has remained (or become) single 
    as the result of this proposal.

    Fiance is a Python list where Fiance[i-1] is the fiancé of
    woman i, or 0 if i is single.
    """
    
    # FILL IN CODE HERE
    Current_fiance = Fiance[woman-1]
    if (Current_fiance == 0):
        return True, None
    if (Inv_women_pref_list[woman-1][new_man-1] < Inv_women_pref_list[woman-1][Current_fiance-1]):
        return True, Current_fiance
    else:
        return False, new_man

def make_stack_of_men(Men_pref_list): #CONFIRMED
    """
    This function creates a stack that contains all
    the men. You can use a python list to implement a stack.
    For a tutorial on this, see the Python 3 tutorial at
    https://docs.python.org/3/tutorial/, Section 5.1.1.
    """

    # FILL IN CODE HERE 
    Stack = []
    i=1
    for man in Men_pref_list:
        Stack.append(i)
        i+=1

    return Stack



def Gale_Shapley(Men_pref_list, Women_pref_list):
    """
    This is the main Gale-Shapley method.  The inputs are two python
    lists.  Men_pref_list[i-1][j-1] gives the jth highest woman in man i's list.
    woman_pref_list[i-1][j-1] gives the jth highest man in woman i's list.

    What must be returned is a list of ordered pairs giving the stable
    set of marriages.  For consistency with the book's notation, list the man
    first in each pair.  A typical returned list for n = 4 is this:
    [(1, 1), (3, 2), (2, 3), (4, 4)], indicating that man 1 is married to woman
    1, man 3 is married to woman 2, etc.

    Store the single men in a stack created by make_stack_of_men().
    To find a single man to make a proposal, pop the stack.  When
    a man gets rejected, push him.

    Make a list Start_position[], where Start_position[i-1] gives
    the position of the first woman in man i's list that hasn't rejected
    him.  
    """    

    # FILL IN CODE HERE
    Single_Men = make_stack_of_men(Men_pref_list)
    Start_position = [1]*len(Men_pref_list)
    NumberOfMen = len(Single_Men)
    
    Inv_women_pref_list = compute_inv_pref_list(Women_pref_list)
    Fiances = [0]*len(Men_pref_list)
    while (len(Single_Men) > 0):
        Man = Single_Men.pop()
        nextPreference = Start_position[Man-1]
        next_eligible_woman = Men_pref_list[Man-1][nextPreference-1]
        response, singleMan = propose(Man, next_eligible_woman, Inv_women_pref_list, Fiances)
        
        if(response and singleMan == None): #This means next_eligible_woman was single and accepts man's proposal automatically
            Fiances[next_eligible_woman-1] = Man #next_eligible_woman is engaged to man
                
        elif(response and singleMan != None): #This means next_eligible_woman broke up with her Fiance, Fiances[j-1], and accepted man's proposal
            previousFiance = Fiances[next_eligible_woman-1] #previousFiance who was broken up with
            Start_position[previousFiance-1] += 1 #previousFiance moves down his preference list by one woman
            Fiances[next_eligible_woman-1] = Man #next_eligible_woman is now engaged to man
            Single_Men.append(previousFiance)

        else: #This means next_eligible_woman rejected man, and is still engaged to Fiance[j-1]
            Start_position[Man-1] += 1 #Man moves down his preference list by one woman
            Single_Men.append(Man)
   
    Marriages = []
    Married_woman = 1
    for Married_man in Fiances:
        Marriages.append((Married_man, Married_woman))
        Married_woman+=1
    return Marriages
    
def checkStability(Men_pref_list, Women_pref_list, Matching):
    '''
    This method checks the stability of a matching.  The first
    argument is a list where Men_pref_list[i-1][j-1] gives the
    jth woman in man i's preference list.  The second argument
    is similar, but for women's preferences.  Matching is an
    array of two-tuples, giving the matching.  

    If the matching has an instability, the method returns
    a triple (False, (m1,w1),(m2,w2)), where m1 prefers w2 to w1
    and w2 prefers m1 to m1.  If the matching is stable, it
    returns a triple (True, (0,0), (0,0)).
    '''
    n = len(Men_pref_list)

    # Compute the inverses of the preference list mappings for men, women
    Inv_men_pref_list = compute_inv_pref_list(Men_pref_list)
    Inv_women_pref_list = compute_inv_pref_list(Women_pref_list)

    # For each marriage, Marriage1...
    for i in range(n):
        Marriage1 = Matching[i]
        m1 = Marriage1[0]
        w1 = Marriage1[1]

        # m1's and m2's rankings of each other
        m1SpousePosition = Inv_men_pref_list[m1-1][w1-1]
        w1SpousePosition = Inv_women_pref_list[w1-1][m1-1]

        # For each later marriage in the list, Marriage2 ...
        for j in range(i+1,n):
            Marriage2 = Matching[j]
            m2 = Marriage2[0]
            w2 = Marriage2[1]

            # m2, m2's rankings of each other
            m2SpousePosition = Inv_men_pref_list[m2-1][w2-1]
            w2SpousePosition = Inv_women_pref_list[w2-1][m2-1]

            # If m1, w2 prefer each other to their spouses ...
            if m1SpousePosition > Inv_men_pref_list[m1-1][w2-1] and w2SpousePosition > Inv_women_pref_list[w2-1][m1-1]:
                return False, Marriage1, Marriage2 

            # If m2, w1 prefer each other to their spouses ...
            if m2SpousePosition > Inv_men_pref_list[m2-1][w1-1] and w1SpousePosition > Inv_women_pref_list[w1-1][m2-1]:
                return False, Marriage2, Marriage1

    #  If no instabilities have been discovered ...
    return True, (0,0), (0,0)

if __name__ == "__main__":
    
    """Men_pref_list, Women_pref_list = read_from_file("TestData")
    Inv_men_pref_list = compute_inv_pref_list(Men_pref_list)
    Inv_women_pref_list = compute_inv_pref_list(Women_pref_list)
    for woman_list in Women_pref_list:
        print(woman_list)
    print('\n')
    for inv_woman_list in Inv_women_pref_list:
        print(inv_woman_list)
    print('\n')
    Fiances = [0, 4, 0, 0, 0]
    Response, SingleMan = propose(2, 2, Inv_women_pref_list, Fiances)
    print(Response)
    print(SingleMan) """

    debug = True 
    filename = input ("\n\nName of file to read data from: ")

    
    """You can uncomment the following statement if you want to generate a random
    instance.  The first paramater tells how large n should be.
    This is not very useful for debugging, where you want to work
    with the same example each time, but it is useful for checking
    on the efficiency of your solution.  Our solution takes a couple
    of seconds to run on an instance where n = 1000.  If yours
    takes a long time on an instance of this size, it's a strong indication 
    that you haven't gotten an O(n^2) time bound."""
    
    generate_rand_data(10, filename)
   
    Men_pref_list, Women_pref_list = read_from_file(filename)

    if debug:
        print("men: ", Men_pref_list)
        print("women: ", Women_pref_list)

    print('\n')
    Man_Stack = make_stack_of_men(Men_pref_list)
    for man in Man_Stack:
        print(man)
    
    Stable_matching = Gale_Shapley(Men_pref_list, Women_pref_list)
    print(Stable_matching)

    #  The following can be uncommented when you get it working to
    #   see whether your returned solutions are stable.
    Check = checkStability(Men_pref_list, Women_pref_list, Stable_matching)
    
    if Check[0]:
        print ("\n\nThis matching is stable!")
    else:
        print ("\n\nInstability in following marriages!: ", Check[1], Check[2])
