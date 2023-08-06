import fitz, re
import xlsxwriter

def pantalla(words):
    for i in range (len(words)):
        if ( words[i][4] != '.' and words[i][4] != '..' and words[i][4] != '*' ):
            print (words[i])

def get_text(words):
    text = []
    tabla = []
    word =""
    
    for i in range (len(words)):
        if ( words[i][4] != '.' and words[i][4] != '..' and words[i][4] != '*' ):
                
            if (words[i][7] != 0):
                    word = word + " " + words[i][4] 
                   
                        
            else:
                text.append(word)
                word = words[i][4]
                if (words[i][6] == 0):
                    tabla.append(text)
                    text = []
   
    tabla.append(text)
    return tabla

file = fitz.open("Fuentes de datos\Smarcities\Valor Bosque Urbano de Madrid.pdf")
page = file[44]

words = page.get_text("words")

print (pantalla(words))
tabla = get_text(words)
print (tabla)
