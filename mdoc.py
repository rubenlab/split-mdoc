import argparse
from datetime import datetime
import os
import shutil
import re
from typing import Tuple
import mdocfile.mdoc


def splitFolder(folder: str, pace: bool):
    files = os.listdir(folder)
    mdocs = []
    for file in files:
        match = re.search(r'.*_ts_.*\.mrc\.mdoc',
                          file) if pace else re.search(r'.*\.mrc\.mdoc', file)
        if match:
            mdocs.append(os.path.join(folder, file))
    for mdoc in mdocs:
        processMdocFile(folder, mdoc)


def processMdocFile(folder: str, mdoc: str):
    (folderName, folderPath) = createMdocFolder(folder, mdoc)
    mdocInfo = mdocfile.mdoc.Mdoc.from_file(mdoc)
    sections = mdocInfo.section_data
    for section in sections:
        ZValue = section.ZValue
        TiltAngle = section.TiltAngle
        DateTime = section.DateTime
        date = datetime.strptime(DateTime, "%d-%b-%y  %H:%M:%S")
        SubFramePath = section.SubFramePath
        originPath = str(SubFramePath)
        eerPath = os.path.join(
            folder, "frames", originPath[originPath.rfind("\\") + 1:])
        newName = folderName + "_" + \
            str(ZValue) + "_" + str(round(TiltAngle, 1)) + \
            "_" + date.strftime("%Y%m%d") + ".eer"
        destPath = os.path.join(folderPath, newName)
        if os.path.exists(eerPath):
            shutil.copyfile(eerPath, destPath)
        else:
            print("file {} not found".format(eerPath))


def createMdocFolder(folder: str, mdoc: str) -> Tuple[str, str]:
    basename = os.path.basename(mdoc)
    foldername = basename.split(".")[0]
    path = os.path.join(folder, foldername)
    if not os.path.exists(path):
        os.mkdir(path)
    return (foldername, path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Split frames based on mdoc files.')
    parser.add_argument('folder', metavar='Folder', type=str,
                        help='folder path to frames folder\'s parent folder')
    parser.add_argument('--pace', action=argparse.BooleanOptionalAction, default=True,
                        help='if it\'s a PACE project')
    args = parser.parse_args()
    splitFolder(args.folder, args.pace)
