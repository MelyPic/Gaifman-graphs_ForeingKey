from FromFileToGraph import *

'''
Input: str from','to
Output: objeto de tipo Edge

Dados string FromTo de tipo str(from)+','+str(to),
EdgeOf regresa el objeto de tipo Edge representado con dicho "nombre"
 
OjO ver quiza habra que modificar el howClansAreSeen*
'''
def EdgeOf(FromTo):
	here = False
	j=0
	while not here and j< len(EdgesNodes):
		if FromTo == str(EdgesNodes[j]):
			here = True
		else:
				j+=1
	if here:
		return EdgesNodes[j]
	else:
		return 'Edge not found'

def ObtainSingles(ListWithoutSingles,Singles):
	for i in ListWithoutSingles:
		if type(i)!= list:
			Singles.append(i)
		else:
			ObtainSingles(i,Singles)
'''
ND
Para trabajar con un grafo dirigido la funcion tendria que cosiderar las aristas del nodo a los elementos del clan

Input: Nodo no visible (str NonVisible), lista de nodos del clan(ClanList), str node 
Output: True/False
Copia los nodos del clan a una nueva lista, OurClanList, y elimina de ella el clan no visible.
Obtienen los elementos de tipo Edge que van de node a OurClanList
y ve nodo a nodo, si las aristas del nodo no visible y de node hacia un mismo nodo, estan en la misma clase de equivalencia. De ser asi sohnidica que forman clan.
'''
def ClanWithNonVisible(NonVisible,ClanList,node):
	NodeToOurClan = []
	NewEdges =[]
	OurClanList = []
	for i in ClanList:
		if i != NonVisible:
			if '[' not in str(i):
				OurClanList.append(i)
			else: #descomponer i hasta obtener solo singletons
				Singles = []
				ObtainSingles(i,Singles)
				OurClanList.extend(Singles)
		
	#OurClanList.remove(NonVisible)

	for i in OurClanList:
		NodeToOurClan.append(EdgeOf(str(i)+','+node))
			
			
	##print 'se lleno'
	#print 'OurClanList', OurClanList
	##print 'NodeToOurClan', NodeToOurClan
	
	TheyAreClans = True
	j=0
	while TheyAreClans and j <len(OurClanList):
		##print str(OurClanList[j])+','+str(NonVisible)
		
		n = EdgeOf(str(OurClanList[j])+','+str(NonVisible))
		##print 'arista del clan al nodo no visible',str(n)
		##print 'vista como: ',Find(n)
		##print 'arista del clan al nuevo nodo',str(NodeToOurClan[j])
		##print 'vista como: ',Find(NodeToOurClan[j])
		if type(n) == str:
			TheyAreClans = False
		else:
			try:
				if Find(n)== Find(NodeToOurClan[j]): 
					j+=1
				else:
					TheyAreClans = False
			except:
				TheyAreClans = False
			
	return TheyAreClans
	
'''
Input: clan.nodes lista de strings y node un str.  
Output: True/False, str: el nodo con el que node hace clan
Busca si alguno de los vertices existentes tiene Edges hacia el resto de los nodos que esten en la misma clase de equivalencia que las edges que conectan con node (desde cada vertice del clan)
'''
def ClanWith(ClanList,node):
	##print 'ClanWith:',node, ClanList
	NewEdges = []
	ClanToNode =[]
	for i in ClanList:
		ClanToNode.append(EdgeOf(str(i)+','+node))#esto en lugar de #% los ve a todos y no tendria porque tronar
	##print 'Aristas encontradas:'
	#for i in ClanToNode:
	#	#print str(i)
	i=0
	ClanFound= False
	while not ClanFound and i<len(ClanList):
		ActNode = ClanList[i]
		same=True
		j=0
		##print ':::::::::::::i',i
		while same and j <len(ClanList):
			##print '::::::::::::::::::::::j', j
			if i!=j:
				n = EdgeOf(str(ClanList[j])+','+str(ActNode))
				##print '****', str(n)
				if 'not' in str(n):
					rep = str(ActNode).split()
					r = rep[0].replace("'","")
					r = r.replace("[","")
					r = r.replace(",","")
					n = EdgeOf(str(ClanList[j])+','+r)
				#n = EdgeOf(str(ClanList[j])+','+str(ClanList[i]))
				##print str(n),'***++++***',str(ClanToNode[j])
				try:
					if Find(n)== Find(ClanToNode[j]): #ClanToNode[j] =str(ClanList[j])+','+node)
						j+=1
					else:
						same = False			
						
				except:
					same = False					
			else:
				j+=1
				
				
		if same==False:
			i+=1
		else:#elif j == len(ClanList):Solo puede hacer clan con un elemento y por lo tanto sale al encontrarlo
			ClanFound=True
	if ClanFound: 		
		return ClanFound, ClanList[i] #True/False,SomeNode
	else:
		return False,''

def RemoveFromActualClan(ListOfNodes):
	notFound = True
	i = 0
	while notFound and i < len(ActualClan.nodes):
		if ListOfNodes == ActualClan.nodes[i]:
			ActualClan.remove_clan(ActualClan.nodes[i])
			notFound = False
		elif str(ListOfNodes) in str(ActualClan.nodes[i]):
			auxclan = ActualClan.getclanwithnodes(ActualClan.nodes[i])
			notFound = False
		else:
			i+=1
		

