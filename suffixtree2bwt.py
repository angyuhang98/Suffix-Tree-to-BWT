"""
Reference: geeksforgeeks
1. https://www.geeksforgeeks.org/ukkonens-suffix-tree-construction-part-1/
2. https://www.geeksforgeeks.org/ukkonens-suffix-tree-construction-part-2/
3. https://www.geeksforgeeks.org/ukkonens-suffix-tree-construction-part-3/
4. https://www.geeksforgeeks.org/ukkonens-suffix-tree-construction-part-4/
5. https://www.geeksforgeeks.org/ukkonens-suffix-tree-construction-part-5/
6. https://www.geeksforgeeks.org/ukkonens-suffix-tree-construction-part-6/

NOTE: I understood the ukkonen's suffix tree construction algorithm through geeksforgeeks. I found it easier than the lecture slides.
The alg. is explained step by step and thats how i was trying my implementation as well. I have not plagerised or copied anything, this is my own attempt for the implementation so please do consider this. However during debugging, i had to look at the code to check where my code is giving problems and then correct my approach.
"""

import sys
class Node:
    def __init__(self):
        self.arr = [None] * 256 #array of characters size, storing all the children nodes of current nodes
        self.suffixIndex = None #for internal nodes its going to be -1 otherwise non-negatives for leaves and will give index of suffix for the path from root to this leaf.
        self.start = None #store the edge label details from parent node
        self.end = None #store the edge label details of current node.
        self.suffixLink = None #points to the other node where current node should point via suffix link


def new(start, end=None, leaf=False):
    node = Node()
    node.suffixLink = root #for root node suffix link = None, as for internal nodes, suffix link = root at first but may change in the following extensions
    node.start = start
    node.end = end
    node.suffixIndex = -1  #set to -1 by default but changes for leaves at the end of all phases
    node.leaf = leaf
    return node



def suffixApply(current, labelHeight):
    #we just want to label the leaves not the internal nodes
    leaf = 1
    for node in current.arr:
        if node:
            leaf = 0
            if node.leaf:
                node.end = END
            suffixApply(node, ((node.end - node.start + 1) + labelHeight))
    if leaf == 1:  # takes care of all the leaf
        current.suffixIndex = len(s) - labelHeight



def suffixArray():
    idx = 0
    array = []
    skips(root, idx, array)
    return array


def skips(n, idx, array):
    if n.suffixIndex == -1:  #If it's an internal node
        for node in n.arr:
            if node:
                skips(node, idx, array)
    #If it is Leaf node
    elif n.suffixIndex > -1:
        idx += 1
        array.append(n.suffixIndex)



#active point consists of 3 elems: Active node, active edge, active length
root = None
previous = None #points to the new internal node whose suffix link will be set maybe a new suffix link (not root) in the next extension of same phase
aN = None
aE = -1 #the 'ord' of character, not the character itself
aL = 0
remain = 0  #indicates how many suffixes are yet to be added in tree
tmpEnd = None
size = -1  # Length of input string
leaf = False



#s = "suffix_trees_and_bwt_are_related$"
#'stringfile.txt' = sys.argv[1]
#outFile = sys.argv[2]
with open('stringfile.txt', 'r') as i:
    s = i.read().replace('\n','')


phases = len(s)


