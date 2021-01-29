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
from __future__ import division
from enum import Enum
import os
import sys


class LogLevel(Enum):
    Info = 0
    Warning = 1
    Error = 2
    Verbose = 3

LogLevelStr = {
    LogLevel.Info : "[INFO]",
    LogLevel.Warning : "[WARN]",
    LogLevel.Error : "[ERROR]",
    LogLevel.Verbose : "[VERBOSE]"
}


class LineCount:

    def __init__(self, args):
        self._fileProcessor = None
        self._arguments = args


    def ProcessFilesInDir(self, pathDir):
        fileStats = False
        totalBlankLines = 0
        totalCommentLines = 0
        totalCodeLines = 0

        if not self._fileProcessor:
            print("[ERROR] No file processor has been specified!")
            return

        # Walk the directory using Pythons os.walk().
        for dirName, subDirList, fileList in os.walk(pathDir):

            # If recursive flag is not sete then delete sub directories.
            if not self._arguments.recursive:
                del subDirList[:]

            for fileName in fileList:
                # Get the extension for the file.
                ext = fileName.rpartition('.')[-1]

                # Check that the file extension is valid.
                if not self._fileProcessor.IsExpectedFileExtension(ext):
                    continue

                fullFilename = os.path.join(dirName, fileName)
                fileStats = self._fileProcessor.ProcessFile(fullFilename)

                if fileStats != False:
                    blankLines, commentLines, codeLines = fileStats

                    totalBlankLines += blankLines
                    totalCommentLines += commentLines
                    totalCodeLines += codeLines

                    if self._arguments.verbose:
                        msgStr = "{0} | Blank Lines : {1} | " + \
                                 "Comment Lines : {2} | " + "Code Lines : {3} |"
                        self.LogMessage(LogLevel.Verbose,
                                        msgStr.format(fullFilename, blankLines,
                                                      commentLines, codeLines))

        totalLines = totalBlankLines + totalCommentLines + totalCodeLines
        print("Results:")
        percentage = round((totalBlankLines / totalLines) * 100, 2) if totalLines else 0
        print("=> Blank lines   : {0} [{1}%]".format(totalBlankLines, percentage))
        percentage = round((totalCommentLines / totalLines) * 100, 2) if totalLines else 0
        print("=> Comment lines : {0} [{1}%]".format(totalCommentLines, percentage))
        percentage = round((totalCodeLines / totalLines) * 100, 2) if totalLines else 0
        print("=> Code lines    : {0} [{1}%]".format(totalCodeLines, percentage))
        print("=> TOTAL : {0} lines".format(totalLines))


    def LoadFileProcessor(self, processorName):
        processorToLoad = "FP_{0}".format(processorName)

        try:
            fileProcessorModule = __import__(processorToLoad)
            fileProcessorClass = getattr(fileProcessorModule, processorName)
            fileProcessor = fileProcessorClass()

        except ImportError as ex:
            msg = f"'{processorName}' file processor load error : {ex}"
            self.LogMessage(LogLevel.Error, msg)
            return False

        except AttributeError as ex:
            print(f"[EXCEPT CAUGHT] {ex}")
            return False

        self._fileProcessor = fileProcessor

        return True


    def LogMessage(self, logLevel, message):
        print(f"{LogLevelStr[logLevel]} {message}")
