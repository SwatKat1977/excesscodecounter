'''
Extensible Code Counter System [EXCESS]
Copyright (C) 2017-2019 Gemma Morriss

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
from FileProcessor import *


class CSharp(FileProcessor):
    _StripCharacters = ' \t\n\r'

    # Comment keywords
    _LongCommentStart = '/*'
    _LongCommentEnd = '*/'
    _ShortComment = '//'

    _Extensions = ['cs']


    def __init__(self):
        self._inComment = False


    def IsBlankLine(self, line):
        # If line is void of characters then it's obviously blank!
        return len(line) == 0


    def IsComment(self, line):
        # If there in comment block then check for end, or just increment the
        # count for comment lines.
        if self._inComment == True:
            if line.startswith(self._LongCommentEnd):
                self._inComment = False

            return True

        else:
            # Long comment has been detected.
            if line.startswith(self._LongCommentStart):
                # It's possible long comment is in one line, so check.
                if not line.endswith(self._LongCommentEnd):
                    self._inComment = True

                return True

            # Short comment has been detected.
            elif line.startswith(self._ShortComment):
                return True

        # Not a comment keyword
        return False


    def IsCode(self, line):
        return True


    def IsExpectedFileExtension(self, extension):
        return extension in self._Extensions
