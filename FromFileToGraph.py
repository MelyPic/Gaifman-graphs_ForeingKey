from itertools import islice
from matplotlib.pylab import hist, show
import networkx as nx
import matplotlib.pyplot as plt
import collections
from math import ceil,log,floor
import os



'''
Generate a plain matrix MyGraph, connected and disconnected nodes  
'''
def MatrixPlain(Matrix, MyGraph):
	for i in range(len(Matrix)):
		MyGraph.append([])
		LA.append([])
		for j in range(len(Matrix[i])):
			if i == j:
				MyGraph[i].append('None')
			else:
				if int(Matrix[i][j][0]) != 0:
					MyGraph[i].append('1')
				else:
					MyGraph[i].append('0')

'''
Given a Matrix, if the value of the element i,j is less than threshold, MyGraph will have 0 in this place, 1 if it is not
'''
def MatrixToShortestPathM(Matrix, MyGraph, threshold):
    for i in range(len(Matrix)):
        MyGraph.append([])
        LA.append([])
        for j in range(len(Matrix[i])):
            if i == j:
                MyGraph[i].append('None')
            elif int(Matrix[i][j][0]) >= threshold:
                # MyGraph[i].append('black')
                MyGraph[i].append('1')
                LA[i].append(j)
            else:
                MyGraph[i].append('0')
                # MyGraph[i].append('red')

'''
Generate a linear matrix MyGraph dividing the original matrix Matrix in intervals of size IntevalSize
'''
def MatrixLinear(Matrix, MyGraph, IntervalSize):
    for i in range(len(Matrix)):
        MyGraph.append([])
        LA.append([])
        for j in range(len(Matrix[i])):
            if i == j:
                MyGraph[i].append('None')            			
            #elif Matrix[i][j][0]!=0 and Matrix[i][j][0]< IntervalSize:
			#	Matrix[i][j][0] = 1					
            else:
                InInterval = ceil(int(Matrix[i][j][0]) / int(IntervalSize))  # funcion techo de la division
                MyGraph[i].append(str(int(InInterval)))
                if InInterval != 0:
                    LA[i].append(j)

'''
Generate a exponential matrix MyGraph dividing the original matrix Matrix in intervals of 2^k  
'''
def MatrixExponential(Matrix, MyGraph):
	for i in range(len(Matrix)):
		MyGraph.append([])
		LA.append([])
		for j in range(len(Matrix[i])):
			if i == j:
				MyGraph[i].append('None')
			else:
				v = int(Matrix[i][j][0])
				if v == 0:
					InInterval = 0
				else:
					InInterval = ceil(log(v+1,2))  # funcion techo del logaritmo
					#InInterval = floor(log(v,2))  # funcion piso del logaritmo
				MyGraph[i].append(str(int(InInterval)))
				if InInterval != 0:
					LA[i].append(j)
	
					


'''
Generate SPG, a matrix with the length of the shortest path between i,j elements in NG (a NetworkGraph).
'''
def gen_ShortestPathMatixFromNetxG(NG):
    SPG = []
    Nodes = NG.nodes()
    for i in range(len(Nodes)):
        SPG.append([])
        for j in range(len(Nodes)):
            SPG[i].append([nx.shortest_path_length(NG, source=i, target=j)])
    return SPG


'''
Returns how many independent paths are between two points (From,To) in a NG (NetworkxGraph)
'''
def EdgeIndependentPath(From, To):
    TP = []
    TotalPaths = nx.all_shortest_paths(NG, source=From, target=To)
    for i in TotalPaths:
        TP.append(i)
    IndependentPaths = []
    if len(TP) > 0:
        IndependentPaths.append(TP[0])
        k = 1
        while k < len(TP):
            ActualPath = TP[k]
            i = 0
            independent = True
            while i < len(IndependentPaths) and independent:
                path = IndependentPaths[i]
                if list(set(ActualPath[1:len(ActualPath) - 1]) & set(path[1:len(path) - 1])) != []:
                    independent = False
                else:
                    i += 1
            if independent:
                IndependentPaths.append(ActualPath)
            k += 1
    return len(IndependentPaths)


'''
Generate SPG, matrix with the number of independent paths between i,j on NG (NetworkGraph).
'''
def gen_MatrixQuantShortestPaths(NG):
    SPG = []
    Nodes = NG.nodes()
    for i in range(len(Nodes)):
        SPG.append([])
        for j in range(len(Nodes)):
            if i == j:
                SPG[i].append([0])
            else:
                SPG[i].append([EdgeIndependentPath(i, j)])
    return SPG


'''
Returns minimum path between two points in an adjacency matrix 
'''
def PathFromTo(i, j, path,LA):
    path += 1
    foundmin = False
    k = 0
    while k < len(LA[j]) and not foundmin:
        if LA[j][k] in LA[i]:
            foundmin = True
        else:
            k += 1
    if foundmin:
        return path
    else:
        paths = []
        for l in LA[j]:
            # #print l,'path', PathFromTo(i,l,path)
            paths.append(PathFromTo(i, l, path,LA))
        return min(paths)

'''
SPG, matrix with the shortest path between two points on an adjacency matrix
'''
def gen_ShortestPathGraph(MyGraph):
    SPG = []
    for i in range(len(MyGraph)):
        SPG.append([])
        for j in range(len(MyGraph[i])):
            if i == j:
                SPG[i].append([0])
            elif MyGraph[i][j] != '0':
                SPG[i].append([1])
            else:
                tpath = PathFromTo(i, j, 1,MyGraph)
                SPG[i].append([tpath])
    return SPG

'''
Shortest path of a graph with general values 
'''
def ShortestPathFromToGeneralMatrix(i,j,path,LA,found):
	path += 1
	#found = False
	k=0
	while k< len(LA[j]) and not found:
		if LA[j][k] in LA[i]:
			found = True
		else:
			k+=1
	if found:
		#print (path)
		return path
	else:
		paths = []
		for l in LA[j]:
			#print (l,'path', ShortestPathFromToGeneralMatrix(i,l,path,LA,found))
			paths.append(ShortestPathFromToGeneralMatrix(i, l, path,LA,found))
		if paths != []:
			#print (min(paths))
			#found = True
			return min(paths)
		else:
			#found = True
			return -1
		
