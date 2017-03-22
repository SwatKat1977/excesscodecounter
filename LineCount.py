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
from __future__ import division
import os
import sys


class LineCount(object):
	
	def __init__(self, fileParser, args):
		self._fileParser = fileParser
		self._arguments = args


	def ProcessFilesInDir(self, pathDir):
		fileStats = False
		totalBlankLines = 0
		totalCommentLines = 0
		totalCodeLines = 0
		
		
		# Walk the directory using Pythons os.walk().			
		for dirName, subDirList, fileList in os.walk(pathDir):
		
			# If recursive flag is not sete then delete sub directories.
			if self._arguments.recursive == False:
				del subDirList[:]

			for fileName in fileList:
				# Get the extension for the file.
				ext = fileName.rpartition('.')[-1]
			
				# Check that the file extension is valid.
				if self._fileParser.IsExpectedFileExtension(ext) == False:
					continue
					
				fullFilename = os.path.join(dirName, fileName)
				fileStats = self._fileParser.ProcessFile(fullFilename)
					
				if fileStats != False:
					blankLines, commentLines, codeLines = fileStats
					
					totalBlankLines += blankLines
					totalCommentLines += commentLines
					totalCodeLines  += codeLines
					
					if self._arguments.verbose == True:
						str = "[FILE] '{0}' | Blank Lines : {1} | " + \
							"Comment Lines : {2} | " + "Code Lines : {3} |"
						print(str.format(fullFilename, blankLines, commentLines,
							codeLines))
		
		totalLines = totalBlankLines + totalCommentLines + totalCodeLines		
		print("Results:")
		percentage = round((totalBlankLines / totalLines) * 100, 2) if totalLines else 0
		print("=> Blank lines   : {0} [{1}%]".format(totalBlankLines, percentage))
		percentage = round((totalCommentLines / totalLines) * 100, 2) if totalLines else 0
		print("=> Comment lines : {0} [{1}%]".format(totalCommentLines, percentage))
		percentage = round((totalCodeLines / totalLines) * 100, 2) if totalLines else 0
		print("=> Code lines    : {0} [{1}%]".format(totalCodeLines, percentage))
		print("=> TOTAL : {0} lines".format(totalLines))