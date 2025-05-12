# HHEMS
### An open-source hybrid home energy management platform for Dutch households
HHEMS, a prototype platform developed at TU Delft, offering a framework for researchers to develop new energy management algorithms.
Developers interacting with the platform are able to configure a hybrid household implementing a range of simulated devices as well as incorporating real hardware components. These devices can then be controlled via the API that HEMS Core provides.

## Prerequisites

- Docker
- if Windows, preferably WSL


## Setup

#### Create a docker network
```sh
docker network create hems_network
```

#### Run Home Assistant
```sh
cd ha
docker compose up -d
```

Create your user and set up home assistant. Then create a long-lived access tokens ([guide](https://community.home-assistant.io/t/how-to-get-long-lived-access-token/162159)). 

#### Setup env for core

```sh
cd hems-core
cp .env.example .env
```

Set the `HA_TOKEN` environment variable with the long-lived access token 

#### Run the core

```sh
cd hems-core
docker build . -t hems-core
docker compose up hems-core -d
```

#### Run the demkit simulation

*Note: if you are using windows (without WSL), make sure you set the paths correctly (using absolute paths) in docker-compose files in `demkit/` folder.*

```sh
cd demkit
docker build . -t demkit
docker compose -f docker-compose.services.yml up -d
docker compose -f docker-compose.demkit.yml up -d
```


### Start the simulation using a config

```sh
python3 configs/basic.py
```
