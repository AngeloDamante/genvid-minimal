# genvid-minimal

A minimal video (dataset) generator for OD purposes.

## Layout Directories
```
├── datasets_out
├── patches
├── routes
├── sequences
├── src
│   ├── BackgroundIterator.py
│   ├── evolver.py
│   ├── LoggingManager.py
│   ├── motion_law.py
│   ├── MovementType.py
│   └── simulator.py
├── test
├── create_random_route.py
├── create_random_sequence.py
├── create_video.py
├── generate_random_dataset.py
├── download_sample_backgrounds.sh
├── run_example_2.sh
├── run_random_sequence_generator.sh
├── run_simple_example.sh
├── Dockerfile
├── docker-compose.yaml
├── requirements.txt
└── README.md
```

## Installation

### Virtualenv

If not installed, install:
```
pip install virtualenv
```
Then create the env:
```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Pip

Tested with python 3.8 and 3.10 
```
pip install -r requirements.txt
```

### Docker
Let's set up the image
```
mkdir datasets_out
docker-compose build 
```

you can work directly in the container with the environment setted or directly run some examples.
```
# launch interactive container
docker-compose run --rm genvid

# launch quick examples  
docker-compose run --rm generate_video
docker-compose run --rm generate_dataset
```
## Optional data

if needed, there are some background videos that can be downloaded automatically to *backgrounds* directory using:

```
./download_sample_backgrounds.sh
```

## Usage

The main script is **create_video.py** which uses src/simulator.py to create the dataset sequences.

A simple example can be found by running ` ./run_simple_example.sh `.

A full example here:

```
python3 create_video.py   --background="0,0,0" --width=640 --height=480 --input-json="square_pentagon_map.json" --fps=30
                          --background="bg1.png"
                          --background="buildings_moving.png"
```

All paths can be passed as static, relative to current dir or relative to own dir:

```
├── create_video.py
├── sequences
│   └── example_2_figures.json
├── patches
│   ├── circle.png
│   └── square.npy
├── routes
│   ├── diag_right.txt
│   └── letter_l.txt
```
## How it works

A sequence video is made by moving a list of objects (patches like 3D ndarray or an image) inside a frame (video size) with certain settings (sequence json file) following a path (txt route file).

![](repo_img/Diagrams.png)