import argparse
from datetime import datetime
import locale
import os
from pathlib import Path
import pickle
import socket
import sys
import json

# CLI Arguments
parser = argparse.ArgumentParser(description="Client for sending images to an object recogniction service")
parser.add_argument("-f", "--file", help="Path to file, also accepts pipeline input", default=None) # accepts pipeline input
parser.add_argument("-s", "--server", help="The host/IP address of the server, required.", required=True)
parser.add_argument("-p", "--port", help="TCP Port to send to. | Example (default): 4949", type=int, default=4949)
parser.add_argument("-b", "--buffer", help="Buffer size. | Example (default): 4096", type=int, default=4096)
parser.add_argument("-e", "--encoding", help="Set encoding. | Example (default): utf-8", default='utf-8')
parser.add_argument("-c", "--objectclass", help="Object class(s) to recognize. | Example 1: cat | Example 2: car airplane 'potted plant' chair | Notes: When using multiple object classes, --maxresults is ignored", nargs='+', default=None)
parser.add_argument("-x", "--detectionbox", help="Detection box size (0.0 min - 1.0 max) [y_min, x_min, y_max, x_max] | Example : 0.0 0.0 0.5 0.5", nargs='+', default=None)
parser.add_argument("-m", "--minscore", help="Minimum detection score (percent). | Example (default): 60", type=int, default=60)
parser.add_argument("-a", "--maxresults", help="Max results returned. | Example (default): 1", type=int, default=1)
parser.add_argument("-u", "--output", help="Output type: silent, simple, detailed, json, onlyclass, onlyscore, onlybox, onlyclassfound, onlywithinbox, raw. | Example (default): simple", default="simple")
parser.add_argument("-d", "--logging", help="Output logging information.", default=False, action='store_true')
args = parser.parse_args()

# Locale
locale.setlocale(locale.LC_ALL, '')

if args.logging: print(f'{datetime.now().strftime("%c")} | {args}')

# Socket
SERVER_HOST = args.server # Server IP Address
SERVER_PORT = args.port # Server Port (tcp)
BUFFER_SIZE = args.buffer # Bytes to receive each time
SEPARATOR = "###"

# Client Parameters
if isinstance(args.objectclass, list):
    fileObjectClass = list((map(lambda x: x.lower(), args.objectclass)))
    fileMaxResults = len(fileObjectClass)
elif args.objectclass == None:
    fileObjectClass = None
    fileMaxResults = args.maxresults
fileBox = args.detectionbox
fileMinScore = args.minscore