'''
Auxiliar funtion to ShortestPathFromToGeneralMatrix
'''
def AdjMatrixStrings(Graph):
	LA= []
	for i in range(len(Graph)):
		LA.append([])
		for j in range(len(Graph)):
			if Graph[i][j] != '0' and Graph[i][j] != 'None':
				LA[i].append(j)
	return LA
		
'''
Auxiliar funtion to ShortestPathFromToGeneralMatrix
'''
def AdjMatrix(Graph):
	LA= []
	for i in range(len(Graph)):
		LA.append([])
		for j in range(len(Graph)):
			if Graph[i][j] != [0]:
				LA[i].append(j)
	return LA

'''
Return the matrix with the shortest path, uses AdjMatrix and ShortestPathFromToGeneralMatrix 
'''
def MatrixShortestPaths(Graph):
	MatrixShortestPaths=[]
	if type(Graph[0][0]) is list:
		LA = AdjMatrix(Graph)
	else:
		LA = AdjMatrixStrings(Graph)
	print(LA)
	for i in range(len(Graph)):
		MatrixShortestPaths.append([])
		for j in range(len(Graph)):
			if i == j :
				MatrixShortestPaths[i].append('None')
			elif LA[i] ==[]:
				MatrixShortestPaths[i].append('0')
			elif i in LA[j]:
				MatrixShortestPaths[i].append('1')
			else:	
				MatrixShortestPaths[i].append(str(ShortestPathFromToGeneralMatrix(i,j,0,LA,False)+1))
	return MatrixShortestPaths

'''
MyGraph 0 if the origina value is less than threshold and 1 o.w.
'''
def MatrixToMATPD(Matrix, MyGraph, threshold,upperthreshold):
	for i in range(len(Matrix)):
		MyGraph.append([])
		LA.append([])
		for j in range(len(Matrix[i])):
			if i == j:
				MyGraph[i].append('None')
			elif Matrix[i][j][0] > threshold:
				if upperthreshold == 0 or Matrix[i][j][0] < upperthreshold: 
					MyGraph[i].append('1')
					LA[i].append(j)
				else:
					MyGraph[i].append('0') 
			else:
				MyGraph[i].append('0')


'''
Used by TxtFile and ArffFile to construct the initial matrix
'''
def WhereStart(AttributeValueQuantity):
    WS = []
    for i in range(len(AttributeValueQuantity)):
        AuxIndex = 0
        j = i
        while j > 0:
            AuxIndex += AttributeValueQuantity[j - 1]
            j -= 1
        WS.append(AuxIndex)
    return WS


'''
From txt To Matrix
'''
def TxtFile(filename, GraphMatrix):
    # #print 'txt'
    fileop = open(filename, "r")
    AttributeValueQuantity = []
    AttributeNameList = []
    AttributeValueList = []
    TotalValues = 0

    AttributeNameList = fileop.readline().split()
    for i in range(len(AttributeNameList)):
        AttributeValueQuantity.append(0)
        AttributeValueList.append([])

    # line = fileop.readline()
    # while line != '':
    it = islice(fileop, 0, None)
    for line in it:
        AtributesLine = line.split()
        for i in range(len(AtributesLine)):
            if AtributesLine[i] not in AttributeValueList[i]:
                AttributeValueList[i].append(AtributesLine[i])
                AttributeValueQuantity[i] += 1
                TotalValues += 1
    fileop.close()

    # #print 'Total de atributos:', len(AttributeValueQuantity)
    # #print 'Atributos y valores:'
    # for i in range(len(AttributeNameList)):
    #	#print AttributeNameList[i],':',AttributeValueQuantity[i],',',AttributeValueList[i]

    # genera matriz con ceros
    for i in range(TotalValues):
        l = []
        for j in range(TotalValues):
            l.append([0])
        GraphMatrix.append(l)
    # for i in GraphMatrix:
    #	#print i

    # Para saber el indice donde comienzan los valores de cada atributo
    WS = WhereStart(AttributeValueQuantity)

    fileop = open(filename, "r")
    it = islice(fileop, 1, None)
    for line in it:
        # #print line
        LineElements = line.split(' ')
        i = 0
        while i < len(LineElements) - 1:
            if i == 0:
                row = AttributeValueList[0].index(
                    LineElements[0])  # Dentro de la lista de valores del atributo i, busca el indice del valor
            else:
                row = WS[i] + AttributeValueList[i].index(LineElements[i])
            for j in range(i + 1, len(LineElements)):
                if '\n' in LineElements[j]:
                    LineElements[j] = LineElements[j].replace('\n', '')
                # #print LineElements[j], ' in ',AttributeValueList[j]
                column = WS[j] + AttributeValueList[j].index(LineElements[j])
                # #print 'Agregar uno al elemento en:', row,column
                GraphMatrix[row][column][0] = int(GraphMatrix[row][column][0]) + 1
                GraphMatrix[column][row][0] = int(GraphMatrix[column][row][0]) + 1
            i += 1
    # #print 'Total values',TotalValues
    for i in range(len(AttributeNameList)):
        TotalAttributesValues.extend(AttributeValueList[i])
    fileop.close()

'''
From txt To Matrix each value is an attribute
'''
def TxtFile_ValueEqualAttribute(filename, GraphMatrix):
    # #print 'txt'
	fileop = open(filename, "r")
	AttributeValueQuantity = []
	AttributeNameList = []
	AttributeValueList = []
	TotalValues = 0
	it = islice(fileop,1,None)
	for AllLine in it:
		Line = AllLine.split(',')
		for i in Line:
			i = i.replace('\n','')
			if i:
				if i not in AttributeNameList:
					AttributeNameList.append(i)
					AttributeValueQuantity.append(1)
					AttributeValueList.append(i)
					TotalValues += 1
	fileop.close()
	#print len(AttributeNameList)
	#print AttributeValueList
	for i in range(TotalValues):
		l = []
		for j in range(TotalValues):
			l.append([0])
		GraphMatrix.append(l)
	#for i in GraphMatrix:
	#	#print i

     #Para saber el indice donde comienzan los valores de cada atributo
	WS = WhereStart(AttributeValueQuantity)
	fileop = open(filename, "r")
	it = islice(fileop, 1, None)
	for line in it:
		##print line
		LineElements = line.split(',')
		for i in range(len(LineElements)):
			LineElements[i] = LineElements[i].replace('\n','')
			if LineElements[i]:
				index_i = AttributeNameList.index(LineElements[i])
				for j in range(i+1,len(LineElements)):
					LineElements[j] = LineElements[j].replace('\n','')
					if LineElements[j]:
						index_j = AttributeNameList.index(LineElements[j])
						GraphMatrix[index_i][index_j][0]+=1
						GraphMatrix[index_j][index_i][0]+=1
						##print index_i, index_j
		#exit(1)
	#for i in range(len(AttributeNameList)):
	TotalAttributesValues.extend(AttributeValueList)
		#TotalAttributesValues.extend(AttributeValueList[i])
	fileop.close()

