
import fitz
import xlsxwriter



def pantalla(words):
    lista = [658.5527954101562, 746.0987548828125, 767.6507568359375, 778.4267578125, 800.9547729492188, 735.32275390625, 652.4848022460938, 663.2608032226562, 722.2672119140625, 733.043212890625, 646.4297485351562,
    756.874755859375, 674.0368041992188, 826.19970703125, 809.2657470703125, 799.8308715820312,790.2230224609375, 770.2509765625, 548.1847534179688, 500.9808044433594]
    for i in range (len(words)):
        if ( words[i][4] != '.' and words[i][4] != '..' and words[i][4] != '*' ):
            if (words[i][1] not in lista):
                print (i, words[i])



def getByCoor ( page ):
   
    element = ""
    words = page.get_text("words")
    for i in range (len(words)):
        if ( words[i][4] != '.' and words[i][4] != '..' and words[i][4] != '*' ):
            if (words[i][1]== coor):
                element = element + " " + words[i][4]


    
    print (element)
    if len(element):
        return element
    

#----------------------------------- Exporta la data a un archivo xlsx -----------------------------------------
def export_csv(tablas):
    
    csv_columns = ['Código','Nombre de parque','Distrito', 'Barrio','Dirección','Tipología', 'Superﬁcie', 'Transporte Metro','Cercanías RENFE','Transporte Bus','Aparcamiento'
    'Eventos deportivos', 'Ferias temácas', 'Educavo/divulgavo', 'Festejos y celebraciones','Espectáculos', 'Rodaje audiovisual','Grandes espacios abiertos',
    'Vistas panorámicas', 'Fecha Creación', 'Fecha Reforma', 'Accesibilidad parques', 'Zonas infantiles', 'Unidades', 'Zonas de mayores', 'Unidades', 'Área canina', 'Unidades','Fuente ornamental'
    'Unidades','Estanque/Lámina agua','Unidades','Instalaciones deportivas','Unidades','Auditorio','Unidades','Senda Ecológica', 'Unidades','Carril bici','Unidades','Aseo público','Unidades',
    'Mirador','Unidades','Jardín Botánico','Unidades','Bancos','Unidades','Papeleras','Unidades','Fuente de beber','Unidades','Es BIC','Red de miradores','Micro reserva biodiversidad'
    'Pradera natural','Césped','Nº total de unidades arbóreas','Superficie de macizos arbustivos'
    ]
    if (tablas[0] != csv_columns):#puede que ya esten introducida la cabecera
        tablas.insert(0,csv_columns)
    
    
    workbook = xlsxwriter.Workbook('sample_data4.xlsx')
    sheet = workbook.add_worksheet()
    
    for row in range (len(tablas)):
        for column in range (len(tablas[row])):
            sheet.write((row), column, tablas[row][column])
    
    
    workbook.close()


def empezar ():
    
    file = fitz.open("Fuentes de datos\Smarcities\CATALOGO DE PARQUES MUNICIPALES MADRID_BAJA RESOLUCIÓN 03.08.2021.pdf") #se abre el documento 

    text = []
    elements = []
    #coordenadas de los elementos importantes del pdf
    #Codigo, Nombre, Distrito, Barrio, Dirrecion 
    coors [81.87679290771484, 81.6767807006836, 108.54875946044922, 106.0367660522461, 130.91275024414062, 130.91275024414062] 
  
    for i in range(len(file)-8):#a partir de la pagina 7, que es donde empieza la informacion 
        texto = ""
        if ((7+i) % 2 != 0): #numero par, porque la info solo se encuentra en paginas impares
            
            page = file[7+i]
            
            #pantalla(words)
            for i in range (len(coors)):
                element = getByCoor ( page, coor )
                elements.append(element)

            text.append(elements)
            


            print (i, "\n")
            
            
    
    export_csv(textos)

def unaPagian():
    file = fitz.open("Fuentes de datos\Smarcities\CATALOGO DE PARQUES MUNICIPALES MADRID_BAJA RESOLUCIÓN 03.08.2021.pdf") #se abre el documento 
    page = file[31]
    words = page.get_text("words") #obtiene las palabras de una pagina del pdf
    pantalla(words)
    getByCoor ( page )
   

unaPagian()