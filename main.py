from bmais import Bmais # importe da classe da arvore B+
from hash import hash
import csv # importe da classe de leitura de arquivo CSV
import time
import matplotlib.pyplot as plt

def execucao_arvore(pag_tam,pag_quant): # Método de execução da arvore 
	arquivo = open('dados.csv')
	linhas = csv.reader(arquivo)
	ini = time.time()
	auxarvore = Bmais(pag_tam,pag_quant)
	for linha in linhas:
		if linha[0] =='+':
			auxarvore.insereRaiz(auxarvore.raiz,int(linha[1]))
	linhas = csv.reader(arquivo)
	for linha in linhas:
		if linha[0] =='-':
			auxarvore.removerRaiz(auxarvore.raiz,int(linha[1]))
	fim = time.time()
	arquivo.close()
	return (fim-ini)

def execucao_hash(pag_tam,pag_quant): # Método de execução da hash
	arquivo = open('dados.csv')
	linhas = csv.reader(arquivo)
	ini = time.time()
	auxhash= hash(pag_tam,pag_quant)
	for linha in linhas:
		if linha[0] =='+':
			auxhash.inserir(int(linha[1]))
	linhas = csv.reader(arquivo)
	for linha in linhas:
		if linha[0] =='-':
			auxhash.remover(int(linha[1]))
	fim = time.time()
	arquivo.close()
	return (fim-ini)

def execucao_arvore2(pag_tam,pag_quant,nome,flag):  # Método de execução da arvore com escolha de 
	arquivo = open('dados'+str(nome)+'.csv')        # do arquivo que dados e de inserções ou remoções
	linhas = csv.reader(arquivo)
	ini = time.time()
	auxarvore = Bmais(pag_tam,pag_quant)
	if flag:
		for linha in linhas:
			if linha[0] =='+':
				auxarvore.insereRaiz(auxarvore.raiz,int(linha[1]))
	else:
		for linha in linhas:
			if linha[0] =='-':
				auxarvore.removerRaiz(auxarvore.raiz,int(linha[1]))
	fim = time.time()
	arquivo.close()
	return (fim-ini)

def execucao_hash2(pag_tam,pag_quant,nome,flag):  # Método de execução da hash com escolha de 
	arquivo = open('dados'+str(nome)+'.csv')      # do arquivo que dados e de inserções ou remoções
	linhas = csv.reader(arquivo)
	ini = time.time()
	auxhash= hash(pag_tam,pag_quant)
	if flag:
		for linha in linhas:
			if linha[0] =='+':
				auxhash.inserir(int(linha[1]))
	else:
		for linha in linhas:
			if linha[0] =='-':
				auxhash.remover(int(linha[1]))
	fim = time.time()
	arquivo.close()
	return (fim-ini)

def main():     # Método principal
	arvore_tempo = []
	hash_tempo = []
	y = []


	'''# codigo para execusão do teste de campos
	for i in range(4,33,4):
		aux = []
		for j in range(0,5):
			aux.append(execucao_arvore(2560,i))
		arvore_tempo.append(aux)
		print(aux)
		y.append(i)
	for i in range(4,33,4):
		aux1 = []
		for j in range(0,5):
			aux1.append(execucao_hash(2560,i))
		hash_tempo.append(aux1)
		print(aux1)
	'''
	'''# codigo para execusão do teste de tamanho de paginas
	for i in range(512,4097,512):
		aux = []
		for j in range(0,5):
			aux.append(execucao_arvore(i,15))
		arvore_tempo.append(aux)
		print(aux)
		y.append(i)
	for i in range(512,4097,512):
		aux1 = []
		for j in range(0,5):
			aux1.append(execucao_hash(i,15))
		hash_tempo.append(aux1)
		print(aux1)              
	'''
	'''# codigo para execusão do teste de inserções
	i = 2000
	while (i < 512001):
		aux = []
		for j in range(0,5):
			aux.append(execucao_arvore2(1560,15,i,True))
		arvore_tempo.append(aux)
		print(aux)
		y.append(i)
		i *= 2
	i = 2000
	while (i < 512001):
		aux = []
		for j in range(0,5):
			aux.append(execucao_hash2(1560,15,i,True))
		hash_tempo.append(aux)
		print(aux)
		i *= 2
	
	'''

	# codigo para execusão do teste de tamanho de remoções
	execucao_arvore2(1560,15,512000,True)

	execucao_hash2(1560,15,512000,True)

	i = 2000
	while (i < 512001):
		aux = []
		for j in range(0,5):
			aux.append(execucao_arvore2(1560,15,i,False))
		arvore_tempo.append(aux)
		print(aux)
		y.append(i)
		i *= 2
	i = 2000
	while (i < 512001):
		aux = []
		for j in range(0,5):
			aux.append(execucao_hash2(1560,15,i,False))
		hash_tempo.append(aux)
		print(aux)
		i *= 2
	
	# calcular a media dos valores de teste
	media_arvore = []
	media_hash = []
	for i  in range(0,len(arvore_tempo)):
		media_arvore.append(sum(arvore_tempo[i])/len(arvore_tempo[i]))
	for i in range(0,len(hash_tempo)):
		media_hash.append(sum(hash_tempo[i])/len(hash_tempo[i]))
	print(media_arvore)
	print(media_hash)

	#plotar grafico
	plt.plot(y,media_arvore)
	plt.plot(y,media_hash)
	plt.grid(True)
	plt.title("Exemplo")
	plt.xlabel("x")
	plt.ylabel("y")
	plt.show()

	# gravar dados no arquivo cvs
	arquivo = open('salve.csv','a')
	for i in range(0,len(y)):
		aux1 = ""
		aux2 = ""
		for j in arvore_tempo[i]:
			if j == arvore_tempo[len(arvore_tempo)-1]:
				aux1 = aux1 + str(j)
			else:
				aux1 = aux1 + str(j)+","
		for j in hash_tempo[i]:
			if j == hash_tempo[len(hash_tempo)-1]:
				aux2 = aux2 + str(j)
			else:
				aux2 = aux2 + str(j)+","
		arquivo.write(str(y[i])+","+aux1+ str(media_arvore[i]) +","+aux2+ str(media_hash[i]) +"\n")
	arquivo.close()
	

if __name__ == '__main__':
	main()