'''
From txt To Matrix, In the txt the attribute name is before the value
'''
def TxtFile_AttributeNameBeforeValue(filename, GraphMatrix):
	fileop = open(filename, "r")
	AttributeValueQuantity = []
	AttributeNameList = []
	AttributeValueList = []
	TotalValues = 0
	Line = fileop.readline().split(',')
	for i in range(len(Line)):
		#print Line[i]
		if '_' in Line[i]:
			PossibleAttribute = Line[i][:Line[i].index('_')].replace('\n','')
			#print 'possible attribute ', PossibleAttribute
			if PossibleAttribute:
				if PossibleAttribute not in AttributeNameList:
					AttributeNameList.append(PossibleAttribute)
					AttributeValueQuantity.append(0)
					AttributeValueList.append([])
	#print AttributeNameList
	it = islice (fileop,0,None)
	for AllLine in it:
		Line = AllLine.split(',')
		for i in range(len(Line)):
			if '_' in Line[i]:
				Attribute = Line[i][:Line[i].index('_')].replace('\n','')
				#ValueToBeAdded = Line[i][Line[i].index('_')+1:].replace('\n','').replace(' ','')
				ValueToBeAdded = Line[i].replace('\n','').replace(' ','')
				##print Attribute
				if ValueToBeAdded:
					IndexToBeAdded = AttributeNameList.index(Attribute)
					if ValueToBeAdded not in AttributeValueList[IndexToBeAdded]:
						AttributeValueList[IndexToBeAdded].append(ValueToBeAdded)
						AttributeValueQuantity[IndexToBeAdded]+=1
						TotalValues+=1
	#print len(AttributeValueList),'--', TotalValues
	fileop.close()
	#exit(1)
	
	# #print 'Total de atributos:', len(AttributeValueQuantity)
    # #print 'Atributos y valores:'
    # for i in range(len(AttributeNameList)):
    #	#print AttributeNameList[i],':',AttributeValueQuantity[i],',',AttributeValueList[i]

    # genera matriz con ceros
    
	
	for i in range(TotalValues):
		l = []
		for j in range(TotalValues):
			l.append([0])
		GraphMatrix.append(l)
	#for i in GraphMatrix:
	#	#print i

    # Para saber el indice donde comienzan los valores de cada atributo
	WS = WhereStart(AttributeValueQuantity)
	fileop = open(filename, "r")
	it = islice(fileop, 1, None)
	for line in it:
		##print line
		LineElements = line.split(',')
		for i in range(len(LineElements)-1):
			for j in range(i+1,len(LineElements)):
				if '_' in LineElements[i] and '_' in LineElements[j]:
					##print LineElements[i],'-',LineElements[j]
					Attribute = LineElements[i][:LineElements[i].index('_')].replace('\n','')
					#Value = LineElements[i][LineElements[i].index('_')+1:].replace('\n','').replace(' ','')
					Value = LineElements[i].replace('\n','').replace(' ','')
					AttributeIndex =AttributeNameList.index(Attribute)
					row = WS[AttributeIndex] + AttributeValueList[AttributeIndex].index(Value)
					Attribute2 = LineElements[j][:LineElements[j].index('_')].replace('\n','')
					Attribute2Index = AttributeNameList.index(Attribute2)
					#Value2 = LineElements[j][LineElements[j].index('_')+1:].replace('\n','').replace(' ','')
					Value2 = LineElements[j].replace('\n','').replace(' ','')
					column = WS[Attribute2Index] + AttributeValueList[Attribute2Index].index(Value2)
					GraphMatrix[row][column][0]=int(GraphMatrix[row][column][0])+1
					GraphMatrix[column][row][0]=int(GraphMatrix[column][row][0])+1
					##print Attribute ,' y ', Attribute2, ' de ', AttributeNameList[AttributeIndex],'-', AttributeNameList[Attribute2Index]
	
    # #print 'Total values',TotalValues
	for i in range(len(AttributeNameList)):
		TotalAttributesValues.extend(AttributeValueList[i])
	#print 'TOTAL ATTributeValues: ', TotalAttributesValues
	fileop.close()


