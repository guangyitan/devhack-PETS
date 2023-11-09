# This repository contains the POC for PETS System 

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#demo">Demo</a>
      <ul>
        <li><a href=#pets-dashboard-demo">PETS Dashboard Demo</a></li>
        <li><a href=#pets-mobile-view-demo">PETS Mobile View Demo</a></li>
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
### PETS Dashboard Demo

[Figma Prototype](https://www.figma.com/proto/Z2IoNZiSgzcobu0HJIBAI9/Untitled?type=design&node-id=43-25637&t=f9RJFsaFJzrJkCrF-1&scaling=scale-down-width&page-id=0%3A1&starting-point-node-id=43%3A25637&show-proto-sidebar=1&mode=design)

### PETS Mobile View Demo

[Figma Prototype](https://www.figma.com/proto/Z2IoNZiSgzcobu0HJIBAI9/Untitled?type=design&node-id=68-15158&t=4mOIi9B7ZspJbZfB-0&scaling=scale-down-width&page-id=0%3A1&starting-point-node-id=68%3A15158&show-proto-sidebar=1)

### Accident & Pothole Detection

If video is not playable: [Youtube PETS - Accident & Pothole Detection - Demo 1](https://youtu.be/zNbTNnXWP5c)

https://github.com/guangyitan/devhack-PETS/assets/83216707/05551d40-6cb1-47f7-877b-f496cbfaf597

If video is not playable: [Youtube PETS - Accident & Pothole Detection - Demo 2](https://youtu.be/evjpWMpXj80)

https://github.com/guangyitan/devhack-PETS/assets/83216707/9feb6c1d-bb77-4b07-ad3e-413c731e9c13

### Traffic Flow & Pothole Detection

If video is not playable: [Youtube PETS - Traffic Flow & Pothole Detection - Demo](https://youtu.be/fCWraJGd9l8)

https://github.com/guangyitan/devhack-PETS/assets/83216707/19984daa-26df-42ba-a723-029d70dc418a

### Parking Detection

If video is not playable: [Youtube PETS - Parking Detection - Demo](https://youtu.be/rwf37F6bov8)

https://github.com/guangyitan/devhack-PETS/assets/83216707/4abc9233-ef3d-477f-b158-33a17fa6c853

## Pothole Detection

If video is not playable: [Youtube PETS - Pothole Detection - Demo 1](https://youtu.be/TqYsIMOEWUY)


https://github.com/guangyitan/devhack-PETS/assets/83216707/3bd6405c-7f76-42da-8adf-e40e14c38a21


If video is not playable: [Youtube PETS - Pothole Detection - Demo 2](https://youtu.be/TMh4xWcqeuI)


https://github.com/guangyitan/devhack-PETS/assets/83216707/7adb7423-a305-4fa5-8b77-f5f650f71c64


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