def SplitClan(ClanList,node, NewNodes, NewClans):
	#print 'Split:'
	#print str(ClanList),type(ClanList)
	#for i in ClanList:
		#print i.nodes	
	
	ToSplit=[]
	ListToSplit = []
		
	for clan in ClanList:
		if clan.clantype == 'complete':
			SplitD={}
			for i in CCT[0]:
				#print 'CCT[0][i]: ',i
				SplitD.setdefault(i, [])	
			SplitEdges = []
			for element in clan.nodes:
				#print 'element',str(element)
				if type(element) == str:
					element = element.replace(' ','')
				SplitEdges.append(str(element)+','+node)
				##print 'SplitEdges:',str(element)+','+node
			#e=0
			#while e < len(SplitEdges):
			for e in range(len(SplitEdges)):
				edge = SplitEdges[e]
				#print 'edge ',edge
				EdgeNode = EdgeOf(edge)
				#print 'EdgeNode :::::::::::::::::',str(EdgeNode)
				if EdgeNode != 'Edge not found':
					##print '******', str(EdgeNode)
					##print 'edgeNode from', EdgeNode.EdgeFrom()
					##print Find(EdgeNode)
					if '[' in str(EdgeNode):
						ElementClan = clan.getclanwithnodes(clan.nodes[e])
						if ElementClan.nodes not in SplitD[Find(EdgeNode)]:
							SplitD[Find(EdgeNode)].append(ElementClan.nodes)
					elif EdgeNode.EdgeFrom() not in SplitD[Find(EdgeNode)]: 		
						SplitD[Find(EdgeNode)].append(EdgeNode.EdgeFrom())
			
				else:
					#print 'The edge ', edge,' is not'
					#print clan.nodes[e], type(clan.nodes[e])
					#print EdgeOf(edge)
					#print 'clan: ',clan.nodes
					#print 'clanes in clan: '
					#for k in clan.clanlist:
						#print k
					auxclan = clan.getclanwithnodes(clan.nodes[e])
					if auxclan == None:
						auxclan = ClanGenerator(clan.nodes[e])
						#ActualClan.remove_clan(auxclan)
						#RemoveFromActualClan(clan.nodes[e])
					ToSplit.append(auxclan)
					#print 'Dictionary values ', SplitD.values()
		
				for i in SplitD.values():
					#print 'Value: ',i
					if len(i)>1:
						if i not in NewClans:
							#print 'It is in new clans ', i
							NewClans.append(i)
							#print i
					
					elif len(i)==1:
						if type(i[0]) == list:
							if i[0] not in NewClans:
								NewClans.append(i[0])
						elif i[0] not in NewNodes:
							NewNodes.append(i[0])
		else:
			for j in clan.nodes:
				if '[' in str(j):
					auxclan = clan.getclanwithnodes(j)
					NewClans.append(auxclan)
				else:
					NewNodes.append(j)
		
	
			
	#for i in ToSplit:
		#print 'ToSplit: ',i			
	if ToSplit != []:
		SplitClan(ToSplit,node,NewNodes,NewClans)
	
	##print 'SPLIT RESULT: ', SplitR
		
			

'''
Input: Lista de Edges NonVisibleClans, node
Output: Devuelve los nodos ya visibles, separados segun el color por el que son vistos
y devuelve los nodo como nodos individuales en NewNodes y los nodos dentro de clanes en NewClans. 
'''
def Split(NonVisibleClans,node,TypeOfNonVisibleClans):
	##print 'Split: ', NonVisibleClans
	##print 'typelist', TypeOfNonVisibleClans
	SplitEdges=[]
	SplitD={}
	SplitR=[]
	
	NewNodes = []
	NewClans = []
	for i in CCT[0]:
		SplitD.setdefault(i, []) 
	
	for Clan in NonVisibleClans:
		##print Clan
		SplitEdges.append(str(Clan)+','+node)
	##print SplitEdges		
	
	
	for i in range(len(SplitEdges)):	
		if TypeOfNonVisibleClans[i] == 'complete':
			##print  'Arista a buscar', SplitEdges[i]
			here = False
			j = 0
			while not here and j< len(EdgesNodes):
				if SplitEdges[i] == str(EdgesNodes[j]):
					here = True
				else:
					j+=1
			if here:
				##print 'Arista encontrada:'
				SplitD[Find(EdgesNodes[j])].append(str(EdgesNodes[j].EdgeFrom()))
				#SplitR.append(str(EdgesNodes[j].EdgeFrom()))
				for i in SplitD.values():
					if i!=[] and i not in SplitR:
						SplitR.append(i)
					
			else:
				##print 'Arista no encontrada, split sobre el nodo', NonVisibleClans[i]
				SplitR.extend(Split(NonVisibleClans[i],node,TypeOfNonVisibleClans[i])[0])
		else:#primitive
			##print 'Arista a buscar (primitive)',SplitEdges[i]
			here = False
			j = 0
			while not here and j< len(EdgesNodes):
				if SplitEdges[i] == str(EdgesNodes[j]):
					here = True
				else:
					j+=1
			if here:
				##print 'Arista encontrada:'
				#SplitD[Find(EdgesNodes[j])].append(str(EdgesNodes[j].EdgeFrom()))				
				i= str(EdgesNodes[j].EdgeFrom())
				##print 'De:', str(EdgesNodes[j]), 'apilar: ',i
				if i!=[] and i not in SplitR:
					SplitR.append(i)			
			else:
				##print 'Arista no encontrada, split sobre el nodo', NonVisibleClans[i]
				SplitR.extend(Split(NonVisibleClans[i],node,[TypeOfNonVisibleClans[i]])[0])
		
	#for i in SplitR:#lista de listas 
	#	#print i
		#if len(i)==1:
			#SplitR.insert(SplitR.index(i),i[0])	
			#SplitR.remove(i)
			#if i[0] not in NewNodes:
			#	NewNodes.append(i[0])
			##print 'por lo tanto es un nodo', type(i)
		if ',' not in str(i):
			#SplitR.insert(SplitR.index(i),)
			if i not in NewNodes:
				NewNodes.append(i)
			##print 'por lo tanto es un nodo', type(i)
			
			
		else:
			##print 'por lo tanto es un clan', type(i)
			NodeList = []
			for j in i:
				if j not in "[ ],'":
					NodeList.append(j)
			##print 'Nodeslist************', NodeList
			NewClans.append(NodeList)				
	return SplitR,NewNodes,NewClans
	