'''
From csv To Matrix
'''
def CsvFile(filename, GraphMatrix):
	fileop = open(filename, "r")
	AttributeValueQuantity = []
	AttributeNameList = []
	AttributeValueList = []
	TotalValues = 0
	AttributeNameList = fileop.readline().split(',')
	##print 'AttributeNameList:', len(AttributeNameList), AttributeNameList
	for i in range(len(AttributeNameList)):
		AttributeValueQuantity.append(0)
		AttributeValueList.append([])
	##print 'AttributeValueQuantity', len(AttributeValueQuantity) 
	##print 'AttributeValueList', len(AttributeValueList)
	# line = fileop.readline()
	# while line != '':
	it = islice(fileop, 0, None)
	for line in it:
		AtributesLine = line.split(',')
		##print 'Attribute line:', len(AtributesLine), AtributesLine
		##print 'Attribute values:', len(AttributeValueList), AttributeValueList
		for i in range(len(AtributesLine)):
			if '\n' in AtributesLine[i]:
				AtributesLine[i] = AtributesLine[i].replace('\n','')
			if AtributesLine[i] not in AttributeValueList[i]:
				AttributeValueList[i].append(AtributesLine[i])
				AttributeValueQuantity[i] += 1
				TotalValues += 1
	fileop.close()
	# #print 'Total de atributos:', len(AttributeValueQuantity)
	# #print 'Atributos y valores:'
	# for i in range(len(AttributeNameList)):
	##print AttributeNameList[i],':',AttributeValueQuantity[i],',',AttributeValueList[i]
	# genera matriz con ceros
	for i in range(TotalValues):
		l = []
		for j in range(TotalValues):
			l.append([0])
		GraphMatrix.append(l)
	# for i in GraphMatrix:
	#	#print i
	# Para saber el indice donde comienzan los valores de cada atributo
	WS = WhereStart(AttributeValueQuantity)
	fileop = open(filename, "r")
	it = islice(fileop, 1, None)
	for line in it:
		# #print line
		LineElements = line.split(',')
		i = 0
		while i < len(LineElements) - 1:
			if i == 0:
				row = AttributeValueList[0].index(LineElements[0])  # Dentro de la lista de valores del atributo i, busca el indice del valor
			else:
				row = WS[i] + AttributeValueList[i].index(LineElements[i])
			for j in range(i + 1, len(LineElements)):
				if '\n' in LineElements[j]:
					LineElements[j] = LineElements[j].replace('\n', '')
				# #print LineElements[j], ' in ',AttributeValueList[j]
				column = WS[j] + AttributeValueList[j].index(LineElements[j])
				# #print 'Agregar uno al elemento en:', row,column
				GraphMatrix[row][column][0] = int(GraphMatrix[row][column][0]) + 1
				GraphMatrix[column][row][0] = int(GraphMatrix[column][row][0]) + 1
			i += 1
	# #print 'Total values',TotalValues
	for i in range(len(AttributeNameList)):
		TotalAttributesValues.extend(AttributeValueList[i])
	fileop.close()

def DocumentsFKTxtFile(GraphMatrix,FatherTable,ForeingKeySet,files_path):
	print ('Carpeta: ',files_path)
	print (ForeingKeySet)
	ForeingKeys = ForeingKeySet.split(',')
	print (ForeingKeys)
	AttributeValueQuantity = []
	AttributeNameList = []
	AttributeValueList = []
	AttributesOnFatherTable = []
	AttributesValueListOnFatherTable = []
	TotalValues = 0
	for filename in os.listdir(files_path):
		fileop = open(files_path+'/'+filename,'r')
		#print ('In file name: ', filename)
		#print ('Father table: ',FatherTable)
		AttributeNameListAux = fileop.readline().split()
		#print ('AttributeNameListAux', AttributeNameListAux)
		if filename == FatherTable+'.txt':
			AttributesOnFatherTable = AttributeNameListAux
			print  (AttributesOnFatherTable[0],'-----------------')
		for i in AttributeNameListAux:
			if i not in AttributeNameList:
				AttributeNameList.append(i)
		for i in range(len(AttributeNameList)):
			AttributeValueQuantity.append(0) 
			AttributeValueList.append([])
		it = islice(fileop, 0, None)
		for line in it:
			AtributesLine = line.split()
			#print('Atributesline: ',AtributesLine)
			#print('AttributeValueList: ', AttributeValueList)			
			#print('AttributeNameList: ',AttributeNameList)
			#print('AttributeNameListAux: ',AttributeNameListAux)
			for i in range(len(AtributesLine)):
				if AtributesLine[i] not in AttributeValueList[AttributeNameList.index(AttributeNameListAux[i])]:
					AttributeValueList[AttributeNameList.index(AttributeNameListAux[i])].append(AtributesLine[i])
					AttributeValueQuantity[AttributeNameList.index(AttributeNameListAux[i])] += 1
					TotalValues += 1
		fileop.close()
	# genera matriz con ceros
	for i in range(TotalValues):
		l = []
		for j in range(TotalValues):
			l.append([0])
		GraphMatrix.append(l)
	print ('AttributeValueList: ', AttributeValueList)
	print ('AttributesOnFatherTable: ', AttributesOnFatherTable)
	print ('Index general: ',AttributeNameList.index(AttributesOnFatherTable[0]))
	print ('AttributeValueson father table: ')
	AttributesValuesOnFatherTable =[]
	for i in range(len(AttributesOnFatherTable)):
		AttributesValuesOnFatherTable.extend(AttributeValueList[AttributeNameList.index(AttributesOnFatherTable[i])])
	print ('Attribute values on father table: ',AttributesValuesOnFatherTable)
		#print(AttributeValueList[AttributeNameList.index(AttributesOnFatherTable[i])])
	WS = WhereStart(AttributeValueQuantity)
	for filename in os.listdir(files_path):
		fileop = open(files_path + '/' + filename, "r")
		AttributeNameListAux = fileop.readline().split()
		it = islice(fileop, 1, None)
		for line in it:
			LineElements = line.split(' ')
			i = 0
			fk_bool = False
			while i < len(LineElements) - 1:
				if i == 0:
					row = AttributeValueList[AttributeNameList.index(AttributeNameListAux[0])].index(LineElements[0])  # Dentro de la lista de valores del atributo i, busca el indice del valor
				else:
					row = WS[AttributeNameList.index(AttributeNameListAux[i])] + AttributeValueList[AttributeNameList.index(AttributeNameListAux[i])].index(LineElements[i])
				for j in range(i + 1, len(LineElements)):
					if '\n' in LineElements[j]:
						LineElements[j] = LineElements[j].replace('\n', '')						
					column = WS[AttributeNameList.index(AttributeNameListAux[j])] + AttributeValueList[AttributeNameList.index(AttributeNameListAux[j])].index(LineElements[j])
					GraphMatrix[row][column][0] = int(GraphMatrix[row][column][0]) + 1
					GraphMatrix[column][row][0] = int(GraphMatrix[column][row][0]) + 1					
				i += 1
		fileop.close()
		# #print 'Total values',TotalValues
	for i in AttributeValueList:
		TotalAttributesValues.extend(i)
	print (TotalAttributesValues)
	for i in GraphMatrix:
		print (i)
	IndexInvolveOnFatherTable =[]
	IndexInvolveForeingKey = []
	IndexByForeingKey =[]	
	for attribute in AttributesOnFatherTable:
		i_a = AttributeNameList.index(attribute)
		init = WS[i_a]
		end = init + len(AttributeValueList[i_a])
		IndexInvolveOnFatherTable.extend(list(range(init,end)))
		if attribute in ForeingKeys:
			IndexInvolveForeingKey.extend(list(range(init,end)))
			IndexByForeingKey.append(list(range(init,end)))
	print('Indices de los atributos en la father table: ', IndexInvolveOnFatherTable)
	print('Indices de los atributos foreing key: ', IndexInvolveForeingKey)
	print('Indices de foreign keys separados: ', IndexByForeingKey)
	
	for i in range(len(GraphMatrix)):
		if i in IndexInvolveForeingKey:
			for j in range(len(GraphMatrix[i])):
				if j not in IndexInvolveOnFatherTable and GraphMatrix[i][j][0]!=0:
					for k in  IndexInvolveOnFatherTable:
						if IsNotSameForeingKey(k,i,IndexByForeingKey):
							GraphMatrix[k][j][0] += GraphMatrix[i][j][0]
							GraphMatrix[j][k][0] += GraphMatrix[i][j][0]
	#print('***************')
	#for i in GraphMatrix:
	#	print (i)
	#print('***************')
	 


