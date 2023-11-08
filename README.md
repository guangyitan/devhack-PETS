# This repository contains the POC for PETS System 

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#demo">Demo</a>
      <ul>
        <li><a href="#accident--pothole-detection">Accident & Pothole Detection</a></li>
        <li><a href="#traffic-flow--pothole-detection">Traffic Flow & Pothole Detection</a></li>
        <li><a href="#parking-detection">Parking Detection</a></li>
        <li><a href="#pothole-detection">Pothole Detection</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#install-required-modules-from-pypi">Install required modules from PyPI</a></li>
        <li><a href="#obtain-model-weights">Obtain model weights</a></li>
        <li><a href="#obtain-testing-video">Obtain testing video</a></li>
        <li><a href="#your-folder-should-looked-like-this">Your folder should looked like this</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
  </ol>
</details>

## Demo
### Accident & Pothole Detection

https://github.com/guangyitan/devhack-PETS/assets/83216707/a1349464-da72-45e3-993b-48b974516d2e

https://github.com/guangyitan/devhack-PETS/assets/83216707/2805335a-ffb9-47a7-a33d-60db0fb1dd8a

### Traffic Flow & Pothole Detection

https://github.com/guangyitan/devhack/assets/83216707/0940b2f2-f4a0-4f41-9a88-dda5c98d992b

### Parking Detection

https://github.com/guangyitan/devhack/assets/83216707/e6b943db-0eac-41e0-9d17-1044172bbd31

## Pothole Detection

https://github.com/guangyitan/devhack/assets/83216707/6427cb47-e716-4fe9-a19a-1e13fa756e33

https://github.com/guangyitan/devhack-PETS/assets/83216707/de6c32bd-130b-4cb6-bd2b-b50c31488218


<!-- GETTING STARTED -->
## Getting Started

### Prerequisite
To run they project locally, make sure Python 3.10.13 is installed

### Install required modules from PyPI
```bash
pip install -r main/requirements.txt
```
### Obtain model weights
1. Download model weights from [Google Drive](https://drive.google.com/drive/folders/1Rm3YCZWh5aWv6dyKvM8eqqsO4TGeaScN?usp=sharing)
2. Store the downloaded folder into the directory `main/model_files`

### Obtain testing video
1. Download sample videos from [Google Drive](https://drive.google.com/drive/folders/1eLCC4GGu1FeTBsK9urqvV4ujhEOTbXK_?usp=sharing)
2. Store the downloaded folder into the root directory of this repository`/media`

### Your folder should looked like this
```bash
├───main
│   ├───deep_sort
│   ├───model_files
│   ├───output
├───media
```

<!-- USAGE -->
## USAGE
```bash
$ python main.py
#or
$ python main/main.py
```
To run detection on other videos, uncomment any of the lines below
```bash
file_name = 'accident-pothole-demo'
# file_name = 'accident-pothole-demo2'
# file_name = 'pothole-demo'
# file_name = 'pothole-demo2'
# file_name = 'traffic-pothole-demo'
# file_name = 'parking-demo'
```
```bash
# comment / uncomment related lines for needed detection
frame = accident_detection.detect(frame)
frame = pothole_detection.detect(frame)
# frame = parking_detection.detect(frame)
# frame = traffic_detection.detect(frame)
```

