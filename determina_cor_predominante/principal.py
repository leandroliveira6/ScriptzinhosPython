from os import path
import numpy as np
from sklearn.cluster import KMeans
from PIL import Image
import threading
from flask import Flask, request, redirect, render_template
from werkzeug.utils import secure_filename



## Servidor web
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

cores_escolhidas = {}
caminho_imagem = ''
cor_dominante_hex = ''
cor_escolhida_familiar = ''

#### Funções principais
@app.route("/", methods=['POST', 'GET'])
def principal():
    return render_template('principal.html', coresEscolhidas=cores_escolhidas, caminhoImagem=caminho_imagem, corDomimante=cor_dominante_hex, corEscolhida=cor_escolhida_familiar)

@app.route('/salvarCores', methods=['POST'])
def salvar_cores():
    cores_escolhidas.update(request.form.to_dict())
    atualizarEspacoCores(cores_escolhidas)
    return redirect('/')

@app.route('/determinarCor', methods=['POST'])
def determinar_cor():
    # salva o arquivo no disco
    caminhos = carregar_arquivos(request.files)

    global caminho_imagem
    caminho_imagem = caminhos[0]
    print(caminho_imagem)

    # carrega o arquivo como uma lista de rgbs
    imagem = Image.open(caminho_imagem)

    # determina o rgb dominante
    rgb_dominante = obterCorPredominante(imagem)
    global cor_dominante_hex
    cor_dominante_hex = rgb2hex(rgb_dominante)

    if(cores_escolhidas):
        indice_cor_familiar = espaco_cores.predict(np.array([rgb_dominante]))
        rgb_familiar = espaco_cores.cluster_centers_[indice_cor_familiar]
        if(rgb_familiar.any()):
            rgb_familiar = rgb_familiar[0]
            hex_familiar = rgb2hex(rgb_familiar)
            cor_escolhida = list(cores_escolhidas.keys())[list(cores_escolhidas.values()).index(hex_familiar)]
            global cor_escolhida_familiar
            cor_escolhida_familiar = 'A cor dominante é bem '
            distancia = obterDistancia(rgb_dominante, rgb_familiar)
            print('Distancia', distancia)
            if(distancia<140):
                cor_escolhida_familiar += 'parecida com a cor {}'.format(cor_escolhida)
            else:
                cor_escolhida_familiar += 'diferente das cores escolhidas'

    return redirect('/')

def iniciar_servidor():
    app.run(port=5000, debug=False)

#### Funções auxiliares
def carregar_arquivos(arquivos):
    caminhos = []
    for nome in arquivos:
        nome_seguro = secure_filename(arquivos[nome].filename)
        caminho_arquivo = path.join(app.config['UPLOAD_FOLDER'], nome_seguro)
        arquivos[nome].save(caminho_arquivo)
        caminhos.append(caminho_arquivo)
    return caminhos

def dicionarioHexParaRgb(cores_em_hex):
    cores_em_rgb = {}
    for k, v in cores_em_hex.items():
        cores_em_rgb[k] = hex2rgb(v)
    return cores_em_rgb

def hex2rgb(hexadecimal):
    hexadecimal = hexadecimal[1:] # remove a hashtag da string
    return [int(hexadecimal[:2], 16), int(hexadecimal[2:4], 16), int(hexadecimal[4:], 16)]

def rgb2hex(rgb):
    hexadecimal = '#'
    for d in rgb:
        hexadecimal+='{:02x}'.format(int(d))
    return hexadecimal



## Determinar cores
espaco_cores = KMeans(n_clusters=6)

def atualizarEspacoCores(cores_em_hex):
    cores_em_rgb = dicionarioHexParaRgb(cores_em_hex)
    print(cores_em_rgb)
    espaco_cores.fit(list(cores_em_rgb.values()))

def obterDistancia(cor1, cor2):
    total = 0
    for i in range(3):
        total+=(cor1[i]-cor2[i])**2
    return total**(1/2)

def obterCorPredominante(imagem):
    cores = np.reshape(np.asarray(imagem), (-1,3))
    kmeans = KMeans(n_clusters=3)
    kmeans.fit(cores)
    indice_cor_predominante = np.argmax(np.bincount(kmeans.labels_))
    cor_predominante = kmeans.cluster_centers_[indice_cor_predominante]
    return cor_predominante


## Principal
servidor = threading.Thread(target=iniciar_servidor)
servidor.start()