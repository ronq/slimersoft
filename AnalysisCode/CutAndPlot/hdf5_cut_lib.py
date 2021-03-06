import pandas
import string
import numpy
class hdf5_cut_lib:
    """ This is a class for applying complex cuts to HDF5 files 
    """
    #------------------------------------------------------------------------------------------------------------------------------------------
    def __init__(self,cutTable):
	    self.lowerLimits, self.variableNames, self.upperLimits, self.cutActions = self.ParseCutTable(cutTable)
	    return   
	#---------------------------------------------------------------------
    def ParseCutTable(self,cutTable):
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
    def ApplyCuts(self,inputTable):
        """ Apply cuts to an inputTable, and return the crunched table
        """ 
        allCutResults=[]
        for lowerLimit,variableName,upperLimit,cutAction in zip(self.lowerLimits, self.variableNames, self.upperLimits, self.cutActions):
            if inputTable.__contains__(variableName):                                                           # check if this cut applies to this DataFrame
                allCutResults.append(self.ComputeCut(inputTable,lowerLimit,variableName,upperLimit,cutAction))  # apply the cut
        if allCutResults:                                                                                       # if at least one cut variable was present in the DataFrame
            return inputTable[self.LogicalAnd(allCutResults)]                                                   # pass the DataFrame with all cuts applied
        else:
            return inputTable                                                                                   # pass the original, uncut             
    #----------------------------------------------------------------------- 
    def ComputeCut(self,df,lower_limit, variableName, upper_limit, cutAction):
	    """ Apply a cut to an DataFrame, and return a logical DataFrame
	    """
	    logicResult=(df[variableName] > lower_limit) & (df[variableName] < upper_limit)
	    if cutAction == "deselect":
	        logicResult = not logicResult
	    return logicResult
    #-----------------------------------------------------------------------
    def LogicalAnd(self,dataFrameArray):
        """ Compute the logical AND of an array of logical DataFrames
        """
        runningLogicFrame=dataFrameArray.pop()
        for element in dataFrameArray:
            runningLogicFrame*=element 
        return runningLogicFrame
    #-----------------------------------------------------------------------
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	       