'''
Input: Lista de strs que representa los nodos a ser metidos en el clan.
Output: Objeto del tipo MyClan
Segun los nodos en la lista, busca si forma un clan complete o primitive y agrega estos nodos al clan.
'''
def ClanGenerator(NodeList):
	#print 'NodeList **************************',type(NodeList)
	if type(NodeList) != list:
		return NodeList
	else:
		if len(NodeList)== 2:
			NewClan = MyClan('complete')
			NewClan.add_nodes_from(NodeList)
		elif len(NodeList)>2 :
			##print NodeList	
			##print 'tamanio de i',len(NodeList),'i[0]',NodeList[0],',',NodeList[1],'i[1]'		
			same = True
			InitialColor = Find(EdgeOf(str(NodeList[0])+','+str(NodeList[1])))					
			n = 0
			while same and n <len(NodeList)-1:
				j = n+1
				while same and j < len(NodeList):
					if Find(EdgeOf(str(NodeList[n])+','+str(NodeList[j])))== InitialColor :
						j+=1
					else: 
						same = False
				##print '****', i		
				if j==len(NodeList):
					n+=1
			if same:
				NewClan = MyClan('complete')
			else:		
				NewClan = MyClan('primitive')
			NewClan.add_nodes_from(NodeList)
		else:
			NewClan = MyClan('complete')
			NewClan.add_nodes_from(NodeList)
		return NewClan

'''
Input: NodeList Lista de str, nodos a compactar
Output: Actualiza EdgesNodes, agregando las aristas que se generan al compactar los nodos de entrada
como decidir si se compacta o no: se compactara cuando en ese momento se tenga almenos un nodo que los haga clan, i.e. que ya los este compactando.
'''
def Pack(NodeList):
	
	#PackFile = open('Pack.txt','w')	
		
	##print '******Make a clan to:' 
	#PackFile.write('******Make a clan to:\n')
	#for k in NodeList:
		#PackFile.write(str(k)+'\n')
		##print k
	if type(NodeList) == list:
		Edges = []
		for i in EdgesNodes:
			frm = i.EdgeFrom()
			to = i.EdgeTo()	
			for j in NodeList:
				if i not in Edges and str(j) == frm and '[' not in to:
					notinNodeList = True
					c=0
					while notinNodeList and c<len(NodeList):
						if to == NodeList[c]:
							notinNodeList = False
						else:
							c+=1
					if notinNodeList:
						Edges.append(i)
	#EdgesNodes cada arista se divide por su from y su to, 
	#Para cada nodo j en nodelist, buscamos este j en los from que ya tenemos con un to que sea un solo nodo
	#Tambien quitamos de las aristas, aquellas que sevayan a evaluar, no vale la pena revisar las que queremos empaquetar porque estaran dentro del empaque.
	#Por ejemplo, si queremos agregar el nodo [23, 24] buscamos en las aristas que tenemos hasta encontrarlo
	# [23,24], 29 ---[23,24] 29
	
	##print '_______elementos de NodeList en:____________'
	#PackFile.write('_______elementos de NodeList en:____________\n')
	#for i in Edges:
	#	PackFile.write(str(i)+', padre: '+str(Find(i))+'\n')
		##print str(i), Find(i)
	
		i = 0
		while i < len(Edges):
			##print 'esta--->',str(Edges[i])	
			to = Edges[i].EdgeTo()
			j = i+1
			pack = True
			ine = False
			count = 0
			InitialColor = Find(Edges[i])
			while pack and j<len(Edges):
				thisto = Edges[j].EdgeTo()
				if to == thisto:
					##print 'igual a esta ',Edges[j]
					##print InitialColor,':::',Find(Edges[j])
					if InitialColor == Find(Edges[j]):
						ine = True
						count += 1				
						j+=1
					else:
						pack = False
				else:
					j+=1
			#Se agregan las aristas que tienen el mismo color que Edges[i] como hijo de Edges[i]		
			if pack and ine and count == len(NodeList)-1:
				if EdgeOf(str(NodeList)+','+to) == 'Edge not found':#
					k = Edge(str(NodeList),',',to)#
					EdgesNodes.append(k)#
					MakeSet(k)#
					Union(Edges[i],k)#
			
				if EdgeOf(to+','+str(NodeList)) == 'Edge not found':#	
					l = Edge( to,',',str(NodeList))#
					EdgesNodes.append(l)#
					MakeSet(l)#
					Union(Edges[i],l)#
				#k = Edge(str(NodeList),',',to)
				#l = Edge( to,',',str(NodeList))
				#EdgesNodes.append(k)
				#EdgesNodes.append(l)
				#MakeSet(k)
				#MakeSet(l)
				#Union(Edges[i],k)
				#Union(Edges[i],l)
				i+=1
			
			elif pack == False:
				#Eliminar todas las Edges con ese to
				#Edges.remove(Edges[j])
				l=0
				while l< len(Edges):
					thisto = Edges[l].EdgeTo()
					if to == thisto:
						Edges.remove(Edges[l])
					else:
						l+=1
			else:
				i+=1
			
	#PackFile.write('--------Aristas finales----------\n')
	##print '--------Aristas finales----------'		
	#for i in EdgesNodes:
	#	PackFile.write(str(i)+', padre: '+str(Find(i))+'\n')
		##print str(i), Find(i)
	#PackFile.close()

'''
Input: Lista de objetos Edge
Output: Devuelve true si todas las aristas en EdgeList tienen el mismo color
'''
def EdgesHaveSameColor(EdgeList):
	Same = True
	InitialColor= Find(EdgeList[0])
	i = 1
	while Same and i < len(EdgeList):
		if InitialColor != Find(EdgeList[i]):
			Same = False
		else:
			i+=1
	return Same

