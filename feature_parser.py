import sys
import os


def insert_header(output_file):
    """
    Escribe en el archivo de salida un header y el import por default.
    """
    output_file.write( "/*\n * Author: Gabriel Chicote\n */\n" )
    output_file.write( "\n// Add corresponding import. Example:\nimport { describe } from 'jest-circus';\n" )
    output_file.write('\n')


def insert_feature_desc(output_file, feature, user_story):
    """
    Escribe en el archivo de salida la descripcion del feature y las dos
    funciones por default para todos los archivos de test.
    """
    output_file.write( f"describe( '{user_story} - {feature}', () => {'{'}\n\n" )
    output_file.write( "\tbeforeAll( () => {\n\t\tawait device.launchApp();\n\t} );\n\n" )
    output_file.write( "\tbeforeEach( () => {\n\t\tawait device.reloadReactNative();\n\t} );\n\n" )


def format_scenario(dicc):
    """
    Toma un diccionario con pares <Gherkin_keyword, texto>, formatea un
    step definition a partir del mismo y lo devuelve como cadena.
    """

    str = '''
    describe( '{}', () => {{ 

        const given = '{}'
        const when = '{}'
        const then = '{}'

        test( `${{given}}, ${{when}} ${{then}}`, async () => {{ 
            // TODO
        }})

    }} ); 
    '''.format(dicc['scenario'], dicc['given'], dicc['when'], dicc['then'])
    return str
    


def insert_scenario(dicc, output_file):
    """
    Inserta un escenario, previamente formateado por 'format_scenario()',
    en el archivo de salida.
    """
    output_file.write(format_scenario(dicc))





def parse_lines(lines, output_file):
    """
    Recorre las lineas del file y las parsea.
    """
    feature = ""
    user_story = ""
    parts = { 'scenario': ""
            , 'given': ""
            , 'when': ""
            , 'then': ""
    }

    with open(output_file, 'w') as f:

        # File header
        insert_header(f)

        for i in range(0, len( lines )):
            l = lines[i].split()
            if "Feature" in l[0]:
                feature = ' '.join( l[1:] )

            elif "US" in l[0]:
                user_story = l[0][:-1]
                insert_feature_desc(f, feature, user_story)

            elif "Scenario" in l[0]:
                parts['scenario'] = ' '.join( l[1:] )

            elif "Given" in l[0]:
                parts['given'] = ' '.join( l )

            elif "When" in l[0]:
                parts['when'] = ' '.join( l )

            elif "Then" in l[0]:
                parts['then'] = ' '.join( l )
                insert_scenario(parts, f)
                parts = parts.fromkeys(parts, "")

        # Llave y parentesis finales.
        f.write("\n});\n") 


def write_file(input_file, output_file):
    """
    Abre el archivo de lectura 
    limpia las lineas que se van a usar y
    delega el trabajo de parseo y insertado a 'parse_lines()'
    """
    with open(input_file, 'r') as f:
        parse_lines( list( filter( lambda x: x != ''
                                 , map( str.strip, f.readlines() )
                                 )
                         )
                   , output_file
        )



def main():
    input_file = sys.argv[1]
    output_file = "{}{}.e2e.js"

    n = 0
    while os.path.isfile(output_file.format(input_file.split('.')[0], '' if n == 0 else '_{}'.format(n))):
        n += 1
    
    output_file = output_file.format(input_file.split('.')[0], '' if n == 0 else '_{}'.format(n))

    write_file(input_file, output_file)






if __name__ == "__main__":
    main()

