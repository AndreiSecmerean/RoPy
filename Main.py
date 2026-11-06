import os.path
# Source - https://stackoverflow.com/a/66663671
# Posted by Simimic, modified by community. See post 'Timeline' for change history
# Retrieved 2026-10-28, License - CC BY-SA 4.0
import tkinter
from tkinter import filedialog
from os import walk
from pathlib import Path
import logging
import shutil
from venv import logger
import random
import pandas as pd

tkinter.Tk().withdraw() # prevents an empty tkinter window from appearing
JPG_DIR = Path(filedialog.askdirectory())

tkinter.Tk().withdraw() # prevents an empty tkinter window from appearing
RAW_DIR = Path(filedialog.askdirectory())

tkinter.Tk().withdraw() # prevents an empty tkinter window from appearing
DESTINATION_FOLDER = Path(filedialog.askdirectory())

Destinations = {'JPG_DIR': JPG_DIR, 'RAW_DIR': RAW_DIR, 'DESTINATION_DIR': DESTINATION_FOLDER}
pd.DataFrame(Destinations)


def GetFileNames(workingDir, trim):
    files = []
    for (dirPaths, dirNames, fileNames) in walk(workingDir):
            files.extend(fileNames)

    if trim:
        for index, file in enumerate(files):
            photo = files[index]
            if photo.endswith(".jpf") or photo.endswith(".JPG") or photo.endswith(".raf") or photo.endswith(".RAF"):
                files[index] = photo[:-4]
        return files

    return files

def CopyFiles(JpgDir, RawDir, DestinationDir):
    jpgPhotos = GetFileNames(workingDir= JpgDir, trim= True)    #excludes .JPG
    rawPhotos = GetFileNames(workingDir= RawDir, trim= True)    #excludes .RAF

    jpgFiles = GetFileNames(workingDir= JpgDir, trim= False)    #includes .JPG
    rawFiles = GetFileNames(workingDir= RawDir, trim= False)    #includes .RAF

    filesInDir = GetFileNames(workingDir= DestinationDir, trim= False)
    logger.info("Dirs: " +
                "\n\t\t\t\t\t\t\t JPG: " + JpgDir +
                "\n\t\t\t\t\t\t\t Raw: " + RawDir +
                "\n\t\t\t\t\t\t\t Dest: "+ DestinationDir)


    logger.debug("Jpg photos: " +
                 "\n\t\t\t\t\t\t\t " + jpgPhotos.__str__())

    logger.debug("Raw photos: "+
                 "\n\t\t\t\t\t\t\t " + rawPhotos.__str__())

    logger.debug("Jpg files: " +
                 "\n\t\t\t\t\t\t\t " + jpgFiles.__str__())

    logger.debug("Raw files: " +
                 "\n\t\t\t\t\t\t\t " + rawFiles.__str__())



    foundMatches = [rawFile for rawFile in rawFiles if any(jpgPhoto in rawFile for jpgPhoto in jpgPhotos)]
    logger.info("Found: " + len(foundMatches).__str__() + " matches")
    logger.debug("Found files are: " + foundMatches.__str__())

    for rawFile in foundMatches:
        copyFile = RawDir + '/' + rawFile
        logger.debug("Copy file: " + copyFile)
        if not rawFile in filesInDir:
            shutil.copy2(copyFile, DestinationDir)
        elif rawFile in filesInDir:
            renameFile = rawFile[:-4]
            shutil.copy2(copyFile, os.path.join(DestinationDir, renameFile + '(' + random.randrange(0,10,1).__str__() + ').RAF').__str__())


def main():
    logging.basicConfig(filename='Ropy.log', format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)

    logger.info("======Started Ropy!======")
    CopyFiles(JpgDir= JPG_DIR.__str__(), RawDir= RAW_DIR.__str__(), DestinationDir= DESTINATION_FOLDER.__str__())
    logger.info("Copied files to: "+ DESTINATION_FOLDER.__str__())
    logger.info("======Ropy finished with success!======\n\n\n\n\n")

if __name__ == "__main__":
    main()