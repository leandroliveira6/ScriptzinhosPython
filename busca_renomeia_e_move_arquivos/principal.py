import os

def renomear_arquivos(n):
    for item in os.listdir('.'):
        print('*'*n, item)
        if(os.path.isdir(item)):
            os.chdir(item)
            renomear_arquivos(n+1)
        else:
            if(item.find('[')>-1):
                os.rename(item, item.replace('[', '').replace(']', ''))
    os.chdir('..')
    
def mover_arquivos(n):
    for item in os.listdir('.'):
        if(os.path.isdir(item)):
            print('*'*n, item)
            if(item in lista_pastas_interessadas):
                destino = os.path.abspath('.')
                indice_interesse = lista_pastas_interessadas.index(item)
                origem = destino + '\\'+lista_pastas_interessadas[indice_interesse]
                comando = 'move /Y {} {} & rmdir {}'.format(origem+'\*.*', destino, origem)
                print(comando)
                os.system(comando)
            else:
                os.chdir(item)
                mover_arquivos(n+1)
    os.chdir('..')

diretorio_inicial = 'D:\\Testes'
os.chdir(diretorio_inicial)

renomear_arquivos(0)

lista_pastas_interessadas = ['PastaTeste1', 'PastaTeste2']
mover_arquivos(0)

print('fim')