def IsNotSameForeingKey(indx_k, indx_i, AllIndxFK):
	print (AllIndxFK)
	print ('i: ',indx_i)
	print ('k: ',indx_k)
	NotFound= True
	i=0
	while(NotFound):
		if indx_i in AllIndxFK[i]:
			NotFound = False
		else:
			i += 1		
	if not NotFound:
		if indx_k in AllIndxFK[i]:
			print('no entra')
			return False
		else:
			print ('entra')
			return True
	else:
		return False
		print (indx_i,' is not a foreing key')

'''
From txt FileS To Matrix
'''
def DocumentsTxtFile(GraphMatrix):
    AttributeValueQuantity = []
    AttributeNameList = []
    AttributeValueList = []
    TotalValues = 0

    for filename in os.listdir(files_path):
        # filename = filename.replace('.txt', '')
        fileop = open(files_path + '/' + filename, "r")
        AttributeNameListAux = fileop.readline().split()
        for i in AttributeNameListAux:
            if i not in AttributeNameList:
                AttributeNameList.append(i)

        for i in range(len(AttributeNameList)):
            AttributeValueQuantity.append(0)
            AttributeValueList.append([])
        # line = fileop.readline()
        # while line != '':
        it = islice(fileop, 0, None)
        for line in it:
            AtributesLine = line.split()
            for i in range(len(AtributesLine)):
                if AtributesLine[i] not in AttributeValueList[AttributeNameList.index(AttributeNameListAux[i])]:
                    AttributeValueList[AttributeNameList.index(AttributeNameListAux[i])].append(AtributesLine[i])
                    AttributeValueQuantity[AttributeNameList.index(AttributeNameListAux[i])] += 1
                    TotalValues += 1
        fileop.close()
    # genera matriz con ceros
    for i in range(TotalValues):
        l = []
        for j in range(TotalValues):
            l.append([0])
        GraphMatrix.append(l)
    # for i in GraphMatrix:
    #   #print i

    #print 'Total de atributos:', len(AttributeValueQuantity)
    #print 'tributeValueList', AttributeValueList
    #print 'Atributos y valores:'
    #for i in range(len(AttributeNameList)):
        #print AttributeNameList[i], ':', AttributeValueQuantity[i], ',', AttributeValueList[i]

    # Para saber el indice donde comienzan los valores de cada atributo
    WS = WhereStart(AttributeValueQuantity)

    for filename in os.listdir(files_path):
        fileop = open(files_path + '/' + filename, "r")
        AttributeNameListAux = fileop.readline().split()
        it = islice(fileop, 1, None)
        for line in it:
            # #print line
            LineElements = line.split(' ')
            i = 0
            while i < len(LineElements) - 1:
                if i == 0:
                    row = AttributeValueList[AttributeNameList.index(AttributeNameListAux[0])].index(
                        LineElements[0])  # Dentro de la lista de valores del atributo i, busca el indice del valor
                else:
                    row = WS[AttributeNameList.index(AttributeNameListAux[i])] + AttributeValueList[
                        AttributeNameList.index(AttributeNameListAux[i])].index(LineElements[i])
                for j in range(i + 1, len(LineElements)):
                    if '\n' in LineElements[j]:
                        LineElements[j] = LineElements[j].replace('\n', '')
                    # #print LineElements[j], ' in ',AttributeValueList[j]
                    column = WS[AttributeNameList.index(AttributeNameListAux[j])] + AttributeValueList[
                        AttributeNameList.index(AttributeNameListAux[j])].index(LineElements[j])
                    # #print 'Agregar uno al elemento en:', row,column
                    GraphMatrix[row][column][0] = int(GraphMatrix[row][column][0]) + 1
                    GraphMatrix[column][row][0] = int(GraphMatrix[column][row][0]) + 1
                i += 1
        fileop.close()
        # #print 'Total values',TotalValues
    for i in AttributeValueList:
        TotalAttributesValues.extend(i)

    #print '******************************'
    #print TotalAttributesValues    
    

