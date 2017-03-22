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
class FileProcessor(object):

	# Override Function: Function to check if the file line is blank.
	def IsBlankLine(self, line):	
		raise NotImplementedError()


	# Override Function: Function to check if the file line is a comment or is
	# within a comment.
	def IsComment(self, line):
		raise NotImplementedError()


	# Override Function: Function to check if the file line is code.
	def IsCode(self, line):
		raise NotImplementedError()
		

	def IsExpectedFileExtension(self, extension):
		raise NotImplementedError()

		
	def ProcessFile(self, filename):
		blankLines = 0
		commentLines = 0
		codeLines = 0

		# Verify that the extension is what we expect, don't raise an error, it
		# is quietly ignored.
		if self.IsExpectedFileExtension(filename.rpartition('.')[-1]) == False:
			print("[DEBUG] Unexpected... ignoring '{0}'".format(filename))
			return False
		
		# Attempt to open the source file.
		fileHandle, msg = self._OpenSourceFile(filename)
		if fileHandle == None:
			print("[ERROR] Unable to open file '{0}' : {1}".format(filename, msg))
			return False

		for line in fileHandle:
			lineLength = len(line)
			
			# Remove trailing characters
			line = line.lstrip(self._StripCharacters)
			
			# If line is within a comment or start/end of long comment then
			# increment count and continue.
			if self.IsComment(line) == True:
				commentLines += 1
				continue

			# If line is blank then increment count and continue.
			if self.IsBlankLine(line) == True:
				blankLines += 1
				continue
	
			# Line is code, increment count and continue.
			if self.IsCode(line) == True:
				codeLines +=1

		# Return statistics for the file.
		return [blankLines, commentLines, codeLines]


	def _OpenSourceFile(self, filename):
		try:
			fileHandle = open(filename)
		except IOError as ioExcept:
			exceptMsg = os.strerror(ioExcept.errno)
			return [None, exceptMsg]

		return [fileHandle, '']
