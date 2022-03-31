import argparse
from six import BytesIO
from datetime import datetime
from PIL import Image
import locale
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from object_detection.utils import label_map_util # https://github.com/tensorflow/hub/blob/master/examples/colab/tf2_object_detection.ipynb
import pickle
import platform
import tensorflow_hub as hub
import tensorflow as tf
import socket
import threading

# CLI Arguments
parser = argparse.ArgumentParser(description='Service to detect objects in images')
parser.add_argument("-p", "--port", help="TCP Port to listen on. Example: 4949", type=int, default=4949)
parser.add_argument("-b", "--buffer", help="Buffer size. Example: 4096", type=int, default=4096)
parser.add_argument("-m", "--model", help="TensorFlow Hub model to use for inference. Example: https://tfhub.dev/tensorflow/centernet/resnet50v1_fpn_512x512/1 or /path/to/centernet_resnet50v1_fpn_512x512_1", required=True)
parser.add_argument("-l", "--labels", help="Labels mapping file. Example: /path/to/mscoco_label_map.pbtxt or C:\path\to\mscoco_label_map.pbtxt", required=True)
#parser.add_argument("-o", "--locale", help="Set locale. | Example : en_US", default='en_US')
parser.add_argument("-e", "--encoding", help="Set encoding. | Example : utf-8", default='utf-8')
parser.add_argument("-d", "--logging", help="Output logging information.", default=False, action='store_true')
args = parser.parse_args()

# Locale
locale.setlocale(locale.LC_ALL, '')

# Platform
cpuArch = platform.machine()
if cpuArch == "AMD64":
    pass
elif cpuArch == "armv6l":
    pass

if args.logging: print(f'{datetime.now().strftime("%c")} | SERVER | {args}')

# Functions
def getIP(): # stackoverflow shinanigans
    tempSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        tempSocket.connect(('10.255.255.255', 1))
        IP = tempSocket.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        tempSocket.close()
    return IP

# Socket
SERVER_HOST = getIP() # IP Address
SERVER_PORT = args.port # Listening Port (tcp)
BUFFER_SIZE = args.buffer # Bytes to receive each time
SEPARATOR = "###"
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create socket
serverSocket.bind((SERVER_HOST, SERVER_PORT)) # Bind socket to IP Address & Port

# Temp paths for storing images while being processed
if os.name == "posix":
        save_path = '/dev/shm/'
elif os.name == "nt":
        save_path = 'c:/windows/temp/'

# Load Model
# https://tfhub.dev/tensorflow/collections/object_detection/1 Optionally use another model
if args.logging: print(f'{datetime.now().strftime("%c")} | SERVER | Loading Model {args.model}')
hubModel = hub.load(args.model)
if args.logging and hubModel: print(f'{datetime.now().strftime("%c")} | SERVER | Model Loaded')

# Load Labels/Classes
# https://raw.githubusercontent.com/tensorflow/models/master/research/object_detection/data/mscoco_label_map.pbtxt
# https://github.com/tensorflow/models/blob/master/research/object_detection/data/mscoco_label_map.pbtxt
categoryIndex = label_map_util.create_category_index_from_labelmap(args.labels, use_display_name=True)

# Functions
def runInference(fileName):
    imageData = tf.io.gfile.GFile(fileName, 'rb').read() # Read file
    image = Image.open(BytesIO(imageData))
    (imgWidth, imgHeight) = image.size # Get image size
    imageNP = np.array(image).reshape((1, imgHeight, imgWidth, 3)).astype(np.uint8) # Convert to np array
    results = hubModel(imageNP) # Run inference
    return {key: value.numpy() for key, value in results.items()}, imgWidth, imgHeight

def receiveFile(clientSocket, clientAddress):
    # New Connection
    if args.logging: print(f'{datetime.now().strftime("%c")} | CLIENT | {clientAddress} New Connection')

    # Receive file info (name and size)
    try:
        fileInfo = clientSocket.recv(BUFFER_SIZE).decode(args.encoding)
        clientSocket.send("ACK".encode(args.encoding))
    except UnicodeDecodeError:
        print(f'{datetime.now().strftime("%c")} | CLIENT | {clientAddress} ERROR: UnicodeDecodeError')
        clientSocket.close()
        return
    
    if args.logging: print(f'{datetime.now().strftime("%c")} | CLIENT | {clientAddress} RAW: {fileInfo}')
    fileName, fileSize = fileInfo.split(SEPARATOR)
    baseName = os.path.basename(fileName)
    fileName = os.path.join(save_path, baseName)
    fileSize = int(fileSize)
    fileSizeLocaleRound = locale.format_string('%d', round(fileSize / 1024 , 1), grouping=True)
    if args.logging: print(f'{datetime.now().strftime("%c")} | CLIENT | {clientAddress} Receiving File: {baseName}')
    if args.logging: print(f'{datetime.now().strftime("%c")} | CLIENT | {clientAddress} File Size: {fileSizeLocaleRound} KB')

    # Receive file
    totalFileLength = 0
    with open(fileName, "wb") as f:
        while True:
            bytesRead = clientSocket.recv(BUFFER_SIZE) # Read in data of buffer size
            f.write(bytesRead) # Write to the file the bytes received
            totalFileLength = totalFileLength + len(bytesRead)
            if int(totalFileLength)>= fileSize:
                break # Done receiving file

    # Begin inference processing
    if args.logging: print(f'{datetime.now().strftime("%c")} | CLIENT | {clientAddress} Inferencing: {baseName} Model: {args.model}')
    inferenceResults, imgWidth, imgHeight = runInference(fileName)
    
    # Return data to client
    if args.logging: print(f'{datetime.now().strftime("%c")} | CLIENT | {clientAddress} Returning Data to Client')
    clientSocket.send(args.model.encode(args.encoding))
    clientSocket.recv(BUFFER_SIZE).decode(args.encoding)
    pickledInferenceResults = pickle.dumps(inferenceResults)
    clientSocket.send(pickledInferenceResults)
    clientSocket.recv(BUFFER_SIZE).decode(args.encoding)
    pickledCategoryIndex = pickle.dumps(categoryIndex)
    clientSocket.send(pickledCategoryIndex)
    clientSocket.recv(BUFFER_SIZE).decode(args.encoding)

    # Close the client socket
    if args.logging: print(f'{datetime.now().strftime("%c")} | CLIENT | {clientAddress} Closing Connection')
    clientSocket.close()

    # Cleanup files
    os.remove(fileName)

def startServer():
    serverSocket.listen()
    if args.logging: print(f'{datetime.now().strftime("%c")} | SERVER | Listening at: {SERVER_HOST}:{SERVER_PORT}')
    while True:
        clientSocket, clientAddress = serverSocket.accept()
        clientThread = threading.Thread(target=receiveFile, args=(clientSocket, clientAddress))
        clientSocket.send("ACK".encode(args.encoding))
        clientThread.start()
        if args.logging: print(f'{datetime.now().strftime("%c")} | SERVER | Active Connections: {threading.activeCount() - 1}')

startServer()

# close the server socket
serverSocket.close()