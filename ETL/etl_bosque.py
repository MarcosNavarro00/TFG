import fitz, re
import xlsxwriter

file = fitz.open("Fuentes de datos\Smarcities\Valor Bosque Urbano de Madrid.pdf")



#----------------------------------- Imprime la tabla por pantalla con solo su str -----------------------------------------
def pantallaDir (tabla):
    for i in range(len (tabla)):
        print(tabla[i], "\n")

#----------------------------------- Imprime el texto por pantalla con todos los atributos -----------------------------------------
def pantalla(words):
    for i in range (len(words)):
        if ( words[i][4] != '.' and words[i][4] != '..' and words[i][4] != '*' ):
            print (words[i])

#----------------------------------- Exporta los datos a un csv-----------------------------------------
def export_xlsx(tablas):
   
    csv_columns = ['Especie', 'Cantidad', 'Porcentaje Población', 'Area Foliar (M2)', 'Porcentaje Área Foliar', 'Biomasa Foliar (Kg)', 'Dominancia', 'Almacén De Carbono (Tn)',
    'Secuestro Carbono (Tn/Año)', 'Captación Contaminación (Kg/Año)', 'Producción Oxígeno (Tn/Año)', 'Agua Interceptada (M3/Año)', 'Escorrentía Evitada (M3/Año)', 
    'Evaporación Potencial (M3)', 'Evaporación (M3)', 'Transpiración (M3)', 'Isoprenos (G/Año)', 'Monoterpenos (G/Año)', 'Voc'
    ]
    if (tablas[0] != csv_columns):#puede que ya esten introducida la cabecera
   
        tablas.insert(0,csv_columns) #se meten el nombre de las columnas en la cabecera
    
    tablas.pop(len(tablas)-1)
    workbook = xlsxwriter.Workbook('prueba.xlsx')
    worksheet = workbook.add_worksheet()
    
    for row_num, row_data in enumerate(tablas):
        for col_num, col_data in enumerate(row_data):
            worksheet.write(row_num, col_num, col_data)
    
    workbook.close()
   
  
#----------------------------------- Limpia los datos -----------------------------------------
def clean (tabla):
    if (tabla[1][1] == '64'):#se borran mas elementos ya que en la primera pagina hay mas 
        for i in range (4):#se borran los dos primeros que es el titulo y numero de pagina
            tabla.pop(0)
    else:
        for i in range (2):#se borran los dos primeros que es el titulo y numero de pagina
            tabla.pop(0)
        
    for i in range (8):#se borran los 8 ultimos que son las primeras columnas
        tabla.pop(len(tabla)-1)
    
    
    for i in range(len (tabla)): #se concatenan los nombres sueltos con los valores y se borran los valores duplicados
        if (len (tabla) > i): #como se van restando miembros de la lista el i puede ser mayor que el tamaño por lo que es un error 
            if (len(tabla[i]) <= 5):
                #print (i,tabla[i] )
                tabla[i] = [tabla[i][0] + " " + tabla[i][1]] + tabla[i+1]
                tabla.pop(i+1)

    for i in range(len (tabla)):
        for j in range(len (tabla[i])):
            if ('%' in tabla[i][j]):#se quitan el % para poder trabajar con los datos 
                tabla[i][j] = tabla[i][j].replace('%', '')
                print (tabla[i][j], '\n')
            if ('.' in tabla[i][j]):#se quitan el . para poder trabajar con los datos
                tabla[i][j] = tabla[i][j].replace('.', '')
            if (',' in tabla[i][j]):#se quitan el , para poder trabajar con los datos 
                tabla[i][j] = tabla[i][j].replace(',', '.')
   
    return tabla


#----------------------------------- Extrae la palabras del pdf formando una tabla -----------------------------------------
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

tablas = []
for i in range (12): #12 paginas con tablas
    page = file[63+i]
    words = page.get_text("words")
    image= page.get_images()
    tabla = get_text(words)
    
    tabla =clean (tabla)
    
    tablas = tablas + tabla #se unen el texto de las diferentes paginas 
    #print ( pantallaDir (tablas))
    export_csv(tablas)


