# buyLotsOfFruit.py
# -----------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
To run this script, type

  python buyLotsOfFruit.py

Once you have correctly implemented the buyLotsOfFruit function,
the script should produce the output:

Cost of [('apples', 2.0), ('pears', 3.0), ('limes', 4.0)] is 12.25
"""

fruitPrices = {'apples':2.00, 'oranges': 1.50, 'pears': 1.75,
              'limes':0.75, 'strawberries':1.00}

def buyLotsOfFruit(orderList):
    """
        orderList: List of (fruit, numPounds) tuples

    Returns cost of order
    """
    #create a variable cost which stores the cost for the fruits given in the list
    cost = 0.0
    #loop for each tuple in the list passes as an argument
    for fruit, numPounds in orderList:
        #if the fruit exists in the fruitPrices, then its cost should be computed and added to cost variable
        #if the fruit does not exist in the fruitPrices, it should print and error and return none.
        if fruitPrices.has_key(fruit):
            cost += fruitPrices[fruit] * numPounds
        else :
            print 'ERROR: fruit does not exist in fruitPrices'
            return None
    print 'The cost of the order is %s' %(cost)
    return cost

# Main Method
if __name__ == '__main__':
    "This code runs when you invoke the script from the command line"
    orderList = [ ('apples', 2.0), ('pears', 3.0), ('limes', 4.0) ]
    print 'Cost of', orderList, 'is', buyLotsOfFruit(orderList)
