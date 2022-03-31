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

<!-- TABLE OF CONTENTS -->
<summary>Table of Contents</summary>
<ol>
  <li>
    <a href="#about-the-project">About The Project</a>
    <ul>
      <li><a href="#built-with">Built With</a></li>
    </ul>
  </li>
  <li>
    <a href="#getting-started">Getting Started</a>
    <ul>
      <li><a href="#prerequisites">Prerequisites</a></li>
      <li><a href="#installation">Installation</a></li>
    </ul>
  </li>
  <li><a href="#usage">Usage</a></li>
  <li><a href="#roadmap">Roadmap</a></li>
  <li><a href="#contributing">Contributing</a></li>
  <li><a href="#license">License</a></li>
  <li><a href="#contact">Contact</a></li>
  <li><a href="#acknowledgments">Acknowledgments</a></li>
</ol>

<!-- ABOUT THE PROJECT -->
## About The Project

tfors is a service that performs object recongition on images sent by a client. tfors let's you centralize any machine learning you have in your environment by having clients send images to a centralized server, perform object recognition, and then return the results to the client.

### Built With

* [Python](https://python.org/)
* [Tensorflow](https://www.tensorflow.org/)

<!-- GETTING STARTED -->
## Getting Started

### Pre-Reqs

1. Python 3.9 64-bit
2. requirements.txt

### Installation (Server)

1. Clone the repo
   ```sh
   git clone https://github.com/tuxthepenguin84/tfors.git
   ```
2. Install PIP packages
  ```sh
   pip3 -r requirements.txt
  ```

### Installation (Client)
1. Clone the repo
   ```sh
    git clone https://github.com/tuxthepenguin84/tfors.git
   ```

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
### Usage (Server)

```sh
  python tfors\server.py -m "https://tfhub.dev/tensorflow/centernet/resnet50v1_fpn_512x512/1" -l "C:\Users\Sam\Documents\git\tfors\mscoco_label_map.pbtxt" -d
```

### Usage (Client)

```sh
  python tfors\client.py -f path\to\image.jpg -s server_ip
```

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