'''
Input: MyClan Clan,str node 
Output: 2 Lists of Edge type y una listas de string q representa los nodos no visibles desde node.
SameColorAsClan, VisibleClans, NonVisibleClans
'''
def HowClansAreSeen(Clan,node):#MyClan Clan, str node 
	NewEdges=[] 
	EdgesNodesList =[]
	
	SameColorAsClan=[]
	VisibleClans=[]#devuelve las aristas visibles
	NonVisibleClans=[]
	VisibleNodes = []#regresa solo el nodo visible	
	for i in Clan.nodes:
		NewEdges.append(str(i)+','+node)
	
	#print ':',node,':'
	#print type(node)
	 		
	for i in range(len(NewEdges)):	
		##print NewEdges[i]
		here = False
		j=0
		while not here and j< len(EdgesNodes):
			if NewEdges[i] == str(EdgesNodes[j]):
				##print 'lo encontro',str(EdgesNodes[j])
				here = True
			else:
				j+=1
		
		if here:
			EdgesNodesList.append(EdgesNodes[j])
			VisibleNodes.append(Clan.nodes[i])
		else:
			to = Clan.nodes[i]
			NonVisibleClans.append(to)
	#print 'NonVisibleClans: ', NonVisibleClans
	
	if Clan.clantype == 'complete':
		##print 'encuentra el color del clan'
		one = Clan.nodes[0]
		two = Clan.nodes[1]
		while type(one)==list or type(two)==list:
			if  type(one)==list:
				one= one[0]
			if  type(two)==list:
				two= two[0]
		#print 'Searching for the color of: '+ one+' to '+ two
		e = str(one)+','+str(two)
		#e = str(Clan.nodes[0])+','+str(Clan.nodes[1])
		j = 0
		i = EdgesNodes[0]
		while e != str(i) and j<len(EdgesNodes):
			i = EdgesNodes[j]
			j+=1
			
		colorclan =Find(i)
		#print 'The color clan is: ',colorclan
		
		for c in range(len(EdgesNodesList)):
			#print 'color of',NewEdges[c],':',Find(EdgesNodesList[c])
			if colorclan != Find(EdgesNodesList[c]):
				VisibleClans.append(EdgesNodesList[c])
			else:
				SameColorAsClan.append(EdgesNodesList[c])
	else:
		for c in range(len(EdgesNodesList)):
			VisibleClans.append(EdgesNodesList[c])
	return SameColorAsClan,VisibleClans, NonVisibleClans, VisibleNodes

def GroupedByColor(VisibleClans,VisibleNodes):
	GroupedD={}
	NewClans = []
	for i in CCT[0]:
		GroupedD.setdefault(i, []) 
	
	for i in range(len(VisibleClans)):
		#print Find(VisibleClans[i])
		#print VisibleNodes[i]
		GroupedD[Find(VisibleClans[i])].append(VisibleNodes[i])
	for i in GroupedD.values():
		if i !=[] and len(i)>1:
			NewClans.append(i)	
	return NewClans
	