'''
From arffFile to Matrix
'''
def ArffFile(filename, GraphMatrix):
    # #print 'Arff'
    # @attribute attribute_name {values}
    # @data
    # % blah blah ....
    # data...los valores estan separados por comas
    AttributeValueQuantity = []
    AttributeNameList = []
    AttributeValueList = []
    TotalValues = 0
    fileop = open(filename, "r")
    line = fileop.readline()
    linenumber = 1
    while '@data' not in line:
        if '@attribute' in line:
            line = line.replace(',', ' ')
            Atr = line.split()
            AttributeNameList.append(Atr[1])
            if '{' in line:
                ValueList = []
                for i in range(2, len(Atr)):
                    if '{' in Atr[i]:
                        Atr[i] = Atr[i].replace('{', '')
                    elif '}' in Atr[i]:
                        Atr[i] = Atr[i].replace('}', '')
                    if Atr[i] != '':
                        ValueList.append(Atr[i])
                TotalValues += len(ValueList)
                AttributeValueQuantity.append(len(ValueList))
                AttributeValueList.append(ValueList)
            else:
                AttributeValueQuantity.append(0)
                AttributeValueList.append([])
        linenumber += 1
        line = fileop.readline()
    # #print 'Total de atributos:', len(AttributeValueQuantity)
    # #print 'Total de valores:', TotalValues
    # #print 'Atributos y valores:'
    # for i in range(len(AttributeNameList)):
    #	#print AttributeNameList[i],':',AttributeValueQuantity[i],',',AttributeValueList[i]

    CompleteValues = True
    i = 0
    while CompleteValues and i < len(AttributeValueQuantity):
        # #print AttributeValueQuantity[i]
        if AttributeValueQuantity[i] == 0:
            CompleteValues = False
        else:
            i += 1

    if not CompleteValues:
        # #print 'there are attributes with non determinated values'
        # Sabe donde se quedo, en ese caso no se necesita linenumber
        it = islice(fileop, 0, None)
        for line in it:
            # #print '*****',line
            if '%' not in line:
                AtributesLine = line.split(',')
                for i in range(len(AtributesLine)):
                    if '\n' in AtributesLine[i]:
                        AtributesLine[i] = AtributesLine[i].replace('\n', '')
                    if AtributesLine[i] not in AttributeValueList[i]:
                        AttributeValueList[i].append(AtributesLine[i])
                        AttributeValueQuantity[i] += 1
                        TotalValues += 1
        fileop.close()

        # #print 'Total de atributos:', len(AttributeValueQuantity)
        # #print 'Atributos y valores:'
        # for i in range(len(AttributeNameList)):
        #	#print AttributeNameList[i],':',AttributeValueQuantity[i],',',AttributeValueList[i]

        for i in range(TotalValues):
            l = []
            for j in range(TotalValues):
                l.append([0])
            GraphMatrix.append(l)
        # for i in GraphMatrix:
        #	#print i

        WS = WhereStart(AttributeValueQuantity)

        fileop = open(filename, "r")
        it = islice(fileop, linenumber, None)
        for line in it:
            if '%' not in line:
                # #print line
                LineElements = line.split(',')
                i = 0
                while i < len(LineElements) - 1:
                    if i == 0:
                        row = AttributeValueList[0].index(
                            LineElements[0])  # Dentro de la lista de valores del atributo i, busca el indice del valor
                    else:
                        row = WS[i] + AttributeValueList[i].index(LineElements[i])
                    for j in range(i + 1, len(LineElements)):
                        if '\n' in LineElements[j]:
                            LineElements[j] = LineElements[j].replace('\n', '')
                        # #print LineElements[j], ' in ',AttributeValueList[j]
                        column = WS[j] + AttributeValueList[j].index(LineElements[j])
                        # #print 'Agregar uno al elemento en:', row,column
                        GraphMatrix[row][column][0] = int(GraphMatrix[row][column][0]) + 1
                        GraphMatrix[column][row][0] = int(GraphMatrix[column][row][0]) + 1
                    i += 1

    else:
        for i in range(TotalValues):
            l = []
            for j in range(TotalValues):
                l.append([0])
            GraphMatrix.append(l)
        # for i in GraphMatrix:
        #	#print i

        WS = WhereStart(AttributeValueQuantity)
        it = islice(fileop, 0, None)
        for line in it:
            if '%' not in line:
                # #print line
                LineElements = line.split(',')
                i = 0
                while i < len(LineElements) - 1:
                    if i == 0:
                        row = AttributeValueList[0].index(
                            LineElements[0])  # Dentro de la lista de valores del atributo i, busca el indice del valor
                    else:
                        row = WS[i] + AttributeValueList[i].index(LineElements[i])
                    for j in range(i + 1, len(LineElements)):
                        if '\n' in LineElements[j]:
                            LineElements[j] = LineElements[j].replace('\n', '')
                        # #print LineElements[j], ' in ',AttributeValueList[j]
                        column = WS[j] + AttributeValueList[j].index(LineElements[j])
                        # #print 'Agregar uno al elemento en:', row,column
                        GraphMatrix[row][column][0] = int(GraphMatrix[row][column][0]) + 1
                        GraphMatrix[column][row][0] = int(GraphMatrix[column][row][0]) + 1
                    i += 1
    # #print 'Total values',TotalValues
    for i in range(len(AttributeNameList)):
        TotalAttributesValues.extend(AttributeValueList[i])
    fileop.close()


'''
From arffFile to Matrix
'''


