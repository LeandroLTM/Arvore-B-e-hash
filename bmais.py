class Pag(object):     # Classe que define as páginas da árvore
	def __init__(self,folha):
		
		self.chaves = []
		self.folha = folha
		if folha:
			self.anterior = None
			self.proximo = None
		else:
			self.filhos = []

class Bmais(object):  # Classe com os atributos da árvore e os métodos
	def __init__(self,tamanho_pagina,quant):
		self.raiz = Pag(True)
		#self.raiz.chaves.append(valor)
		self.tamanho = tamanho_pagina/(28+32)
		self.tamanhoFolha = tamanho_pagina/(28*quant)

	# Método inserção inicial que recebe a raiz.
	def insereRaiz(self,raiz,valor):

		pagReturn, chave = self.insere(raiz,valor)
		if pagReturn or chave:
			pagNew = Pag(False)
			pagNew.chaves.append(chave)
			pagNew.filhos.append(raiz)
			pagNew.filhos.append(pagReturn)
			self.raiz = pagNew

	# Método intermediário que realiza a chamada da remoção para as paginas 
	# folhas, além de realizar a divisão das paginas quando necessario. 
	def insere(self,pag,valor):
		if pag.folha:
			pagReturn, chave = self.insereFolha(pag,valor)
		else:
			flag = False
			for i in pag.chaves:
					if i > valor:
						pagReturn, chave = self.insere(pag.filhos[pag.chaves.index(i)],valor)
						flag = True
						break
			if not flag:
				pagReturn, chave = self.insere(pag.filhos[len(pag.filhos)-1],valor)
			if pagReturn or chave:
				if len(pag.chaves) < int(self.tamanho):
					pag.chaves.append(chave)
					pag.chaves.sort()
					pag.filhos.insert(pag.chaves.index(chave)+1,pagReturn)
					return None,None
				else:
					pagNew = Pag(False)
					pag.chaves.append(chave)
					pag.chaves.sort()
					pag.filhos.insert(pag.chaves.index(chave)+1,pagReturn)
					pagNew.chaves = pag.chaves[int((self.tamanho/2)+0.5):]
					pag.chaves = pag.chaves[:int((self.tamanho/2)+0.5)]
					pagNew.filhos = pag.filhos[int((self.tamanho/2)+0.5)+1:]
					pag.filhos = pag.filhos[:int((self.tamanho/2)+0.5)+1]
					aux = pagNew.chaves[0]
					pagNew.chaves.pop(0)
					return pagNew,aux
		return pagReturn, chave

	# Método que insere nas paginas folhas, fazendo a divisão e conexão
	# dos irmãos
	def insereFolha(self,pag,valor):
		if len(pag.chaves) < int(self.tamanhoFolha):
			pag.chaves.append(valor)
			pag.chaves.sort()
			return None,None
		else:
			pagNew = Pag(True)
			pag.chaves.append(valor)
			pag.chaves.sort()
			pagNew.chaves = pag.chaves[int((self.tamanhoFolha/2)+0.5):]
			pag.chaves = pag.chaves[:int((self.tamanhoFolha/2)+0.5)]
			pagNew.proximo = pag.proximo
			if(pag.proximo):
				pag.proximo.anterior = pagNew
			pag.proximo = pagNew
			pagNew.anterior = pag
			return pagNew,pagNew.chaves[0]

	# Primeiro método chamado para remoção, trocando a pagina a raiz quando 
	# necessario 
	def removerRaiz(self,raiz,valor):
		if raiz.folha:
			if valor in raiz.chaves:
				raiz.chaves.remove(valor)
				return None, None
			else:
				#print("Valor não Existe")
				return None, None

		flag = False
		for i in raiz.chaves:
			if i > valor:
				pagReturn,chave = self.remover(raiz,raiz.filhos[raiz.chaves.index(i)],valor)
				flag = True
				break
		if not flag:
			pagReturn,chave = self.remover(raiz,raiz.filhos[len(raiz.chaves)],valor)
		if (pagReturn or chave) and len(raiz.chaves) == 0:
			aux = raiz
			self.raiz = pagReturn
			del aux

	# Método que auxilia na remoção, vericando se os irmão não folha possuem
	# a capacidade mínima 
	def verificaIrmao(self,pai,pag):
		esquerda = direita = False
		for i in pai.filhos:
			if i == pag:
				index = pai.filhos.index(i)
		if index > 0:
			if len(pai.filhos[index-1].chaves) > int(self.tamanho/2):
				esquerda = True
		if index < len(pai.filhos)-1:
			if len(pai.filhos[index+1].chaves) > int(self.tamanho/2):
				direita = True
		return esquerda, direita

	# Método que auxilia na remoção, vericando se os irmão folha possuem
	# a capacidade mínima
	def verificaIrmaoFolha(self,pai,pag):
		esquerda = direita = False
		for i in pai.filhos:
			if i == pag:
				index = pai.filhos.index(i)
		if index > 0:
			if len(pai.filhos[index-1].chaves) > int(self.tamanhoFolha/2):
				esquerda = True
		if index < len(pai.filhos)-1:
			if len(pai.filhos[index+1].chaves) > int(self.tamanhoFolha/2):
				direita = True
		return esquerda, direita

	# Método que verifica de existe irmão a esquerda e a direita
	def verificaSeExisteIrmao(self,pai,pag):
		esquerda = direita = False
		for i in pai.filhos:
			if i == pag:
				index = pai.filhos.index(i)
		if index < len(pai.filhos)-1:
				direita = True
		return direita

	# Método que remove e altera as paginas não folha, pegando do irmão a 
	# direita ou esquerda quando possuem capacidade mínima, e também junda 
	# as paginas quando necessario 
	def remover(self,pai,pag,valor):
		if pag.folha:
			pagReturn,chave = self.removerFolha(pai,pag,valor)
			return pagReturn,chave
		else:
			flag = False
			for i in pag.chaves:
				if i > valor:
					pagReturn,chave = self.remover(pag,pag.filhos[pag.chaves.index(i)],valor)
					flag = True
					break
			if not flag:
				pagReturn,chave = self.remover(pag,pag.filhos[len(pag.chaves)],valor)
		if pagReturn or chave:
			if len(pag.chaves) >= (self.tamanho/2):
				return None,None
			else:
				esquerda,direita = self.verificaIrmao(pai,pag)
				if esquerda:
					index_ir = pai.filhos.index(pag)-1
					pai.filhos[index_ir].chaves.remove(max(pai.filhos[index_ir].chaves))
					aux = pai.filhos[index_ir].filhos[len(pai.filhos[index_ir].filhos)-1]
					pag.filhos.insert(0,aux)
					pag.chaves.insert(0,pag.filhos[1].chaves[0])
					pai.filhos[index_ir].filhos.pop(len(pai.filhos[index_ir].filhos)-1)
					return None,None
				elif direita:
					index_ir = pai.filhos.index(pag)+1
					pai.filhos[index_ir].chaves.pop(0)
					pag.filhos.append(pai.filhos[index_ir].filhos[0])
					pag.chaves.append(pai.filhos[index_ir].filhos[0].chaves[0])
					pai.filhos[index_ir].filhos.pop(0)
					return None,None
				else:
					direita = self.verificaSeExisteIrmao(pai,pag)
					if direita:
						pagReturn,chave = self.juntarNo(pai,pag,pai.filhos[pai.filhos.index(pag)+1])
					else:
						pagReturn,chave = self.juntarNo(pai,pai.filhos[pai.filhos.index(pag)-1],pag)
					return pagReturn,chave
		return None,None	


	# Método que remove nas paginas folhas, realizando também a junção das
	# paginas ou a troca com os irmãos 
	def removerFolha(self,pai,pag,valor):
		if valor in pag.chaves:
			pag.chaves.remove(valor)
		else:
			#print("Valor não Existe")
			return None, None
		if len(pag.chaves) >= int(self.tamanhoFolha/2):
			return None,None
		else:
			esquerda,direita = self.verificaIrmaoFolha(pai,pag)
			if esquerda:
					aux = max(pai.filhos[pai.filhos.index(pag)-1].chaves)
					pai.filhos[pai.filhos.index(pag)-1].chaves.remove(aux)
					pai.chaves[pai.filhos.index(pag)-1] = aux
					pag.chaves.insert(0,aux)
					return None,None
			elif direita:
				aux = min(pag.proximo.chaves)
				pag.proximo.chaves.remove(aux)
				pai.chaves[pai.filhos.index(pag)] = min(pag.proximo.chaves)
				pag.chaves.append(aux)
				return None,None
			else:
				direita = self.verificaSeExisteIrmao(pai,pag)
				if direita:
					pagReturn,chave = self.juntarNofolha(pai,pag,pai.filhos[pai.filhos.index(pag)+1])
				else:
					pagReturn,chave = self.juntarNofolha(pai,pai.filhos[pai.filhos.index(pag)-1],pag)
		return pagReturn,chave

	# Método que auxilia na junção das paginas folha
	def juntarNofolha(self,pai,pag_esq,pag_dir):
		pai.chaves.pop(pai.filhos.index(pag_esq))
		for i in pag_dir.chaves:
			pag_esq.chaves.append(i)
		pai.filhos.remove(pag_dir)
		pag_esq.proximo = pag_dir.proximo
		del pag_dir 
		return pag_esq,min(pag_esq.chaves)

	# Método que auxilia na junção das paginas não folha
	def juntarNo(self,pai,pag_esq,pag_dir):
		pag_esq.chaves.append(pai.chaves[pai.filhos.index(pag_esq)])
		pai.chaves.pop(pai.filhos.index(pag_esq))
		for i in pag_dir.chaves:
			pag_esq.chaves.append(i)
		for i in pag_dir.filhos:
			pag_esq.filhos.append(i)
		pai.filhos.remove(pag_dir)
		del pag_dir 
		return pag_esq,min(pag_esq.chaves)

	# Método que realiza a busca por igualdade 
	def buscaPorIgualdade(self,pag,valor):
		if pag.folha:
			for i in pag.chaves:
				if i == valor:
					print(valor)
					return 0
			print("valor não existe na arvore")
		else:
			flag = False
			for i in pag.chaves:
				if i > valor:
					self.buscaPorIgualdade(pag.filhos[pag.chaves.index(i)],valor)
					flag = True
					break
			if not flag:
				self.buscaPorIgualdade(pag.filhos[len(pag.filhos)-1],valor)

	# Método ajuda no printe dos valores do intervalo
	def printIntervalo(self,pag,valor_min,valor_max):
		flag = True
		flag2 = True
		while(flag):
			for i in pag.chaves:
				if i > valor_min:
					if i < valor_max:
						print(i," ")
						flag2 = False
					else:
						flag = False
			pag = pag.proximo
		return flag2

	# Método que realiza a busca por intervalo
	def buscaPorIntervalo(self,pag,valor_min,valor_max):
		flag = True
		if pag.folha:
			for i in pag.chaves:
				if i >= valor_min:
					flag = self.printIntervalo(pag,valor_min,valor_max)
			if flag:
				print("intervalo não existe")
		else:
			flag = False
			for i in pag.chaves:
				if i > valor_min:
					self.buscaPorIntervalo(pag.filhos[pag.chaves.index(i)],valor_min,valor_max)
					flag = True
					break
			if not flag:
				self.buscaPorIntervalo(pag.filhos[len(pag.filhos)-1],valor_min,valor_max)

	# Método que mostra a árvore inteira começando da raiz
	def mostrarArvore(self,pag):
		if not pag.folha:
			print(pag.chaves," Não folha")
			for i in range(len(pag.filhos)):
				self.mostrarArvore(pag.filhos[i])
		else:
			print(pag.chaves)