'''
Input: Clan de tipo MyCLan, str node que sera el nodo a aniadir
Output:el Clan actualizado.
Funcion que agrega un nuevo nodo a un clan existente.eje
'''
#Hacer Pack cuando se crean nuevos clanes			
def AddNode(Clan,node): #MyClan Clan, str node
	print ('Node to add: ',node)
	print ('Clan nodes (actual tree): ',Clan.nodes)
	print ('Clan type: ',Clan.clantype)
	##print 'Clanes en el clan con tipo'
	#for i in Clan.clanlist:
		#print i.nodes, i.clantype
	if len(Clan.nodes)==1:
		##print Clan.nodes[0]
		if '[' not in str(Clan.nodes[0]):
			Clan.add_node(node)
			##print 'un nodo habia'
		else: 
			##print 'un clan habia'
			ActualNode = Clan.nodes[0]
			for i in ActualNode:
				Clan.add_node(i)
			Clan.remove_node(ActualNode)
			AddNode(Clan,node)
	else:		
		HCAS = HowClansAreSeen(Clan,node)
		SameColorAsClan = HCAS[0]
		VisibleClans = HCAS[1]
		NonVisibleClans = HCAS[2]
		
		if Clan.clantype=='complete':
			if len(SameColorAsClan)==len(Clan.nodes):
				print ('El nodo ve a todos los elementos del mismo color que el color del clan')
				Clan.add_node(node)
				
			elif len(SameColorAsClan)!= 0:
				#print ':::INFORMACION'
				#print 'NonVisibleClans: ', NonVisibleClans
				#print 'SamecolorAsClan: ', SameColorAsClan 
				#print 'VisibleClans: ', VisibleClans
				
				ListNodesSameColor = []
				ListNodesDiferentColor = []
				for i in SameColorAsClan:
					ListNodesSameColor.append(i.EdgeFrom())
				print ('El nodo ve a algunos elementos del clan del mismo color que el color del clan')
				print ('los elementos son: ', ListNodesSameColor)
				#print ListNodesSameColor
				
				NodesInClan = Clan.nodes[:]
				for i in NodesInClan:
					#print i
					if str(i) not in ListNodesSameColor:
						ListNodesDiferentColor.append(i)
				print ('Elementos del clan que no son vistos del mismo color:', ListNodesDiferentColor)
				
				if len(ListNodesDiferentColor) == 1 and '[' in str(ListNodesDiferentColor[0]):
					ClanNotSameColor = Clan.getclanwithnodes(ListNodesDiferentColor[0])
					Clan.remove_clan(ClanNotSameColor)					
				else:
					ClanNotSameColor = MyClan('complete')
					for i in ListNodesDiferentColor:
						##print '*************',i,'+++'
						if '[' in str(i): #Se trata de un clan
							##print 'clan'
							clan_i = Clan.getclanwithnodes(i)
							##print clan_i.nodes
							ClanNotSameColor.add_clan(clan_i)
							Clan.remove_clan(clan_i)
						else:
							##print 'nodo'
							ClanNotSameColor.add_node(i)
							Clan.remove_node(i)
				
				##print Clan.nodes		
				##print '*********************'
				AddNode(ClanNotSameColor,node)
				
				##print ClanNotSameColor.nodes
				##print '++++++'
				##print Clan.nodes				
				Clan.add_clan(ClanNotSameColor)
				##print 'clan final', Clan.nodes
				Pack(ClanNotSameColor.nodes)
				##print '************************************* compacta a: ', ClanNotSameColor.nodes		
				Pack(Clan.nodes)
				
			elif len(NonVisibleClans)!=0:
				print ('El nodo no puede ver a ',len(NonVisibleClans) ,' elementos del clan y estos son:', NonVisibleClans)
				##print 'Nodos del Clan antes del Split: ', Clan.nodes
				#for i in NonVisibleClans:
				#	#print 'nodo en NonVisibleClans: ', i
				NonVisibles_ClanList =[]
					
				#TypeOfNonVisibleclans = []
				ClanList =[]#
				##print Clan.nodes
				for i in NonVisibleClans:
					##print 'buscar clan', i
					auxclan = Clan.getclanwithnodes(i)
					NonVisibles_ClanList.append(auxclan)					
					ClanList.append(auxclan)#
					#TypeOfNonVisibleclans.append(auxclan.clantype)
					Clan.remove_clan(auxclan)
				#for i in TypeOfNonVisibleclans:
					##print 'tipos', i
				
				Clan.add_node(node)
				#Clan.remove_nodes_from(NonVisibleClans)
				Clan.clantype = 'primitive'
				
				
				#S=Split(NonVisibleClans,node,TypeOfNonVisibleclans)
				S1=[]
				S2=[]
				S=SplitClan(ClanList,node,S1,S2)#
				##print 'Nuevos nodos', S[1]
				#print 'Nuevos nodos', S1
				Clan.add_nodes_from(S1)
				##print 'Nuevos clanes', S[2]
				#print 'Nuevos clanes' 
				#for u in S2:
					#print str(u)				
				for i in S2:
					#if i.nodes !=[]:# and i!=['']:
					CG = ClanGenerator(i)
					Clan.add_clan(CG)
					#Clan.add_clan(i)
					Pack(CG.nodes)				
				#print 'Nodos del Clan despues del Split: ', Clan.nodes,'***'
				
				if VisibleClans != []:
					VisibleNodes = HCAS[3]
					for j in NonVisibles_ClanList:
						if j.clantype == 'complete':
							print (j.nodes, '*******', j.clantype)
							GC = GroupedByColor(VisibleClans, VisibleNodes)
							if GC!=[]:
								for clani in GC:
									NewClan = MyClan('complete')
									for i in clani:
										if '[' in str(i):
											auxclan = Clan.getclanwithnodes(i)
											NewClan.add_clan(auxclan)
											Clan.remove_clan(auxclan)
										else:
											NewClan.add_node(i)
											Clan.remove_node(i)
									Clan.add_clan(NewClan)
									Pack(NewClan.nodes)
					
				#if VisibleClans!=[] and EdgesHaveSameColor(VisibleClans):
				#	#print 'Nodos no visibles pero el resto de nodos es visto del mismo color'
				#	VisibleNodes = HCAS[3]
				#	NewClan = MyClan('complete')
				#	for i in VisibleNodes:
				#		#print i
				#		if '[' in str(i):
				#			auxclan = Clan.getclanwithnodes(i)
				#			NewClan.add_clan(auxclan)
				#			Clan.remove_clan(auxclan)
				#		else:
				#			NewClan.add_node(i)
				#			Clan.remove_node(i)	
				#	#print 'nodos del nuevo clan: ', NewClan.nodes
				#	Clan.add_clan(NewClan)					
				#	Pack(NewClan.nodes)
				#print 'nodos finales: ', Clan.nodes
				print('el clan ', Clan.nodes ,' es ', Clan.clantype)
				
			else:
				if EdgesHaveSameColor(VisibleClans):
					print ('El nodo ve con el mismo color a todos los elementos del clan, y este color es distintos al color del clan.')
					NodesInVisibleClans =Clan.nodes[:]
					NewClan = MyClan('complete')
					for i in NodesInVisibleClans:
						##print i
						if '[' in str(i):
							auxclan = Clan.getclanwithnodes(i)
							NewClan.add_clan(auxclan)
							Clan.remove_clan(auxclan)
						else:
							NewClan.add_node(i)
							Clan.remove_node(i)
					
					#NodesInVisibleClans =Clan.nodes[:]
					Clan.add_node(node)
					#Clan.remove_nodes_from(NodesInVisibleClans)					 
					#NewClan.add_nodes_from(NodesInVisibleClans)
					Clan.add_clan(NewClan)					
					Pack(NodesInVisibleClans)
					##print 'Los nodos del clan resultante son: ', Clan.nodes, '\n **********************************mismos que se compactaron'
				else:#Si ve a k nodos del mismo color estos se deben agrupar y no se estan agrupando... revisar esto con un ejemplo
					#print 'los ve a todos pero de distinto color'				
					ClanList=[]
					Nodes = Clan.nodes[:]
					AuxClan =MyClan('complete')
					for i in Nodes:
						if '[' in str(i):
							auxclan = Clan.getclanwithnodes(i)
							AuxClan.add_clan(auxclan)
							Clan.remove_clan(auxclan)
						else:
							AuxClan.add_node(i)
							Clan.remove_node(i)
										
					#for i in Nodes:
					#	if '[' in str(i):
					#		auxclan = Clan.getclanwithnodes(i)
					#		Clan.remove_clan(auxclan)
					#	else:
					#		Clan.remove_node(i)
					
					#print 'AuxClan', AuxClan.nodes
					#print 'Clan', Clan.nodes
					#print 'Nodes', Nodes 
										
					Clan.add_node(node)
					Clan.clantype = 'primitive'
					##print 'se mantiene la copia?', AuxClan.nodes#
					ClanList.append(AuxClan)#
					#print 'ClanList ', ClanList[0].nodes
					#print 'node', node
					#S=Split(Nodes,node,['complete']) #nodees o clans???#
					S1=[]
					S2=[]				
					S=SplitClan(ClanList,node,S1,S2)#
					
					#print 'New nodes', S1
					Clan.add_nodes_from(S1)
					#print 'New clans', S2
					for i in S2:
						if i !=[] and i!=['']:
							CG = ClanGenerator(i)
							Clan.add_clan(CG)
							Pack(i)
					##print 'Nodos en el Clan despues de Split', Clan.nodes
					#No se hace pack ya que se compactara hasta que llegue un fondo que los vea a todos igual
		
		else:#primitive
			if len(NonVisibleClans) != 0:
				#print 'Hay elementos no visibles y son:'
				#for n in NonVisibleClans:
					##print n
				##print 'si el tamanio del non visible es uno, ver si hace clan con este, sino colocarlo como uno mas y hacer split'
				if len(NonVisibleClans) == 1 and ClanWithNonVisible(NonVisibleClans[0],Clan.nodes,node):
					#print 'hay un nodo/clan no visible y hace clan con el, es:', NonVisibleClans[0]
					##print 'buscarlo en: ', Clan.nodes
					ClanAux = Clan.getclanwithnodes(NonVisibleClans[0])
					Clan.remove_clan(ClanAux)
					AddNode(ClanAux,node)#Aqui se hace pack segun donde deba compactarse
					#Clan.remove_node(NonVisibleClans[0])
					Clan.add_clan(ClanAux)
				else:
					#print 'Hay un nodo/clan o mas nodos/clanes no visibles desde node: '+str(NonVisibleClans)+' (pero no forma clan con el) '
					#TypeOfNonVisibleclans = []#
					ClanList = [] #
					for i in NonVisibleClans:
						#print i
						auxclan = Clan.getclanwithnodes(i)
						#TypeOfNonVisibleclans.append(auxclan.clantype)
						Clan.remove_clan(auxclan)
						#print 'clanes restantes despues de quitar el no visible: ', Clan.nodes					
						ClanList.append(auxclan)
						
					Clan.add_node(node)
					#Clan.remove_nodes_from(NonVisibleClans)
										
					#S = Split(NonVisibleClans,node,TypeOfNonVisibleclans)
					S1 = []
					S2 = []
					S = SplitClan(ClanList,node,S1,S2)
					##print 'Nuevos nodos', S[1]
					Clan.add_nodes_from(S1)
					print ('Nuevos clanes', S2)
					for i in S2:
						print (i)
						if i!=[] and i!=[''] and i!= None:
							CG = ClanGenerator(i)
							print (CG)
							Clan.add_clan(CG)
							#Clan.add_clan(i)
							Pack(i)
					##print 'Nodos en el Clan despues de Split', Clan.nodes
				
			elif EdgesHaveSameColor(VisibleClans): 
				#print 'El nodo ve a todos los elementos del clan primitive del mismo color.'
				NodesInVisibleClans =Clan.nodes[:]
				
				NewClan= MyClan('primitive')
				for i in NodesInVisibleClans:
					if '[' in str(i):
						auxclan = Clan.getclanwithnodes(i)
						NewClan.add_clan(auxclan)
						Clan.remove_clan(auxclan)
					else:
						NewClan.add_node(i)
						Clan.remove_node(i)
							
				#Clan.remove_nodes_from(NodesInVisibleClans)
				#NewClan.add_nodes_from(NodesInVisibleClans)
				
				Clan.add_node(node)
				Clan.clantype = 'complete'
				
				Clan.add_clan(NewClan)
				Pack(NodesInVisibleClans)#Se compactan porque ya el node los esta compactando.
			else:
				#print 'Buscar si hace clan con alguno y sino colocarlo como un nodo mas'
				CW =ClanWith(Clan.nodes,node)
				if CW[0]:
					#print 'hizo clan con un node/clan'
					
					if '[' in str(CW[1]):
						#print 'hizo clan con un clan'
						AuxClan = Clan.getclanwithnodes(CW[1])
						Clan.remove_clan(AuxClan)
					else:
						#print 'hizo clan con un nodo'
						AuxClan=MyClan('complete')
						AuxClan.add_node(CW[1])
						Clan.remove_node(CW[1])
					
					AddNode(AuxClan,node)
					Pack(AuxClan.nodes)
					Clan.add_clan(AuxClan)
						
				else:
					#print 'no hizo clan, solo se agrega el nodo y el clan se mantiene primitive'
					Clan.add_node(node)
					Pack(Clan.nodes)