root = new(-1, -1, leaf) #Root is a special node, with no parent and so it’s start and end will be -1, for all other nodes, start and end indices will be non-negative.
aN = root #First activeNode will be root
for pos in range(phases): #for number of phases

    #increment END and all leaf edge end indices will point to END

    #takes care of extending all leaves created so far in tree
    END = pos


    #Increment remaining suffix count to keep track of how many suffixes are yet to be added
    remain += 1 #to track how many extensions are yet to be performed explicitly in any phase (after trick 3 is performed)

    #when starting a new phase, previous is set to None which indicates that there is no internal node waiting for its suffix link reset in current phase
    previous = None

    #Add all suffixes (yet to be added) one by one in tree
    while remain > 0: #for extensions left

        #Active Point Change for active length zero(APCFALZ).If activeLength is ZERO, set activeEdge to the current character being processed.
        if aL == 0:
            aE = pos

        #Check if there is an edge going out from activeNode for the activeEdge.

        #if character is present in the array, walk
        if aN.arr[ord(s[aE])] is not None:

            #If current character being added in tree is seen before, then phase i will complete early (as soon as Extension Rule 3 applies) without going through all i extensions


            #Get the next node at the end of edge starting with active Edge
            post = aN.arr[ord(s[aE])]


            #if the node is a leaf,
            if post.leaf:
                post.end = END #set it's end to END
            eL = post.end - post.start + 1 #calculate the length of the edg


            #No walk down needed if activeLength < edgeLength.
            if aL < eL:
                pass
            else: #Active Point Change for walk down.(The trick 1 – skip/count)
                aE = aE + eL #adjust active edge accordingly to represent the same active Point
                aL = aL - eL #adjust active length accordingly to represent the same active Point
                aN = post #set the next internal node as the active Node
                continue


            #Extension Rule 3 (current character being processed is already on the edge)
            #Check if the current character of s is already present after the active Point. If yes, no more processing (rule 3)
            if s[post.start + aL] == s[pos]:
                # Active point change for extension rule 3 (APCFER3) tell us to increment the active length and STOP all further processing in this phase and move on to next phase
                aL += 1
                #If a newly created node waiting for it's suffix link to be set
                if previous != None and aN != root:
                    #then set suffix link of that waiting node to curent active node
                    previous.suffixLink = aN
                    previous = None
                break


            #Extension Rule 2(a new leaf edge and a new internal node is created): when Active Point is in the middle of an edge but the current character being processed isnt on the edge,
            #we add a new internal node and a new leaf edge going out of that new node
            tmpEnd = post.start + aL - 1 #calculate where the end of where to split
            internal = new(post.start, tmpEnd) #new internal node
            aN.arr[ord(s[aE])] = internal #add the intenal node to the array


            internal.arr[ord(s[pos])] = new(pos, leaf=True) #New leaf coming out of new internal node
            post.start = post.start+ aL
            internal.arr[ord(s[post.start])] = post

            #New internal node here so if theres any internal node created in last extensions of same phase,
            #which is still waiting for its suffix link reset, we'll do it now
            if previous == None:
                pass
            else:
                previous.suffixLink = internal #previous suffixLink points to current newly created internal node
            previous = internal


        else: #the character isnt present

            #Extension Rule 2: A new leaf edge gets created
            aN.arr[ord(s[aE])] = new(pos, leaf=True)

            #Rule 2 creates a new leaf edge (And may also create new internal node, if the path label ends in between an edge)

            #if there is any internal node waiting for it's suffix link to get reset
            if previous is not None:
                #point the suffix link from that last internal node to current activeNode
                previous.suffixLink = aN
                #set previous to None indicating no more node waiting for suffix link reset.
                previous = None


        #Once extension is performed, decrement remain
        remain -= 1

        #if remain is 0, this tells that all suffixes supposed to be added in tree, are added explicitly and present in tree.
        #else: at the end of any phase, that tells that suffixes  are in the tree implicitly but not explicitly because of rule3
        #cause we stopped early



        #activePoint change for extension rule 2 (APCFER2):
        #Case 1 (APCFER2C1): If activeNode is root and activeLength is greater than ZERO, then decrement the activeLength by 1
        # and activeEdge will be set “S[i – remainingSuffixCount + 1]” where i is current phase number
        if aN == root and aL > 0:  #activePoint change for extension rule 2:Case 1 (APCFER2C1)
            aL -= 1 #because activePoint gets closer to root by 1 after every extension
            aE = pos - remain + 1 #gets the active edge for extension


        #Case 2 (APCFER2C2): If activeNode is not root, then follow the suffix link from current activeNode.
        # The new node (which can be root node or another internal node) pointed by suffix link will be the activeNode for next extension.
        # No change in activeLength and activeEdge

        #"activePoint gets closer to root by length 1 after every extension”,
        # this reduction in length will happen above the node s(v) but below s(v), no change at all.
        # So when activeNode is not root in current extension, then for next extension,
        # only activeNode changes (No change in activeEdge and active Length).
        if aN != root:  # APCFER2C2
            aN = aN.suffixLink




labelHeight = 0
suffixApply(root, labelHeight)
d=suffixArray()

bwt = ''
lol = []

for i in range(len(s)):
    lol.append(d[i] - 1)

for j in range(len(s)):
    bwt += s[lol[j]]


file = open('output_bwt.txt', 'w')
file.write(str(s) + str(bwt)+"\n")
file.close()
