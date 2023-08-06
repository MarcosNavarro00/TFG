

import fitz, re
import xlsxwriter



"""""
pdf_path = "Fuentes de datos\Eulogh\incendios-decenio-2006-2015_tcm30-521617.pdf"
df = tabula.read_pdf(pdf_path, pages= '49')
print (df)

35.72410202026367, 81.87679290771484, 91.40410614013672, 96.27679443359375
35.72410202026367, 81.87679290771484, 91.40410614013672, 96.27679443359375,
with pdfplumber.open("Fuentes de datos\Smarcities\Valor Bosque Urbano de Madrid.pdf") as pdf:
    
    page = pdf.pages[72]
    table = page.extract_table()
    print(table)
df = pd.DataFrame(table[1:], columns=table[0])
for column in ["Especie", "Cantidad", "Porcentaje \nPoblación"]:
    df[column] = df[column].str.replace(" ", "")

print(df)
"""""

book =  []

file = fitz.open("Fuentes de datos\Smarcities\CATALOGO DE PARQUES MUNICIPALES MADRID_BAJA RESOLUCIÓN 03.08.2021.pdf")

print(file)
#----------------------------------- Extrae todo el texto por pagina del pdf -----------------------------------------
def get_text(words):
    lista = [658.5527954101562, 746.0987548828125, 767.6507568359375, 778.4267578125, 800.9547729492188, 735.32275390625, 652.4848022460938, 663.2608032226562, 722.2672119140625, 733.043212890625, 646.4297485351562,
    756.874755859375, 674.0368041992188, 826.19970703125, 809.2657470703125, 799.8308715820312,790.2230224609375, 770.2509765625, 548.1847534179688, 500.9808044433594,479.38580322265625, 670.67578125, 
    682.7987670898438, 663.8447875976562, 656.0878295898438, 684.3748168945312, 703.2327880859375, 722.0908203125, 740.9487915039062, 665.5167846679688, 673.2738037109375, 674.94580078125, 731.5198364257812,
    693.8038330078125, 712.6618041992188]
    text = []
    word =""
    #
    for i in range (len(words)):
        if ( words[i][4] != '.' and words[i][4] != '..' and words[i][4] != '*' ): #quita los puntos y asteriscos
            if (words[i][1] not in lista): #comprueba que estan las coordenadas de informacion no relevante
                if (words[i][7] != 0):
                    word = word + " " + words[i][4]
                    
                else:
                    text.append(word)
                    word = words[i][4]
   
    return text #devuelve el texto con cadenas unidas limpiado del pdf


#----------------------------------- Obtiene la informacion a partir de las coordenas -----------------------------------------
def get_codes (file):
    codes = []
    for i in range (len (file)):
        page = file[i]
        words = page.get_text("words")
    
        coor_code = (491.0459899902344, 587.2937622070312, 531.7529907226562, 598.09375)
        code = page.get_text("text", clip=coor_code)
  
        if len(code):
            codes.append(code)
    return codes


def clean (texto):
    for i in range (67):#se borra lo que no es necesario
        texto.pop(0)
   
    texto = [texto[0],texto[2],texto[5],texto[4],texto[6],texto[1],texto[3],texto[7],texto[8],texto[9],texto[10],texto[11],texto[12],texto[13],texto[14],texto[15],texto[16],#16
    texto[17],texto[18],texto[19],texto[21],texto[24],texto[29],texto[32],texto[35],texto[37],texto[39],
    texto[41],texto[43],texto[46],texto[48],texto[50],texto[52],texto[54],texto[22],texto[25],texto[30],texto[26],texto[27]
    ,texto[33],texto[44],
    ]
    
    #Es bic 23, red de miradores 26, pradera 27, Césped 28, Micro reserva biodiversidad 31, Nº total de unidades arbóreas 34, 45 Superficie de macizos arbustivos:, 
    for i in range(len (texto)):
        if ('m²' in texto[i]):#se quitan el % para poder trabajar con los datos 
            texto[i]= texto[i].replace('m²', '')
        if ('ud' in texto[i]):#se quitan el % para poder trabajar con los datos 
            texto[i]= texto[i].replace('ud', '')
        if ('.' in texto[i]):#se quitan el . para poder trabajar con los datos
            texto[i] = texto[i].replace('.', '')
        if (',' in texto[i]):#se quitan el , para poder trabajar con los datos 
            texto[i]= texto[i].replace(',', '.')
        if ('km' in texto[i]):#se quitan el , para poder trabajar con los datos 
            valor= texto[i].replace('km', '')
            texto[i] = float(valor)*1000
            
    print (texto)
    return texto

#----------------------------------- Exporta la data a un archivo xlsx -----------------------------------------
def export_xlsx(tablas):
    
    csv_columns = ['Código','Nombre de parque','Distrito', 'Barrio','Dirección','Tipología', 'Superﬁcie', 'Transporte Metro','Cercanías RENFE','Transporte Bus','Aparcamiento',
    'Eventos deportivos', 'Ferias temácas', 'Educavo/divulgavo', 'Festejos y celebraciones','Espectáculos', 'Rodaje audiovisual','Grandes espacios abiertos',
    'Vistas panorámicas','Accesibilidad parques', 'Zonas infantiles', 'Zonas de mayores', 'Área canina','Fuente ornamental', 'Estanque/Lámina agua','Instalaciones deportivas','Auditorio','Senda Ecológica',
    'Carril bici','Aseo público','Mirador','Jardín Botánico','Bancos','Papeleras','Es BIC','Red de miradores','Micro reserva biodiversidad','Pradera natural','Césped',
    'Nº total de unidades arbóreas','Superficie de macizos arbustivos'
    ]
    if (tablas[0] != csv_columns):#puede que ya esten introducida la cabecera
        tablas.insert(0,csv_columns)
    
    
    workbook = xlsxwriter.Workbook('sample_data4.xlsx')
    sheet = workbook.add_worksheet()
    
    for row in range (len(tablas)):
        for column in range (len(tablas[row])):
            sheet.write((row), column, tablas[row][column])
    
    
    workbook.close()

#----------------------------------- Imprime el texto por pantalla con todos los atributos -----------------------------------------
def pantalla(words):
    lista = [658.5527954101562, 746.0987548828125, 767.6507568359375, 778.4267578125, 800.9547729492188, 735.32275390625, 652.4848022460938, 663.2608032226562, 722.2672119140625, 733.043212890625, 646.4297485351562,
    756.874755859375, 674.0368041992188, 826.19970703125, 809.2657470703125, 799.8308715820312,790.2230224609375, 770.2509765625, 548.1847534179688, 500.9808044433594]
    for i in range (len(words)):
        if ( words[i][4] != '.' and words[i][4] != '..' and words[i][4] != '*' ):
            if (words[i][1] not in lista):
                print (i, words[i])



def empezar ():
    textos = []
  
    for i in range(len(file)-8):#a partir de la pagina 7, que es donde empieza la informacion 
        texto = ""
        if ((7+i) % 2 != 0): #numero par, porque la info solo se encuentra en paginas impares
            
            page = file[7+i]
            words = page.get_text("words") #obtiene las palabras de una pagina del pdf
            #pantalla(words)
            texto = get_text(words)
            print (i, "\n")
            
            if (i!=176 and i!=186 ):
                texto = clean(texto)
                                
                textos.append(texto)
            #print (texto, "\n")
            
    
    export_xlsx(textos)

empezar ()


def unaPagian():
    page = file[185]
    words = page.get_text("words") #obtiene las palabras de una pagina del pdf
    pantalla(words)
    texto = get_text(words)
    texto = clean(texto)
    print (texto)

#unaPagian()











