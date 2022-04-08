<div id="top"></div>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/tuxthepenguin84/tfors">
    <!-- <img src="images/logo.png" alt="Logo" width="80" height="80"> -->
  </a>

<h3 align="center">tfors</h3>

  <p align="center">
    TensorFlow Object Recognition Service
    <br />
    <a href="https://github.com/tuxthepenguin84/tfors"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/tuxthepenguin84/tfors">View Demo</a>
    ·
    <a href="https://github.com/tuxthepenguin84/tfors/issues">Report Bug</a>
    ·
    <a href="https://github.com/tuxthepenguin84/tfors/issues">Request Feature</a>
  </p>
</div>

<!-- ABOUT THE PROJECT -->
## About The Project

tfors is a service that performs object recongition on images sent by a client. tfors let's you centralize any machine learning you have in your environment by having clients send images to a centralized server, perform object recognition, and then return the results to the client.

### Built With

* [Python](https://python.org/)
* [Tensorflow](https://www.tensorflow.org/)

<!-- GETTING STARTED -->
## Getting Started

### Docker Installation (Server)
Recommended way to host tfors
https://hub.docker.com/r/tuxthepenguin/tfors

### Traditional App Installation (Server)

1. Install pre-reqs
```sh
apt-get update && apt-get install -y --no-install-recommends \
  python3 \
  python3-pip \
  python-is-python3 \
  build-essential \
  python3-dev \
  git \
  protobuf-compiler \
  apt-transport-https \
  ca-certificates
```
2. Configure Object Detection & PIP packages
```sh
git clone --depth 1 https://github.com/tensorflow/models
cd models/research/
protoc object_detection/protos/*.proto --python_out=.
cp object_detection/packages/tf2/setup.py .
python -m pip install .
pip install httplib2
```

### Traditional App Usage (Server)
```sh
python server.py -m "https://tfhub.dev/tensorflow/centernet/resnet50v1_fpn_512x512/1" -l "C:\Users\Sam\Documents\git\tfors\mscoco_label_map.pbtxt" -d
```

### Traditional App Arguments (Server)
```
parser.add_argument("-p", "--port", help="TCP Port to listen on. Example: 4949", type=int, default=4949)
parser.add_argument("-b", "--buffer", help="Buffer size. Example: 4096", type=int, default=4096)
parser.add_argument("-m", "--model", help="TensorFlow Hub model to use for inference. Example: https://tfhub.dev/tensorflow/centernet/resnet50v1_fpn_512x512/1 or /path/to/centernet_resnet50v1_fpn_512x512_1", required=True)
parser.add_argument("-l", "--labels", help="Labels mapping file. Example: /path/to/mscoco_label_map.pbtxt or C:\path\to\mscoco_label_map.pbtxt", required=True)
parser.add_argument("-e", "--encoding", help="Set encoding. | Example : utf-8", default='utf-8')
parser.add_argument("-d", "--logging", help="Output logging information.", default=False, action='store_true')
```

### Docker/Traditional App Installation (Client)
```sh
git clone https://github.com/tuxthepenguin84/tfors.git
```

### Docker/Traditional App Usage (Client)
```sh
python client.py -f path\to\image.jpg -s server_ip
```

### Docker/Traditional App Arguments (Client)
```
parser.add_argument("-f", "--file", help="Path to file", default=None) # accepts pipeline input
parser.add_argument("-s", "--server", help="The host/IP address of the server", required=True)
parser.add_argument("-p", "--port", help="TCP Port to send to. Example: 4949", type=int, default=4949)
parser.add_argument("-b", "--buffer", help="Buffer size. Example: 4096", type=int, default=4096)
parser.add_argument("-e", "--encoding", help="Set encoding. | Example : utf-8", default='utf-8')
parser.add_argument("-c", "--objectclass", help="Object class to recognize. | Example : cat", default=None)
parser.add_argument("-x", "--detectionbox", help="Detection box size (0.0 min - 1.0 max) [y_min, x_min, y_max, x_max] | Example : 0.0 0.0 0.5 0.5", nargs='+', default=None)
parser.add_argument("-m", "--minscore", help="Minimum detection score (percent). | Example : 60", type=int, default=60)
parser.add_argument("-a", "--maxresults", help="Max results returned. | Example : 1", type=int, default=1)
parser.add_argument("-u", "--output", help="Output type: simple, detailed, json, raw. | Example : simple", default="simple")
parser.add_argument("-d", "--logging", help="Output logging information.", default=False, action='store_true')
```

### Systemd
See: tfors.service file

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

- [ ] Return data to client in JSON format
- [ ] Return all inferenced class, score, and bounding box data to client

See the [open issues](https://github.com/tuxthepenguin84/tfors/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Sam Dockery - [@SFTuxTweet](https://twitter.com/SFTuxTweet) - samueldockery@gmail.com

Project Link: [https://github.com/tuxthepenguin84/tfors](https://github.com/tuxthepenguin84/tfors)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Best-README-Template](https://github.com/othneildrew/Best-README-Template)
* [pythoncode-tutorials](https://github.com/x4nth055/pythoncode-tutorials)
* [tensorflow/models](https://github.com/tensorflow/models)
* [tfhub.dev](https://tfhub.dev/tensorflow/collections/object_detection/1)

<p align="right">(<a href="#top">back to top</a>)</p>