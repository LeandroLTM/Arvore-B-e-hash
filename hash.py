class Pag(object):   # Classe que define as páginas da hash
	def __init__(self):
		
		self.chaves = []
		self.over = None

class hash(object):   # Classe com os atributos da hash e seus métodos
	def __init__(self,tamanho,quantidade):
		self.bucket = [Pag(),Pag(),Pag(),Pag()]
		self.tamanho = int(tamanho/(quantidade*28))
		self.h0 = 4 
		self.h1 = 8
		self.proximo = 0

    # Método que calcula qual a pagina do valor passado.
	def h(self,valor):
		if self.proximo <= valor % self.h0 < self.h0:
			return valor % self.h0
		else:
			return valor % self.h1

	# Método que auxilia na inserção, quando tem overflow
	def over(self,valor,pag):
		if len(pag.chaves) < self.tamanho:
			pag.chaves.append(valor)
		elif pag.over:
			self.over(valor,pag.over)
		else:
			pag.over = Pag()
			self.over(valor,pag.over)		

	# Método para inserção de um valor, movimenta o próximo e cria outras 
	# paginas pro bucket, além de mudar a função h0 e h1. 
	def inserir(self,valor):
		resto = self.h(valor)
		if len(self.bucket[resto].chaves) < self.tamanho:
			self.bucket[resto].chaves.append(valor)
		else:
			self.over(valor,self.bucket[resto])
			self.bucket.append(Pag())
			aux = list()
			aux = self.bucket[self.proximo].chaves[:]
			aux_over = self.bucket[self.proximo].over
			self.bucket[self.proximo].chaves = list()
			self.bucket[self.proximo].over = None
			if self.proximo < self.h0:
				self.proximo = self.proximo + 1
			else:
				self.proximo = 0
				self.h0 = self.h1
				self.h1 = self.h1 + self.h1
			for chaves in aux:
				self.inserir(chaves)
			while aux_over:
				for chaves in aux_over.chaves:
					self.inserir(chaves)
				aux_over = aux_over.over

	# Método que auxilia na remoção quando acontece overflow.
	def remover_over(self,valor,pag):
		
		if valor in pag.chaves:
			pag.chaves.remove(valor)
			if len(pag.chaves) == 0:
				return True
		elif pag.over:
			if(self.remover_over(valor,pag.over)):
				pag.over = None
		else:
			#print("Valor nao existe")
			pass

	# Método de remoção de um valor informado.
	def remover(self,valor):
		resto = self.h(valor)
		if valor in self.bucket[resto].chaves:
			self.bucket[resto].chaves.remove(valor)
		else:
			self.remover_over(valor,self.bucket[resto])
	
	# Método que auxilia na pesquisa quando tem overflow
	def pesquisa_over(self,valor,pag):
		if pag:
			if valor in pag.chaves:
				print("Valor ",valor," encontrado! ")
			else:
				self.pesquisa_over(valor,pag.over)
		else:
			print("Valor não existe!!")

	# Método que pesquisa um valor na hash
	def pesquisa(self,valor):
		resto = self.h(valor)
		if valor in self.bucket[resto].chaves:
			print("Valor ",valor," encontrado! ")
		else:
			self.pesquisa_over(valor,self.bucket[resto].over)

	# Método que mostra todas as chaves da hash
	def mostrar(self):
		for pag in self.bucket:
			while pag:
				print(pag.chaves," ",end="")
				pag = pag.over
			print()