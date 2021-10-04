"""
Author: Gabriel Chicote
"""
from typing import Dict, List
from pathlib import Path
import argparse, sys, os

# Create the parser
parser = argparse.ArgumentParser(
		description='Parse files from [.feature] format into [.e2e.js] format' )

# Define parser version
parser.version = 'Feature parser. version: 1.0'

# Add the arguments
parser.add_argument('Path',
					metavar='path',
					type=Path,
					nargs='+',
					help='Path to work with')
parser.add_argument('-d',
					'--dir',
					action='store_true',
					dest='directory',
					help='parses all files in specified directory')
parser.add_argument('-V',
					'--version',
					action='version',
					help='shows CLI version')

# Execute parse_args()
args = parser.parse_args()


def insert_header(output_file: str) -> None:
	""" Escribe en el archivo de salida un header y el import por default.
	"""

	output_file.write( "/*\n * Author: Gabriel Chicote\n */\n" )
	output_file.write( "\n// Add corresponding imports. Example:\nimport { describe } from 'jest-circus';\n" )
	output_file.write('\n')


def insert_feature_desc(output_file: str, feature: str, user_story: str) -> None:
	""" Escribe en el archivo de salida la descripcion del feature y las dos
	funciones por default para todos los archivos de test.
	"""

	output_file.write( f"describe( '{user_story} - {feature}', () => {'{'}\n\n" )
	output_file.write( "\tbeforeAll( () => {\n\t\tawait device.launchApp();\n\t} );\n\n" )
	output_file.write( "\tbeforeEach( () => {\n\t\tawait device.reloadReactNative();\n\t} );\n\n" )


def format_scenario(dicc: Dict[str, str]) -> str:
	""" Toma un diccionario de pares <Gherkin_keyword, texto>, formatea un
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
	

def insert_scenario(parts: Dict[str, str], output_file: str) -> None:
	""" Inserta un escenario, previamente formateado por 'format_scenario()',
	en el archivo de salida.
	"""

	output_file.write(format_scenario(parts))


def write_file(lines: List[str], output_file: str) -> None:
	""" Recorre y parsea las lineas del file, y escribe el resultado en el 
	output file cuando corresponda.
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


def prepare_input_file(input_file: str, output_file: str) -> None:
	""" Abre el archivo de lectura limpia las lineas que se van a usar y
	delega el trabajo de parseo y insertado a 'parse_lines()'
	"""

	with open(input_file, 'r') as f:
		write_file(
			list(filter( lambda x: x != '' , map(str.strip, f.readlines()))),
			output_file
		)


def prepare_output_file(input_file: str, output_dir: str) -> None:
	""" Crea y guarda un archivo de salida para el archivo de entrada.
	"""

	n = 0
	output_file_name = "{}{}.e2e.js"

	while (
		os.path.isfile(
			os.path.join(
				output_dir,
				output_file_name.format(
					os.path.basename(input_file).split('.')[0],
					'' if n == 0 else '_{}'.format(n)
				)
			)
		)
	):
		n += 1
	output_path = os.path.join( output_dir, output_file_name.format( os.path.basename(input_file).split('.')[0], '' if n == 0 else '_{}'.format(n) ) )
	prepare_input_file( input_file, output_path )


def parse_n_files(paths: List[str] ) -> None:
	""" Crea y guarda un archivo final para cada archivo parametro.
	"""

	output_dir = create_dir( os.path.split(str(paths[0]))[0] ) 
	for file_path in paths:
		prepare_output_file( file_path, output_dir )


def parse_all_files_in_dir(dir: str) -> None:
	""" Crea y guarda un archivo final para cada archivo del directorio dado.
	"""

	output_dir = create_dir(dir)
	files = filter(
				lambda f: os.path.isfile(f) and os.path.basename(f).startswith("US") and os.path.basename(f).endswith(".feature"),
				map( lambda x: os.path.join(dir, x), os.listdir(dir) )
			)
	for file in files:
		prepare_output_file( file, output_dir )


def create_dir(dir: str) -> None:
	""" Crea el directorio 'step_definitions' si este no existe.
	"""

	output_dir = 'step_definitions'
	if not os.path.exists(os.path.join(dir, output_dir)):
		os.mkdir( os.path.join(dir, output_dir) )
	return os.path.join(dir, output_dir)



def main() -> None:

	if args.directory:
		if not os.path.isdir( args.Path[0] ):
			sys.exit(f"Error! {args.Path} is not a directory.")
		elif len( args.Path ) > 1:
			sys.exit(f"Error! Only one directory is accepted.")
		parse_all_files_in_dir( args.Path[0] )
	else:
		for file in args.Path:
			if not os.path.isfile( file ):
				sys.exit(f"Error! {file} is not a file.")
		parse_n_files( args.Path )




if __name__ == "__main__":
	main()

