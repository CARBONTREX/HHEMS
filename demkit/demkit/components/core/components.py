# Copyright 2023 University of Twente

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from demkit.components.dev.loadDev import LoadDev				# Static load device model
from demkit.components.dev.curtDev import CurtDev				# Also a static load, but one that van be turned off (curtailed/shed)
from demkit.components.dev.btsDev import BtsDev				# BufferTimeShiftable Device, used for electric vehicles
from demkit.components.dev.tsDev import TsDev					# Timeshiftable Device, used for whitegoods
from demkit.components.dev.bufDev import BufDev				# Buffer device, used for storage, such as batteries
from demkit.components.dev.bufConvDev import BufConvDev		# BufferConverter device, used for heatpumps with heat store

from demkit.components.dev.electricity.solarPanelDev import SolarPanelDev			# Solar panel
from demkit.components.dev.thermal.solarCollectorDev import SolarCollectorDev 	# solar collector

# Thermal Devices
from demkit.components.dev.thermal.zoneDev2R2C import ZoneDev2R2C
from demkit.components.dev.thermal.zoneDev1R1C import ZoneDev1R1C
from demkit.components.dev.thermal.heatSourceDev import HeatSourceDev
from demkit.components.dev.thermal.thermalBufConvDev import ThermalBufConvDev
from demkit.components.dev.thermal.heatPumpDev import HeatPumpDev
from demkit.components.dev.thermal.combinedHeatPowerDev import CombinedHeatPowerDev
from demkit.components.dev.thermal.gasBoilerDev import GasBoilerDev
from demkit.components.dev.thermal.dhwDev import DhwDev
from demkit.components.ctrl.thermal.thermostat import Thermostat


# Environment
from environment.sunEnv import SunEnv
from environment.weatherEnv import WeatherEnv

from demkit.components.dev.meterDev import MeterDev			# Meter device that aggregates the load of all individual devices


# Controllers
from demkit.components.ctrl.congestionPoint import CongestionPoint	# Import a congestion point
from demkit.components.ctrl.loadCtrl import LoadCtrl			# Static load controller for predictions
from demkit.components.ctrl.curtCtrl import CurtCtrl			# Static Curtailable load controller for predictions
from demkit.components.ctrl.btsCtrl import BtsCtrl    		# BufferTimeShiftable Controller
from demkit.components.ctrl.tsCtrl import TsCtrl				# Timeshiftable controller
from demkit.components.ctrl.bufCtrl import BufCtrl			# Buffer controller
from demkit.components.ctrl.bufConvCtrl import BufConvCtrl 	# BufferConverter

from demkit.components.ctrl.groupCtrl import GroupCtrl		# Group controller to control multiple devices, implements Profile Steering

from demkit.components.ctrl.thermal.thermalBufConvCtrl import ThermalBufConvCtrl

from demkit.components.ctrl.auction.btsAuctionCtrl import BtsAuctionCtrl
from demkit.components.ctrl.auction.tsAuctionCtrl import TsAuctionCtrl
from demkit.components.ctrl.auction.bufAuctionCtrl import BufAuctionCtrl
from demkit.components.ctrl.auction.bufConvAuctionCtrl import BufConvAuctionCtrl
from demkit.components.ctrl.auction.loadAuctionCtrl import LoadAuctionCtrl
from demkit.components.ctrl.auction.curtAuctionCtrl import CurtAuctionCtrl
from demkit.components.ctrl.auction.aggregatorCtrl import AggregatorCtrl
from demkit.components.ctrl.auction.auctioneerCtrl import AuctioneerCtrl
from demkit.components.ctrl.auction.thermal.thermalBufConvAuctionCtrl import ThermalBufConvAuctionCtrl

# Planned Auction controllers, follows same reasoning
from demkit.components.ctrl.plannedAuction.paBtsCtrl import PaBtsCtrl
from demkit.components.ctrl.plannedAuction.paLoadCtrl import PaLoadCtrl
from demkit.components.ctrl.plannedAuction.paCurtCtrl import PaCurtCtrl
from demkit.components.ctrl.plannedAuction.paBufCtrl import PaBufCtrl
from demkit.components.ctrl.plannedAuction.paBufConvCtrl import PaBufConvCtrl
from demkit.components.ctrl.plannedAuction.paTsCtrl import PaTsCtrl
from demkit.components.ctrl.plannedAuction.paGroupCtrl import PaGroupCtrl
from demkit.components.ctrl.plannedAuction.thermal.thermalPaBufConvCtrl import ThermalPaBufConvCtrl

# Import physical network
from demkit.components.flow.el.lvNode import LvNode
from demkit.components.flow.el.lvCable import LvCable
from demkit.components.flow.el.elLoadFlow import ElLoadFlow