#@profile
		
	
class MyClan:
	def __init__ (self,typeof):
		self.clantype = typeof
		self.nodes=[]
		self.clanlist = []
		
	def nodes(self): 
		return self.nodes
	
	def remove_node(self,node):
		self.nodes.remove(node)
	
	def add_node(self,node):
		self.nodes.append(node)
		
	def add_nodes_from(self,nodelist):
		for n in nodelist:
			self.nodes.append(n)
	
	def remove_nodes_from(self,nodelist):
		for n in nodelist:
			self.nodes.remove(n)
			
	def add_clan(self,clan):
		self.add_node(clan.nodes)
		self.clanlist.append(clan)
		
	def remove_clan(self,clan):
		self.nodes.remove(clan.nodes)
		#self.remove_nodes_from(clan.nodes)
		self.clanlist.remove(clan)
			
	def getclanwithnodes(self,nodes):
		found1 = False
		c = 0
		while not found1 and c < len(self.clanlist):
			if nodes == self.clanlist[c].nodes:
				found1 = True
			else:
				c+=1
		if found1:
			return self.clanlist[c]
		#else:
			#print 'There is not clan with nodes',nodes

class Edge:
	def __init__ (self, labelFrom,sep,labelTo):
		self.label = labelFrom+sep+labelTo
		self.labelFrom = labelFrom
		self.labelTo = labelTo
		
	def __str__(self):
		return self.label
	
	def EdgeFrom(self):
		return self.labelFrom
		
	def EdgeTo(self):
		return self.labelTo
		


