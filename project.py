import pandas as pd
import numpy as np


def calculate_support (data , combinations_arr ,support):
    temp = set()
    last_combs = []
    for comb in combinations_arr:
        and_temp = np.array([True]*5822)
        for i in range (len(comb)):
            attr = int(comb[i][5:7])
            val = int(comb[i][12:])
            and_temp &= (data[attr] == val)

        count = len(data[and_temp])
        if(count > support *5822 /100):
            last_combs.append(comb)
            for i in range (len(comb)):
                temp.add(comb[i])

    next_segments = list(temp)
    next_segments.sort()
    return last_combs , next_segments



# The main function that prints all combinations of size r in 
# arr[] of size n. This function mainly uses combinationUtil() 
def getCombinations(arr, n, r): 
	
	# A temporary array to store all combination one by one 
    data = [0]*r
    combinations = []
	# get all combination using temprary array 'data[]' 
    combinationUtil(combinations , arr, data, 0, n - 1, 0, r)
    
    return combinations

# arr[] ---> Input Array 
# data[] ---> Temporary array to 
#		 store current combination 
# start & end ---> Staring and Ending 
#			 indexes in arr[] 
# index ---> Current index in data[] 
# r ---> Size of a combination 
# to be printed 
def combinationUtil(combinations , arr, data, start,end, index, r): 
						
	# Current combination is ready to be printed, print it 
    if (index == r):
        combinations.append([]) 
        for j in range(r): 
            
            combinations[-1].append(data[j]) 
        
        return

	# replace index with all possible elements. The condition "end-i+1 >= r-index" makes sure that 
	# including one element at index will make a combination with remaining elements at remaining positions 
    i = start
    while(i <= end and end - i + 1 >= r - index):
        same_atrr_flag = False
        if (index == 0):
            data[index] = arr[i]
            combinationUtil(combinations , arr, data, i + 1,end, index + 1, r)
        else:
            for k in range (index):
                if (data[k][5:7] == arr[i][5:7]):
                    same_atrr_flag = True
                    
            if (same_atrr_flag):
                i += 1
                continue
            
            data[index] = arr[i]
            combinationUtil(combinations , arr, data, i + 1,end, index + 1, r)
        i += 1 



def appriori_alg ( data ,support,the_confidence):
    segments = []

    
    for i in range(20,32):
        unique_segments = data[i].value_counts()
        temp = []
        for (value , count) in unique_segments.iteritems():
            if (count > support * 5822 / 100):
                temp.append(value)

        segments.append(temp)

    
    
    l1= []
    for i in range (12):
        for  j in range (len(segments[i])):
            
            l1.append("attr_"+str(20+i)+"_val_"+str(segments[i][j]))
    l1.sort()
    last_segments = l1
    
    for r in range (2,13):
        
        combinations = getCombinations(last_segments, len(last_segments),r)
        last_combinations , next_segments = calculate_support (data , combinations ,support)
        
        if (len(next_segments) == 0):
            
            break
        else:
            last_segments = next_segments
            combinations_for_rules = last_combinations

    confidence(combinations_for_rules,the_confidence)
   
    
        

def Left_combinations_rules(singlerule):
    rule_level = len(singlerule)
    TotalCombinations = list() 
    for i in range(rule_level-1):
        semiComb=list(getCombinations(singlerule,len(singlerule),i+1))
        for element in semiComb :
            TotalCombinations.append(element)
    
    return TotalCombinations

def LL_support(comb):
    and_temp = np.array([True]*5822)
    for i in range (len(comb)):
        attr = int(comb[i][5:7])
        val = int(comb[i][12:])
        and_temp &= (data[attr] == val)
    count = len(data[and_temp])
    support = count /5822
    return support


Attributes_Name=dict ([(20,"Entrepreneur"),        ( 21,"Farmer"),
                     (22,"Middle_management"),    (23,"Skilled_labourers"),
                    ( 24,"Unskilled_labourers"),  (25,"Social_class_A"),
                    ( 26,"Social_class_B1"),      (27,"Social_class_B2"),
                     (28,"Social_class_C"),       (29,"Social_class_D"),
                    ( 30,"Rented_house"),         (31,"Home_owners"),
                    ( 32,"1_car")])



def confidence(rules,confidence) :
    
    Table = list()
    dataframe = pd.DataFrame(columns = [ 'Lift','Leverage'])
    for singlerule in rules:
        support_All = LL_support(singlerule)
        willBeCount = np.array([True]*5822)
        for element in singlerule:
            attr= int(element[5:7])
            val = int(element[12:])
            willBeCount&= (data[attr] == val)
        TotalCount= len(data[willBeCount])
        ListOfCombinations = list(Left_combinations_rules(singlerule))
        
        for combine in ListOfCombinations :

           
            combine_set=set()
            willBeCount = np.array([True]*5822)
            
            for i in range(len(combine)):
                attr= int(combine[i][5:7])
                val = int(combine[i][12:])
                willBeCount&=(data[attr] == val)
            IfCount=len(data[willBeCount])
            if (TotalCount/IfCount)>= confidence :
                Left_support = LL_support(combine)
                rule_string=""
                for x in range(len(combine)):
                    combine_set.add(combine[x])
                    attr= int(combine[x][5:7])
                    val = int(combine[x][12:])
                    attr_name = Attributes_Name[attr]
                    if x==len(combine)-1:
                        rule_string= rule_string +attr_name+"_"+str(val)+ " -> "
                        
                    else:
                        rule_string= rule_string +attr_name+"_"+str(val) + ","
                        
                count=len(combine)
                Right_combination = list()
                for y in singlerule:
                    if y in combine_set :                        
                        continue  
                    else:
                        Right_combination.append(y)
                        count+=1
                        attr= int(y[5:7])
                        val = int(y[12:])
                        attr_name = Attributes_Name[attr]
                        if count == len(singlerule):
                            rule_string= rule_string +attr_name+"_"+str(val)
                           
                        else:
                            rule_string= rule_string +attr_name+"_"+str(val)+ ","
                            
                Right_support = LL_support(Right_combination)
                Lift =  support_All/(Left_support*Right_support)
                
                Leverage= support_All - ( Left_support * Right_support)
                
                temp = list([Lift,Leverage])
                Table.append(temp)
                dataframe.loc[rule_string]=temp
    
    print(dataframe)

# MAIN

data = pd.read_csv('ticdata2000.txt', sep="\t",header=None)
data = data.iloc[0: , 19:32]
data.columns += 1
appriori_alg (data , 20, 0.5)