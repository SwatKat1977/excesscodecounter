'''
Extensible Code Counter System [EXCESS]
Copyright (C) 2017 Paul Morriss

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
import argparse
import os
from LineCount import *

		
def main():
	argsParser = argparse.ArgumentParser()
	
	# 'Optional Arguments' : 'language'.
	argsParser.add_argument('-l', '--language', required = True, 
		help = 'Programming language files to process.')

	# 'Optional Arguments' : 'recursive'.
	argsParser.add_argument('-r', '--recursive', action="store_true",
		help = 'Flag to specify if to recurse sub directories.')
		
	# 'Optional Arguments' : 'verbose'.
	argsParser.add_argument('-v', '--verbose', action="store_true",
		help = 'Flag to specify if to display verbose text.')

	# 'Positional Arguments' : 'path to start from'.
	argsParser.add_argument('path', help ='Root to search from')
	
	# Parse the arguments.
	args = argsParser.parse_args()

	# Check if the specified directory is valid.
	if os.path.isdir(args.path) == False:
		print("[ERROR] Path '{0}' isn't valid.".format(args.path))
		sys.exit(2)

	try:
		fileProcessorModule = __import__(args.language)
		fileProcessorClass = getattr(fileProcessorModule, args.language)
		fileProcessor = fileProcessorClass()

	except ImportError as ie:
		print("[EXCEPT CAUGHT] {0}".format(ie))
		sys.exit(2)

	except AttributeError as ae:
		print("[EXCEPT CAUGHT] {0}".format(ae))
		sys.exit(2)	

	lc = LineCount(fileProcessor, args)
	lc.ProcessFilesInDir(args.path)
		

if __name__ == "__main__":
	main()
	sys.exit()