"""
MakeSet(x) initializes the decomposition
Find(x) returns representative object of the set containing x
Union(x,y) makes two sets containing x and y respectively into one set
"""

def MakeSet(x):
     x.parent = x
     x.rank   = 0

def Union(x, y):
     xRoot = Find(x)
     yRoot = Find(y)
     if xRoot.rank > yRoot.rank:
         yRoot.parent = xRoot
     elif xRoot.rank < yRoot.rank: 
         xRoot.parent = yRoot
     elif xRoot != yRoot: # Unless x and y are already in same set, merge them
         yRoot.parent = xRoot
         xRoot.rank = xRoot.rank + 1
     
def Find(x):
     if x.parent == x:
        return x
     else:
        x.parent = Find(x.parent)
        return x.parent
''''''''''''''''''

def ElementInX(x,ElementsList): #regresa los elementos de ElementsList que tienen raiz x
	xRoot=Find(x)
	l=[]
	for i in range(xRoot.rank+1):
		l.append([])
	for element in ElementsList:
		if str(Find(element))== str(x):
			l[element.rank].append(str(element))
	return l

def ConstructColorTrees(ColorMatrix,EdgesNodes):
	ListColors = []
	ListParents= []
	for i in range(len(ColorMatrix)):
		for j in range(len(ColorMatrix[i])):
			FromTo=str(i)+','+str(j)
			n = Edge(str(i),',',str(j))
			#n = Edge(FromTo)
			EdgesNodes.append(n)
			MakeSet(n)
			if ColorMatrix[i][j] in ListColors:
				Index= ListColors.index(ColorMatrix[i][j])
				Union(ListParents[Index],n)
			else:
				ListParents.append(n)
				ListColors.append(ColorMatrix[i][j])
	
	#for i in ListParents:
	#	#print ElementInX(i,EdgesNodes) 
	return ListParents,ListColors
#Usa Pack 1
#MyGraph_1=[['None','black','blue','black','black','black','black'],['black','None','red','black','black','black','black'],['blue','red','None','black','black','black','black'],['black','black','black','None','blue','blue','blue'],['black','black','black','blue','None','black','red'],['black','black','black','blue','black','None','blue'],['black','black','black','blue','red','blue','None']]
#Usa Split/Pack/ClanWith uno no visible		
#MyGraph_1=[['None','black','black','red','black','red','red'],['black','None','blue','red','black','red','black'],['black','blue','None','red','black','red','red'],['red','red','red','None','black','red','blue'],['black','black','black','black','None','blue','black'],['red','red','red','red','blue','None','red'],['red','black','red','blue','black','red','None']]
#Pack/ClanWith un nodo visible(el ultimo) 3
#MyGraph_1=[['None','red','blue','blue'],['red','None','black','black'],['blue','black','None','black'],['blue','black','black','None']]
#Pack/ClanWith un clan visible(el ultimo) 4
#MyGraph_1=[['None','red','blue','blue','blue','blue'],['red','None','black','black','black','black'],['blue','black','None','red','red','black'],['blue','black','red','None','red','black'],['blue','black','red','red','None','black'],['blue','black','black','black','black','None']]
#Pack/ClanWith un clan visible(el ultimo) 5
#MyGraph_1=[['None','red','blue','blue','blue','blue'],['red','None','black','black','black','black'],['blue','black','None','red','red','red'],['blue','black','red','None','red','red'],['blue','black','red','red','None','red'],['blue','black','red','red','red','None']]
#primitive y el ultimo nodo no ve a varios nodos 6
#MyGraph_1=[['None','red','blue','black','red','blue','black'],['red','None','black','red','blue','black','red'],['blue','black','None','blue','black','red','blue'],['black','red','blue','None','red','blue','black'],['red','blue','black','red','None','black','blue'],['blue','black','red','blue','black','None','red'],['black','red','blue','black','blue','red','None']]
#2 clanes no visibles 7
#MyGraph_1=[['None','red','red','red','black','red','red','red','black'],['red','None','red','red','red','red','red','red','black'],['red','red','None','black','red','red','red','black','red'],['red','red','black','None','red','red','red','black','black'],['black','red','red','red','None','red','red','red','red'],['red','red','red','red','red','None','black','red','red'],['red','red','red','red','red','black','None','red','red'],['red','red','black','black','red','red','red','None','black'],['black','black','red','black','red','red','red','black','None']]

#MyGraph =[
#['0',	'1',	'0',	'2',	'2'],
#['1',	'0',	'0',	'1',	'1'],
#['0',	'0',	'0',	'0',	'0'],
#['2',	'1',	'0',	'0',	'1'],
#['2',	'1',	'0',	'1',	'0']]#ExampleM1

#MyGraph =[
#['0',	'0',	'0',	'1',	'1'],
#['0',	'0',	'0',	'1',	'1'],
#['0',	'0',	'0',	'1',	'1'],
#['1',	'1',	'1',	'0',	'1'],
#['1',	'1',	'1',	'1',	'0']]#ExampleM2

#MyGraph =[
#['0',	'0',	'0',	'1',	'1'],
#['0',	'0',	'0',	'1',	'1'],
#['0',	'0',	'0',	'1',	'1'],
#['1',	'1',	'1',	'0',	'2'],
#['1',	'1',	'1',	'2',	'0']]#ExampleM3