# Functions
def sendFile(fileName):

    # Create socket and connect to host and port
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((SERVER_HOST, SERVER_PORT))
    clientSocket.recv(BUFFER_SIZE).decode(args.encoding)
    if args.logging: print(f'{datetime.now().strftime("%c")} | {clientSocket.getsockname()}')

    # Send file info
    fileSize = os.path.getsize(fileName)
    baseName = os.path.basename(fileName)
    fileSizeLocaleRound = locale.format_string('%d', round(fileSize / 1024 , 1), grouping=True)
    if args.logging: print(f'{datetime.now().strftime("%c")} | Sending File: {fileName}')
    if args.logging: print(f'{datetime.now().strftime("%c")} | Size: {fileSizeLocaleRound} KB')
    if args.logging: print(f'{datetime.now().strftime("%c")} | Uploading...')
    clientSocket.send(f"{fileName}{SEPARATOR}{fileSize}".encode(args.encoding).strip()) # Send file info (name and size)
    clientSocket.recv(BUFFER_SIZE).decode(args.encoding)

    # Send file
    with open(fileName, "rb") as f:
        while True:
            bytesRead = f.read(BUFFER_SIZE) # Read the bytes from the file
            if not bytesRead:
                break # Done sending file
            clientSocket.sendall(bytesRead)

    # Receive data back
    modelInfo = clientSocket.recv(BUFFER_SIZE).decode(args.encoding)
    clientSocket.send("ACK".encode(args.encoding))
    if args.logging: print(f'{datetime.now().strftime("%c")} | TensorFlow Model: {modelInfo}')
    pickledInferenceResults = clientSocket.recv(BUFFER_SIZE)
    clientSocket.send("ACK".encode(args.encoding))
    inferenceResults = pickle.loads(pickledInferenceResults)
    pickledCategoryIndex = clientSocket.recv(BUFFER_SIZE)
    clientSocket.send("ACK".encode(args.encoding))
    categoryIndex = pickle.loads(pickledCategoryIndex)

    # Store results
    resultNumDetections, allResultClasses, allResultScores, allResultBoxes = inferenceResults['num_detections'][0].astype(int), inferenceResults['detection_classes'][0], inferenceResults["detection_scores"][0], inferenceResults["detection_boxes"][0]
        
    # Begin outputting
    silentExit = 1
    if args.output == "raw":
        print(inferenceResults)
    else:
        jsonOutput = []
        for i in range(resultNumDetections):
            if allResultScores[i] >= fileMinScore/100 and i < fileMaxResults:
                
                # Determine if object in detection box
                if fileBox != None: # [y_min, x_min, y_max, x_max]
                    boxCenterX = (allResultBoxes[i][1]+allResultBoxes[i][3])/2
                    boxCenterY = (allResultBoxes[i][0]+allResultBoxes[i][2])/2
                    if (boxCenterX >= float(fileBox[1])) and (boxCenterX <= float(fileBox[3])) and (boxCenterY >= float(fileBox[0])) and (boxCenterY <= float(fileBox[2])):
                        withinBox = True
                    else:
                        withinBox = False
                        # Only output when objects are within box
                        if args.output != "silent":
                            continue
                else:
                    withinBox = None
                
                # Determine if object class found
                if fileObjectClass != None:
                    for currentObjectClass in range(len(fileObjectClass)):
                        if fileObjectClass[currentObjectClass] == categoryIndex[allResultClasses[i]]["name"]:
                            resultClassFound = True
                            break
                        else:
                            resultClassFound = False
                    # Only output when classes that were specified are found
                    if resultClassFound == False and args.output != "silent":
                        continue
                else:
                    resultClassFound = None                
                
                # Print output
                if args.output == "silent":
                    if resultClassFound == True and withinBox == None: # Class only
                        silentExit = 0
                        break
                    elif resultClassFound == None and withinBox == True: # Box only
                        silentExit = 0
                        break
                    elif resultClassFound == True and withinBox == True: # Class & Box
                        silentExit = 0
                        break
                    else:
                        silentExit = 1
                elif args.output == "simple":
                    print(f'{baseName}, {categoryIndex[allResultClasses[i]]["name"]}, {int(allResultScores[i] * 100)}, {allResultBoxes[i]}, {resultClassFound}, {withinBox}')
                elif args.output == "detailed":
                    print(f'Filename: {baseName}')
                    print(f'Inferenced Class: {categoryIndex[allResultClasses[i]]["name"]}')
                    print(f'Inferenced Score: {int(allResultScores[i] * 100)}%')
                    print(f'Inferenced Box: {allResultBoxes[i]}')
                    print(f'Class Found: {resultClassFound}')
                    print(f'Within Detection Box: {withinBox}')
                elif args.output == "json":
                    jsonOutput.append({ "Filename":baseName, "Inferenced Class":categoryIndex[allResultClasses[i]]["name"], "Inferenced Score":int(allResultScores[i] * 100), "Inferenced Box":str(allResultBoxes[i]), "Class Found":resultClassFound, "Within Detection Box":withinBox})
                elif args.output == "onlyclass":
                    print(f'{categoryIndex[allResultClasses[i]]["name"]}')
                elif args.output == "onlyscore":
                    print(f'{int(allResultScores[i] * 100)}%')
                elif args.output == "onlybox":
                    print(f'{allResultBoxes[i]}')
                elif args.output == "onlyclassfound":
                    print(f'{resultClassFound}')
                elif args.output == "onlywithinbox":
                    print(f'{withinBox}')
                else:
                    print(f'Unknown output option specified.')
    # Print JSON output
    if args.output == "json":
        print(json.dumps(jsonOutput, indent=3))
    # Close the client socket
    if args.logging: print(f'{datetime.now().strftime("%c")} | Closing Connection')
    clientSocket.close()
    # Check for silent output
    if args.output == "silent":
        #print(silentExit)
        sys.exit(silentExit)

# Check for pipeline input, folder, or file and call sendFile()
if args.file == None:
    for fileName in sys.stdin:
        sendFile(fileName.strip())
elif os.path.isdir(args.file):
    folderName = Path(args.file)
    allFiles = list(folderName.glob("*"))
    for fileName in allFiles:
        sendFile(fileName)
elif os.path.isfile(args.file):  
    fileName = args.file
    sendFile(fileName)
else:
    print("Unknown file input.")