def DocumentsArffFile(GraphMatrix):
    # #print 'Arff'
    # @attribute attribute_name {values}
    # @data
    # % blah blah ....
    # data...los valores estan separados por comas

    AttributeValueQuantity = []
    AttributeNameList = []
    AttributeValueList = []
    TotalValues = 0

    for filename in os.listdir(files_path):
        # #print f
        # filename = filename.replace('.arff', '')
        # fileop = open(filename, "r")
        fileop = open(files_path + '/' + filename, "r")
        line = fileop.readline()
        linenumber = 1
        while '@data' not in line:
            if '@attribute' in line:
                line = line.replace(',', ' ')
                Atr = line.split()
                AttributeNameList.append(Atr[1])
                if '{' in line:
                    ValueList = []
                    for i in range(2, len(Atr)):
                        if '{' in Atr[i]:
                            Atr[i] = Atr[i].replace('{', '')
                        elif '}' in Atr[i]:
                            Atr[i] = Atr[i].replace('}', '')
                        if Atr[i] != '':
                            ValueList.append(Atr[i])
                    TotalValues += len(ValueList)
                    AttributeValueQuantity.append(len(ValueList))
                    AttributeValueList.append(ValueList)
                else:
                    AttributeValueQuantity.append(0)
                    AttributeValueList.append([])
            linenumber += 1
            line = fileop.readline()
        # #print 'Total de atributos:', len(AttributeValueQuantity)
        # #print 'Total de valores:', TotalValues
        # #print 'Atributos y valores:'
        # for i in range(len(AttributeNameList)):
        #	#print AttributeNameList[i],':',AttributeValueQuantity[i],',',AttributeValueList[i]
        CompleteValues = True
        i = 0
        while CompleteValues and i < len(AttributeValueQuantity):
            # #print AttributeValueQuantity[i]
            if AttributeValueQuantity[i] == 0:
                CompleteValues = False
            else:
                i += 1

        if not CompleteValues:
            # #print 'there are attributes with non determinated values'
            # Sabe donde se quedo, en ese caso no se necesita linenumber
            it = islice(fileop, 0, None)
            for line in it:
                # #print '*****',line
                if '%' not in line:
                    AtributesLine = line.split(',')
                    for i in range(len(AtributesLine)):
                        if '\n' in AtributesLine[i]:
                            AtributesLine[i] = AtributesLine[i].replace('\n', '')
                        if AtributesLine[i] not in AttributeValueList[i]:
                            AttributeValueList[i].append(AtributesLine[i])
                            AttributeValueQuantity[i] += 1
                            TotalValues += 1
            fileop.close()

            # #print 'Total de atributos:', len(AttributeValueQuantity)
            # #print 'Atributos y valores:'
            # for i in range(len(AttributeNameList)):
            # #print AttributeNameList[i],':',AttributeValueQuantity[i],',',AttributeValueList[i]

        for i in range(TotalValues):
            l = []
            for j in range(TotalValues):
                l.append([0])
            GraphMatrix.append(l)
            # for i in GraphMatrix:
            #	#print i

        WS = WhereStart(AttributeValueQuantity)

        for filename in os.listdir(files_path):
            fileop = open(filename, "r")
            it = islice(fileop, linenumber, None)
            for line in it:
                if '%' not in line:
                    # #print line
                    LineElements = line.split(',')
                    i = 0
                    while i < len(LineElements) - 1:
                        if i == 0:
                            row = AttributeValueList[0].index(
                                LineElements[
                                    0])  # Dentro de la lista de valores del atributo i, busca el indice del valor
                        else:
                            row = WS[i] + AttributeValueList[i].index(LineElements[i])
                        for j in range(i + 1, len(LineElements)):
                            if '\n' in LineElements[j]:
                                LineElements[j] = LineElements[j].replace('\n', '')
                            # #print LineElements[j], ' in ',AttributeValueList[j]
                            column = WS[j] + AttributeValueList[j].index(LineElements[j])
                            #   #print 'Agregar uno al elemento en:', row,column
                            GraphMatrix[row][column][0] = int(GraphMatrix[row][column][0]) + 1
                            GraphMatrix[column][row][0] = int(GraphMatrix[column][row][0]) + 1
                        i += 1

        else:
            for i in range(TotalValues):
                l = []
                for j in range(TotalValues):
                    l.append([0])
                GraphMatrix.append(l)
            # for i in GraphMatrix:
            #	#print i

            WS = WhereStart(AttributeValueQuantity)
            it = islice(fileop, 0, None)
            for line in it:
                if '%' not in line:
                    # #print line
                    LineElements = line.split(',')
                    i = 0
                    while i < len(LineElements) - 1:
                        if i == 0:
                            row = AttributeValueList[0].index(
                                LineElements[
                                    0])  # Dentro de la lista de valores del atributo i, busca el indice del valor
                        else:
                            row = WS[i] + AttributeValueList[i].index(LineElements[i])
                        for j in range(i + 1, len(LineElements)):
                            if '\n' in LineElements[j]:
                                LineElements[j] = LineElements[j].replace('\n', '')
                            # #print LineElements[j], ' in ',AttributeValueList[j]
                            column = WS[j] + AttributeValueList[j].index(LineElements[j])
                            # #print 'Agregar uno al elemento en:', row,column
                            GraphMatrix[row][column][0] = int(GraphMatrix[row][column][0]) + 1
                            GraphMatrix[column][row][0] = int(GraphMatrix[column][row][0]) + 1
                        i += 1
        # #print 'Total values',TotalValues
        for i in range(len(AttributeNameList)):
            TotalAttributesValues.extend(AttributeValueList[i])
        fileop.close()



def ReadFile():
	filename_ext = input('Name of the database file with its extension: ')
	if '.arff' not in filename_ext and '.txt' not in filename_ext and '.csv' not in filename_ext:
		print ('file extension not accepted')
	else:
		if '.arff' in filename_ext:
			ArffFile(filename_ext, GraphMatrix)
			filename = filename_ext.replace('.arff', '')
		elif '.txt' in filename_ext:
			TxtFile_ValueEqualAttribute(filename_ext,GraphMatrix)
			#TxtFile_AttributeNameBeforeValue(filename_ext,GraphMatrix)
			#TxtFile(filename_ext, GraphMatrix)
            #CsvFile(filename_ext, GraphMatrix)
			filename = filename_ext.replace('.txt', '')
		elif '.csv' in filename_ext:
			CsvFile(filename_ext, GraphMatrix)
			filename = filename_ext.replace('.csv', '')


# Histogram

def ReadNetworkxGraph():
    # NG = nx.read_edgelist('data/facebook_combined.txt',create_using = nx.Graph(), nodetype=int)
    NG = nx.karate_club_graph()
    filename = 'karate_club'
    # #print nx.info(NG)
    # plt.axis('off')
    nx.draw_circular(NG, with_labels=True)
    # nx.draw_networkx(NG,with_labels =True,node_size=35)
    plt.show()
    for n in range(len(NG.nodes())):
        row = []
        for k in range(len(NG.nodes())):
            row.append([0])
        GraphMatrix.append(row)

    Nodes = NG.nodes()
    for i in range(len(Nodes)):
        for j in range(len(Nodes)):
            if j in list(NG.neighbors(i)):
                GraphMatrix[i][j][0] += 1
    for i in NG.nodes():
        TotalAttributesValues.append(str(i))
    return NG


MyGraph = []
GraphMatrix = []
LA = []
TotalAttributesValues = []
filename = ''
opt = input('Select an option:\n 1.Data from file\n 2.Data from a set of files \n 3.Data from networkx graph \n')
if '1' in opt:
	ReadFile()
elif '2' in opt:
	files_path = input('File name:')
	fk_bool = input('There is a foreign key?(Y/N) ')
	if fk_bool=='n' or fk_bool=='N':
		typeoffiles = input('Give the files type: \n')
		if 'txt' in typeoffiles or 'csv' in typeoffiles:
			DocumentsTxtFile(GraphMatrix)     
		elif 'arff' in typeoffiles:
			DocumentsArffFile(GraphMatrix)
	else:
		FatherTable = input('Father table name: ')
		ForeingKeySet=input('Give the set of foreign keys: ')
		print('ok, let us go work with: ',files_path)
		DocumentsFKTxtFile(GraphMatrix,FatherTable,ForeingKeySet,files_path)
		
		