#MyGraph =[
#['0',	'2',	'2',	'0',	'0'],
#['2',	'0',	'2',	'1',	'0'],
#['2',	'2',	'0',	'1',	'0'],
#['0',	'1',	'1',	'0',	'2'],
#['0',	'0',	'0',	'2',	'0']]#ExampleM4

#MyGraph =[
#['0',	'0',	'1',	'1',	'1',	'1',	'1'],
#['0',	'0',	'2',	'1',	'1',	'1',	'1'],
#['1',	'2',	'0',	'1',	'1',	'1',	'1'],
#['1',	'1',	'1',	'0',	'2',	'1',	'1'],
#['1',	'1',	'1',	'2',	'0',	'1',	'1'],
#['1',	'1',	'1',	'1',	'1',	'0',	'0'],
#['1',	'1',	'1',	'1',	'1',	'0',	'0']]#ExampleM5

#MyGraph =[
#['0',	'0',	'1',	'0',	'0',	'2',	'2'],
#['0',	'0',	'2',	'0',	'0',	'2',	'2'],
#['1',	'2',	'0',	'0',	'0',	'2',	'2'],
#['0',	'0',	'0',	'0',	'2',	'1',	'1'],
#['0',	'0',	'0',	'2',	'0',	'1',	'1'],
#['2',	'2',	'2',	'1',	'1',	'0',	'0'],
#['2',	'2',	'2',	'1',	'1',	'0',	'0']]#ExampleM6



#MyGraph =[['0',	'0',	'2',	'2',	'2',	'1'],
#['0',	'0',	'1',	'2',	'2',	'1'],
#['2',	'1',	'0',	'2',	'2',	'1'],
#['2',	'2',	'2',	'0',	'1',	'0'],
#['2',	'2',	'2',	'1',	'0',	'0'],
#['1',	'1',	'1',	'0',	'0',	'0']]#Example2

#MyGraph =[['0',	'0',	'2',	'2',	'2',	'1',	'1'],#
#['0',	'0',	'1',	'2',	'2',	'1',	'1'],
#['2',	'1',	'0',	'2',	'2',	'1',	'1'],
#['2',	'2',	'2',	'0',	'2',	'0',	'0'],
#['2',	'2',	'2',	'2',	'0',	'0',	'0'],
#['1',	'1',	'1',	'0',	'0',	'0',	'2'],
#['1',	'1',	'1',	'0',	'0',	'2',	'0']]#Example2


#MyGraph =[['0',	'1',	'1',	'0',	'1',	'1',	'1'],
#['1',	'0',	'0',	'1',	'0',	'0',	'1'],
#['1',	'0',	'0',	'1',	'0',	'0',	'1'],
#['0',	'1',	'1',	'0',	'1',	'1',	'0'],
#['1',	'0',	'0',	'1',	'0',	'1',	'1'],
#['1',	'0',	'0',	'1',	'1',	'0',	'1'],
#['1',	'1',	'1',	'0',	'1',	'1',	'0']]#Example1
#TotalAttributesValues = ['A','B', 'C','D','E','F','G']

'''
EdgesNodes tiene objetos Edge, sobre los cuales operan directamente MakeSet, y asi Find y Union
'''
EdgesNodes =[]
CCT=ConstructColorTrees(MyGraph,EdgesNodes)
#MyGraph =[[[0],	[1],	[1],	[1],	[1],	[1],	[1],	[1],	[1],	[0],	[1],	[1]],
#[[1],	[0],	[1],	[1],	[0],	[0],	[0],	[1],	[0],	[0],	[0],	[0]],
#[[1],	[1],	[0],	[1],	[0],	[0],	[0],	[1],	[1],	[1],	[0],	[0]],
#[[1],	[1],	[1],	[0],	[0],	[0],	[0],	[1],	[0],	[0],	[0],	[0]],
#[[1],	[0],	[0],	[0],	[0],	[0],	[1],	[0],	[0],	[0],	[1],	[0]],
#[[1],	[0],	[0],	[0],	[0],	[0],	[1],	[0],	[0],	[0],	[1],	[0]],
#[[1],	[0],	[0],	[0],	[1],	[1],	[0],	[0],	[0],	[0],	[0],	[0]],
#[[1],	[1],	[1],	[1],	[0],	[0],	[0],	[0],	[0],	[0],	[0],	[0]],
#[[1],	[0],	[1],	[0],	[0],	[0],	[0],	[0],	[0],	[0],	[0],	[0]],
#[[0],	[0],	[1],	[0],	[0],	[0],	[0],	[0],	[0],	[0],	[0],	[0]],
#[[1],	[0],	[0],	[0],	[1],	[1],	[0],	[0],	[0],	[0],	[0],	[0]],
#[[1],	[0],	[0],	[0],	[0],	[0],	[0],	[0],	[0],	[0],	[0],	[0]]
#]


ActualClan = MyClan('complete')
ActualClan.add_node(str(0))

for i in range(1,len(MyGraph)):
	AddNode(ActualClan,str(i))

print ("compara")
print (ActualClan.nodes)

def ObtainLeaves(SomeClan,LeavesList):
	for i in SomeClan.nodes:
		if type(i)== list:
			AuxClan = SomeClan.getclanwithnodes(i)
			ObtainLeaves(AuxClan, LeavesList)
		else:
			LeavesList.append(i)
	

def ExtractLeaves(SomeClan):
	LL=[]
	ObtainLeaves(SomeClan,LL)
	tleave =''
	for i in LL:
		tleave = tleave + TotalAttributesValues[int(i)]
	##print LL,'Internal'
	#print tleave, 'internal'
	for i in SomeClan.nodes:
		if type(i)==list:
			AuxClan = SomeClan.getclanwithnodes(i)
			ExtractLeaves(AuxClan)
		#else:
			#print TotalAttributesValues[int(i)]
			##print i, 'leaves'

		
#print '-------------------------'
ExtractLeaves(ActualClan)				
