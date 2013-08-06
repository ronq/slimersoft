import pandas
import string
import numpy
class hdf5_cut_lib:
    """ This is a class for applying complex cuts to HDF5 files 
    """
    #------------------------------------------------------------------------------------------------------------------------------------------
    def __init__(self,df,cutTable):
	    lowerLimit, variableName, upperLimit, cutAction = self.parseCutTable(cutTable)
	    logicIndex=self.computeCuts(df,lowerLimit, variableName, upperLimit, cutAction)
	    self.result=df[logicIndex]
	    return   
	#---------------------------------------------------------------------
    def parseCutTable(self,cutTable):
	    """ parse a cut table which should be in the format:
	            lower_limit of variable   variable name  upper_limit of variable  cutAction (select or deselect)
	    """
	    lower_limit=[]
	    variable_name=[]
	    upper_limit=[]
	    cut_action=[]
	    lines=cutTable.split('\n')
	    for line in lines:
	        line_variables = line.split()  
	        if len(line_variables)==4:      
	            lower_limit.append(float(line_variables[0]))
	            variable_name.append(line_variables[1])
	            upper_limit.append(float(line_variables[2]))
	            cut_action.append(line_variables[3])
	    return lower_limit, variable_name, upper_limit, cut_action
	#-----------------------------------------------------------------------
    def computeCuts(self,df,lower_limit, variableName, upper_limit, cutAction):
	    """
	    """
	    logicArrayList=[]        
	    for i in range(len(variableName)):
	        logicResult=(df[variableName[i]] > lower_limit[i]) and (df[variableName[i]] < upper_limit[i])
	        if cutAction[i] == "deselect":
	            logicResult = not logicResult 
	        print i, logicResult
	        logicArrayList.append(logicResult)
	    # now convert to a numpy array so we can use an efficient array manipulation
	    logicArray=numpy.array(logicArrayList)
	    # once this is done, I'll want to OR all the arrays together to form the final cut mask
	    #print logicArray
	    cutMask=numpy.any(logicArray,axis=1)
	    #print cutMask
	    return cutMask 
	#----------------------------------------------------------------------
	       
