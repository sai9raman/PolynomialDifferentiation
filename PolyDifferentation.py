#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Mon Feb 17 17:37:44 2020

@author: sairaman
"""

###################### CLASS DEFINITION ###########################

class term(object):
    """
    A class for defining a term of a polynomial which have two attributes:
        Coefficient: the coefficient of the term; e.g. for "-2x^5", it'll be -2
        Power: the exponent to which the variable (say) "x" is raised
    """
    def __init__(self, coef, power):
        
        self.coef = coef
        self.power = power
        
    def differentiate(self):
        
        """ A function that differentiates a given term and returns the deriv"""    
        if self.power ==0:
            return term(0,0)
        return term(self.power*self.coef,self.power-1)
    
    def integration(self):
        """ A function to integrate a given term"""
        
        if self.power == -1:
            raise ValueError
        return term(self.coef/(self.power+1),self.power+1)
    
    def __mul__(self,other):
        
        return term(self.coef*other.coef,self.power+other.power)
    
    def __str__(self):
        """ A function that returns a string format of the term provided"""    

        if self.power ==1:
            powstr = "x"
        elif self.power ==0:
            powstr = ""
        else:
            powstr = "x^"+str(self.power)
            
        if self.coef==1:
            if self.power==0:
                coefstr = "1"
            else:
                coefstr = ""
        else:
            coefstr = str(self.coef)
        
        return coefstr+powstr

###################################################################
# %% MAIN
    
def main():
          
    polyExp = input("Please input your univariate polynomial expression in x (cannot handle paranthesis): ")    
    
    polyExp2 = input("Please input your 2nd univariate polynomial expression in x (cannot handle paranthesis): ")    
    
    MultipliedTerm = convertToTerm(polyExp)*convertToTerm(polyExp2)
    
    print(MultipliedTerm)
    
#    testPolyDifferentiator()
    
#    diffPoly = PolynomialDifferentiator(polyExp)
#    print(diffPoly)
    
    
    
    
    
    
if __name__ == '__main__':
    main()
    
###################################################################

#%%  TEST SCRIPT 
    
def testPolyDifferentiator():
    
    testInput = ["x^2", "2x^3+9", "3", "", "1/2x", "-x^-2-3+6x+7x^3-2/4x^-8/4","3*x"]
    expectedOutput = ["2x", "6x^2", "", "", "0.5", "2x^-3+6+21x^2+x^-3.0","3"]

#    testInput = ["x^2"]
#    expectedOutput = ["2x"]
    
    failCase = []
    for i in range(len(testInput)): 
        
        tempOut = PolynomialDifferentiator(testInput[i])
        print(tempOut)
        if tempOut != expectedOutput[i]:
            failCase.append(testInput[i])
        else:
            continue
        
    if failCase == [] :
        print("All Tests Passed")
    else:
        print("Test failed for the following cases: ", failCase)
        
###################################################################

#%% CORE FUNCTION
        
def PolynomialDifferentiator(polyExpression) :
    
    if checkPolynomial(polyExpression) == False:
        print( "Error - Polynomial expression contains non-parseable characters")
        return
    
    polyExpression = polyExpression.replace(" ","")
    
    termsList = parsePoly(polyExpression)
        
    diffTermsList = []
    
    for temp in termsList:
        diffTermsList.append(temp.integration())
    
    fullDiffPoly = joinPolynomialTerms(diffTermsList)
    
    return fullDiffPoly

###################################################################

#%%    CHECKS INPUT 

def checkPolynomial(poly):
    
    """
    A Function to check the appropriateness the user input of a one variable polynomial 
    
    Input: Polynomial String
    Output: Boolean-  True if polynomial is appropriate 
    """
    
    allowedChars = [" ","*","+","-","/","x","^"]
    
    for elem in poly: 
        if elem in allowedChars or elem.isdigit()==True:
            continue
        else:
            return False
    
    poly2 = poly.replace(" ","")
    
    
    ## Checks for corner  cases of user mis-entry
    
    signs = ["*","+","-","/"]

    for i in range(len(poly2)-1):
        if poly2[i] in signs and poly2[i+1] in signs: # checks for e.g. +- / +* 
            return False 
        if poly2[i] in signs and poly2[i+1]=="^": # checks for e.g. +^, -^
            return False 
        if poly2[i] == 'x' and poly2[i+1].isdigit(): #checks for x3 or x4
            return False 
        if poly2[i] in ["*","/","^"] and poly2[i+1] == "x": #checks for *x or ^x
            return False 
    
    return True

###################################################################
    
#%% Parse the Polynomial 
    
def parsePoly(poly):
    
    """
    Break down a Polynomial String into a list term objects 
    
    Input: String
    Output: List of Terms(coef,power)
    
    """ 
    termStringList = []
    
    ######## Convert each term to a separate string and add it to a list ###### 
    
    modifiedPoly = poly
    modifiedPoly = modifiedPoly.replace("^+","^")
    modifiedPoly = modifiedPoly.replace("^-","^(neg)")
    modifiedPoly = modifiedPoly.replace("-","+(neg)") 

    modifiedSplits = modifiedPoly.split("+")
    
    for temp in modifiedSplits:
        if temp == '':
            continue
        temp2 = temp.replace("(neg)","-")
        temp2 = temp2.replace("^(neg)","^-")
        termStringList.append(temp2)
        
        
    ### Convert each String Term to a Poly Term ###
    
    termsList = []
    for temp in termStringList: 
        
        termsList.append(convertToTerm(temp))

    return termsList        

###################################################################   

# %% Converts String to Term to Object 

def convertToTerm(termStr):   
    
    """
    Convert a Term Object from a string form to a Term (class) form
    
    Input: String
    Output: Term(coef,power)
    
    """
    
    if "^" in termStr: 
        power = eval(termStr.split("^")[1])
        termStr = termStr.split("^")[0]
    
    elif "x" in termStr:
        power = 1
        termStr = termStr.replace("x","")
        
    else:
        power = 0
        
    termStr = termStr.replace("x","")
    
    if termStr == "" or termStr == "+":
        coeff = 1        
    elif termStr == '-':
        coeff = -1        
    else:           
        coeff = eval(termStr)
    
    return term(coeff,power)
            
###################################################################           
           
    
#%% join  string terms of a polynomial 
    
def joinPolynomialTerms(termsList):
    
    """
    Convert a list of Term Objects into a string representative of a Polynomial
    
    Input: List of Terms(coef,power)
    Output: String
    
    """ 
    
    fullPolynomialString = ''
    for temp in termsList: 
        if temp.coef>0 and fullPolynomialString!='':
            fullPolynomialString+="+"
        if temp.coef==0:
            continue
        
        fullPolynomialString+=temp.stringTerm()
        
    return fullPolynomialString
            
###################################################################