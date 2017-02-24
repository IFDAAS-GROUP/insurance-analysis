#!/usr/bin/python

import pandas as pd
import numpy as np
import sys

sys.path.insert(0, '../lib')
import DatabaseMethods as dbm


def PlotDataFromFile(seguradoraId):
    
    import matplotlib.pyplot as plt
    
    seguradoraName = dbm.GetAccountLabel(seguradoraId)
    
    # Le o dataframe
    df = pd.read_csv('%s/%s.csv' % (seguradoraName, seguradoraName))
    
    # Elimina colunas com NaNs
    df = df.dropna(axis = 'columns',\
        how = 'all')

    
    # Calcula a frequencia de aparicao das...
    #...palavras nos documentos
    words = []
    words_freq = []
    for row in df.index:
        
        occurencies = 0
        
        for column in df.columns[1:]:
            occurencies += df[column][row]
        
        words += [df['Unnamed: 0'][row],]
        words_freq += [occurencies,]
        
    # Cria pares com as palavras e suas frequencias
    zipped = zip(words, words_freq)
    
    # Ordena de modo decrescente as palavras de acordo...
    #...com as frequencias
    zipped_sorted = sorted(zipped, key = lambda t: t[1],\
        reverse = True)
    
    # Array com os dados
    data = np.array([_[1] for _ in zipped_sorted])
    data_labels = [_[0] for _ in zipped_sorted]
    
    # Encontra os quartis e a mediana
    q1, medians, q3 = np.percentile(data, [25, 50, 75])
    
    print q1, medians, q3
    
    # Desenha o grafico de barras palavras por ocorrencias
    plt.figure(1)
    plt.bar(np.arange(len(data_labels)),\
            data,\
            align = 'center',\
            alpha = 0.5)
    
    plt.xlabel('Palavras')
    plt.ylabel('Ocorrencias')
    plt.title('Ocorrencia das palavras nos documentos da seguradora %s'\
        % seguradoraName)
    plt.savefig('%s/%s_ocorrenciaPalavras.png'\
        % (seguradoraName, seguradoraName))    
    plt.close()
    
    # Desenha o boxplot
    plt.figure(2)
    plt.title('Boxplot da seguradora %s'\
        % seguradoraName)
    bp = plt.boxplot(data)
    plt.savefig('%s/%s_boxplot.png'\
        % (seguradoraName, seguradoraName))
    plt.close()
    
    # Desenha o violin PlotDataFromFile
    plt.figure(3)
    plt.title('Densidade e ocorrencia dos termos nos documentos da seguradora %s'\
        % seguradoraName)
    plt.xlabel('Densidade')
    plt.ylabel('Ocorrencias')
    plt.violinplot(data,\
        showmeans = True,\
        showmedians = True,\
            showextrema = True)
    plt.savefig('%s/%s_violinplot.png'\
        % (seguradoraName, seguradoraName))
    
    CutFile(q1, q3, zipped, df, seguradoraName)
    
    plt.close()
    
def CutFile(quartile1, quartile3, data, df, label):
    
    print 'cutting %s file' % label
    
    sequence_to_remove = []
    
    for i, _ in enumerate(data):
        if _[1] < quartile3:
            sequence_to_remove += [i,]
    
    df = df.drop(df.index[sequence_to_remove])
    
    sequence_to_remove = []
    for c in df.columns:
        if c != 'Unnamed: 0':
            acc = 0.
            for r in df.index:
                acc += df[c][r]
            if acc == 0.:
                print c, ' removed'
                #sequence_to_remove += [c,]
                df = df.drop(c, axis = 1)
    
    df.to_csv('%s/%s_sliced.csv'\
        % (label, label))
    
seguradoraIduradoras = dbm.GetAllSeguradoras()

for seguradoraId in seguradoraIduradoras:
    
    #quartile1 = 20#int(input("\t\tInforme o corte minino: "))
    #quartile3 = 25#int(input("\t\tInforme o corte maximo: "))
    try:
        PlotDataFromFile(seguradoraId)
        #cut_file(seguradoraId, quartile1, quartile3)
    except(IOError):
        next
    except(KeyError), e:
        with open("ERR.txt", "w") as arq:
            arq.write("\n[KeyError cortanto o arquivo]\n")
        print "\t\tErro redimensionando os dados..."
        print e
    print "\t\tCorte gerado"
    
