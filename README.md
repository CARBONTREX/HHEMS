# HHEMS - Hybrid Home Energy Management System

### An open-source hybrid home energy management platform for Dutch households

HHEMS is a research prototype developed at TU Delft as part of the [Convergence](https://cesi-nl.github.io/) initiative. The platform provides a framework for developing and testing energy management algorithms while enabling integration with both real smart home devices and simulated energy systems.

**🌐 [Project Website](https://algtudelft.github.io/HHEMS/)**

## What is HHEMS?

HHEMS (Hybrid Home Energy Management System) is an experimental platform that combines real smart home device control with energy system simulation. The system addresses the challenge of developing and testing energy management algorithms without requiring expensive hardware setups.

The platform integrates [Home Assistant](https://www.home-assistant.io/) for device communication with [DEMKit](https://www.utwente.nl/en/eemcs/energy/demkit/) simulation capabilities, allowing researchers to work with both physical devices (when available) and simulated alternatives (solar panels, batteries, electric vehicles) within the same framework.

### Core Components

- **Home Assistant Integration**: Connects to real smart home devices through existing integrations
- **DEMKit Simulation Engine**: Simulates energy devices like solar panels, batteries, and electric vehicles
- **HEMS Core**: Provides APIs for energy management algorithm development
- **Unified Interface**: Treats real and simulated devices identically from the algorithm perspective

![HHEMS Architecture](https://algtudelft.github.io/HHEMS/public/architecture.png)

## Use Cases

### Research Applications

- Algorithm development without hardware dependencies
- Testing energy management strategies in controlled environments
- Comparative studies between different optimization approaches
- Educational demonstrations of smart energy concepts

### Practical Applications

- Homeowners with existing smart devices seeking optimization
- Prototyping energy management solutions before hardware investment
- Integration testing for new smart home device configurations

## Technical Architecture

The system operates through several interconnected components:

1. **Home Assistant Core**: Manages real device communications and provides a unified device interface
2. **HEMS Core**: Implements the main energy management logic and exposes APIs for algorithm development
3. **DEMKit Integration**: Handles simulation of energy devices and systems
4. **Configuration Layer**: Allows setup of hybrid environments mixing real and simulated devices

Developers interact with the platform through APIs that abstract device complexity, enabling focus on energy optimization logic rather than hardware communication protocols.

## Mobile Application Development

A mobile application is currently under development by students as part of the CSE2000 software project course. The app aims to provide a user interface for energy monitoring and device control, complementing Home Assistant's automation-focused interface.

### Current Mobile App Interface

<table>
<tr>
<td><img src="https://algtudelft.github.io/HHEMS/public/mobile/image1.png" width="200" alt="Mobile App Screenshot 1"/></td>
<td><img src="https://algtudelft.github.io/HHEMS/public/mobile/image2.png" width="200" alt="Mobile App Screenshot 2"/></td>
<td><img src="https://algtudelft.github.io/HHEMS/public/mobile/image3.png" width="200" alt="Mobile App Screenshot 3"/></td>
</tr>
<tr>
<td><img src="https://algtudelft.github.io/HHEMS/public/mobile/image4.png" width="200" alt="Mobile App Screenshot 4"/></td>
<td><img src="https://algtudelft.github.io/HHEMS/public/mobile/image5.png" width="200" alt="Mobile App Screenshot 5"/></td>
<td><img src="https://algtudelft.github.io/HHEMS/public/mobile/image6.png" width="200" alt="Mobile App Screenshot 6"/></td>
</tr>
<tr>
<td><img src="https://algtudelft.github.io/HHEMS/public/mobile/image7.png" width="200" alt="Mobile App Screenshot 7"/></td>
<td><img src="https://algtudelft.github.io/HHEMS/public/mobile/image8.png" width="200" alt="Mobile App Screenshot 8"/></td>
<td><img src="https://algtudelft.github.io/HHEMS/public/mobile/image9.png" width="200" alt="Mobile App Screenshot 9"/></td>
</tr>
</table>

## Future Research Directions

Current research explores extensions including:

- **Multi-household coordination**: Investigating energy sharing and coordination between connected households
- **Community-scale optimization**: Developing algorithms for neighborhood-level energy management
- **Grid integration**: Exploring how coordinated household systems might interact with larger energy infrastructure
- **Mobile energy storage**: Research into electric vehicles as distributed energy storage resources

## Prerequisites

- Docker
- If Windows, preferably WSL

## Installation

### 1. Create Docker Network

```bash
docker network create hems_network
```

### 2. Set Up Home Assistant

```bash
cd ha
docker compose up -d
```

Create your user and configure Home Assistant, then create a long-lived access token ([guide](https://community.home-assistant.io/t/how-to-get-long-lived-access-token/162159)).

### 3. Configure HEMS Core Environment

```bash
cd hems-core
cp .env.example .env
```

Set the `HA_TOKEN` environment variable with your long-lived access token.

### 4. Run HEMS Core

```bash
cd hems-core
docker build . -t hems-core
docker compose up hems-core -d
```

### 5. Start DEMKit Simulation

**Note**: Windows users without WSL should verify absolute paths in docker-compose files in the `demkit/` folder.

```bash
cd demkit
docker build . -t demkit
docker compose -f docker-compose.services.yml up -d
docker compose -f docker-compose.demkit.yml up -d
```

### 6. Run Basic Configuration

```bash
python3 configs/basic.py
```

## Development Status

HHEMS is an active research project at TU Delft. The codebase is available for research purposes, algorithm development, and experimentation. The platform continues to evolve based on research needs and community feedback.

## Contributing

The project welcomes contributions in areas including:

- Energy management algorithm implementations
- Device integration extensions
- Simulation model improvements
- Documentation and examples
- Testing and validation

## License

This project is open-source. License details are specified in the repository.

---

*Additional information available at the [project website](https://algtudelft.github.io/HHEMS/).*