elif '3' in opt:
    NG = ReadNetworkxGraph()

if GraphMatrix != []:
	# Histograma
	#OutputFile = open(filename+'_info.txt', 'w')
	#max_value = 0
	#min_value = 0
	#data = []
	#total = 0
	#quant = {}
	#OutputFile.write('Matrix: '+str(len(GraphMatrix[0]))+'x'+str(len(GraphMatrix)))
	for i in GraphMatrix:
		print (i)
	#	OutputFile.write(str(i) + '\n')
	#	for j in i:
	#		if j[0] in quant:
	#			quant[j[0]] += 1
	#		else:
	#			quant[j[0]] = 1
	#		data.append(j[0])
	#		total += 1
	#		if j[0] > max_value:
	#			max_value = j[0]
	#		elif j[0] < min_value:
	#			min_value = j[0]
	#hist(data,total,(min_value,max_value))
	#show()
	#d = collections.OrderedDict(sorted(quant.items()))
	#for k, v in d.iteritems():
	#	OutputFile.write(str(k) + ': ' + str(v) + '\n')
	#OutputFile.close()
	#print 'total ',len(TotalAttributesValues)
	#fin del histograma
	# for i in LA:
	#	#print i
	##print 'Total attributes: ', len(TotalAttributesValues)
	ans = input('Would you like to apply the decomposition algorithm on: \n 1.Current graph \n 2.Standard Gaifman graph \n 3.Thresholded graph  \n 4.Lineal graph  \n 5.Exponential Gaifman graph \n 6.Shortest path graph \n 7.Quantity of shortest independent paths graph \n  ')
	if '1' in ans:
		MyGraph = GraphMatrix
	if '3' in ans:
		threshold = input('The edges greater than the threshold will be considered. Give a lower threshold: ')
		uthreshold = input('The edges below than the threshold will be considered. Give a upper threshold (0 = not upper threshold): ')
		
		# threshold ='0'
		MatrixToMATPD(GraphMatrix, MyGraph, int(threshold),int(uthreshold))
		for i in MyGraph:
			print (i)
	elif '4' in ans:
		lowerthreshold = input('Give a lower threshold:')
		upperthreshold = input('Give a upper threshold (0 = not upper threshold):')
		IntervalSize = input('Give the interval size: ')
		if lowerthreshold != '0':
			for i in range(len(GraphMatrix)):
				for j in range(len(GraphMatrix[i])):
					if i != j and int(GraphMatrix[i][j][0]) <= int(lowerthreshold):
						GraphMatrix[i][j][0] = '0'
		if upperthreshold != '0':
			sameclass = str(int(upperthreshold) + int(IntervalSize))
			for i in range(len(GraphMatrix)):
				for j in range(len(GraphMatrix[i])):
					if i != j and int(GraphMatrix[i][j][0]) > int(upperthreshold):
						GraphMatrix[i][j][0] = sameclass						
		MatrixLinear(GraphMatrix, MyGraph, IntervalSize)
		for i in MyGraph:
			print (i)
		sp=input('Would you like to get the shortest path version: (y/n)')
		if sp=='y':
			MyGraph = MatrixShortestPaths(MyGraph)
		
		for i in MyGraph:
			print (i)
	elif '6' in ans:
		ShortestPathGraph = []
		if '1' in opt or '2' in opt:
			ShortestPathGraph = MatrixShortestPaths(GraphMatrix)
			#print ('Here')
			#print(ShortestPathGraph)
		else:
			ShortestPathGraph = gen_ShortestPathMatixFromNetxG(NG)
		#OutputFile.write('ShortestPath\n')
		for i in ShortestPathGraph:
			print (i)
			#OutputFile.write(str(i) + '\n')
		mp = input('Would you like to give a path threshold? (y/n)')
		if mp== 'y':	
			threshold = input('The length paths less or equal to threshold will be considered. Give a threshold: ')
			MatrixToShortestPathM(ShortestPathGraph, MyGraph, int(threshold))
		#OutputFile.write('-----------\n')
		#OutputFile.write('Threshold: ' + threshold + '\n')
		MyGraph = ShortestPathGraph
		for i in MyGraph:
			print (i)
			#OutputFile.write(str(i) + '\n')
	elif '7' in ans:
		if '1' in opt or '2' in opt:
			print ('It is not possible jet')
			# ShortestPathGraph = gen_MatrixQuantShortestPaths(NG)
		else:
			ShortestPathGraph = gen_MatrixQuantShortestPaths(NG)
			#OutputFile.write('QuantityOfShortestPath\n')
			#for i in ShortestPathGraph:
				#print i
				#OutputFile.write(str(i) + '\n')
			threshold = input('The length paths less than the threshold will be not considered. Give a threshold: ')
			MatrixToShortestPathM(ShortestPathGraph, MyGraph, int(threshold))
			OutputFile.write('-----------\n')
			OutputFile.write('Threshold: ' + threshold + '\n')
			for i in MyGraph:
				#print i
				OutputFile.write(str(i) + '\n')
	elif '5' in ans:
		lowerthreshold = input('Give a lower threshold:')
		upperthreshold = input('Give a upper threshold (0 = not upper threshold):')
		if lowerthreshold != '0':
			for i in range(len(GraphMatrix)):
				for j in range(len(GraphMatrix[i])):
					if i != j and int(GraphMatrix[i][j][0]) <= int(lowerthreshold):
						GraphMatrix[i][j][0] = '0'
		if upperthreshold != '0':
			sameclass = str(int(floor(log(int(upperthreshold),2))))
			for i in range(len(GraphMatrix)):
				for j in range(len(GraphMatrix[i])):
					if i != j and int(GraphMatrix[i][j][0]) > int(upperthreshold):
						GraphMatrix[i][j][0] = sameclass
		MatrixExponential(GraphMatrix, MyGraph)
		for i in MyGraph:
			print (i)
		sp=input('Would you like to get the shortest path version: (y/n)')
		if sp=='y':
			MyGraph = MatrixShortestPaths(MyGraph)
			
	elif '2' in ans:
		MatrixPlain(GraphMatrix,MyGraph)
		for i in MyGraph:
			print (i)
              
	
	
	
print(TotalAttributesValues)	
for i in TotalAttributesValues:
	print (i)

