from eve import Eve
from threading import Thread
from flask import Blueprint, jsonify, request, Response
import json

from demkit.components.dev.haDev import HADev
from demkit.components.dev.meterDev import MeterDev
from demkit.components.hosts.restHost import RestHost
from util.Complex import replace_complex
from util.ComposerStatus import ComposerStatus
from util.entities import EntityDeserializer
from util.entities.ModelRestEntity import ModelRestEntity

from demkit.conf.usrconf import demCfg


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from util.ModelRestComposer import ModelRestComposer


def send_func_result(result):
	if result is None:
		return Response(status=200)
	else:
		# print(replace_complex(result))
		return jsonify(replace_complex(result))

class RestApi:
	def __init__(
		self, composer: 'ModelRestComposer', port: int, address: str = "0.0.0.0"
	):
		self.composer = composer
		self.port = port
		self.address = address
		self.host: RestHost = None

		settings = {"X_DOMAINS": "*", "DOMAIN": {"": {}}}
		self.app = Eve(settings=settings)
		config_routes = self.addConfigRoutes()
		sim_routes = self.addSimRoutes()
		meta_routes = self.addMetaRoutes()
		sim_control_routes = self.addSimControlRoutes()

		self.app.register_blueprint(config_routes)
		self.app.register_blueprint(sim_control_routes)
		self.app.register_blueprint(sim_routes)
		self.app.register_blueprint(meta_routes)


	def start(self):
		self.thread = Thread(target=self._start)
		# self.thread.daemon = True
		self.thread.start()

	def _start(self):
		print(f"Starting REST API on {self.address}:{self.port}")

		from waitress import serve
		serve(self.app, host=self.address, port=self.port)

	def addMetaRoutes(self):
		app = Blueprint(name="meta", import_name="meta")

		@app.route("/composer", methods=["GET"])
		def get_status():
			status: ComposerStatus = self.composer.status
			return Response(status.value, content_type="text/plain")  # Return plaintext response

		@app.route("/composer/reset", methods=["POST"])
		def reset_sim():
			self.composer.reset()
			return jsonify(self.composer.sim_params)

		@app.route("/composer/start", methods=["POST"])
		def start_simulation():
			self.composer.start()
			return jsonify(True)

		return app

	def addSimControlRoutes(self):
		app = Blueprint(name="simulation", import_name="simulation")


		@app.before_request
		def check_sim():
			if self.composer.status != ComposerStatus.ACTIVE:
				return Response("Simulation is not running", status=503, content_type="text/plain")

		@app.route("/simulation/pause", methods=["POST"])
		def stop_simulation():
			self.composer.host.inner.pauseSim()
			return jsonify(True)

		@app.route("/simulation/resume", methods=["POST"])
		def resume_simulation():
			self.composer.host.inner.resumeSim()
			return jsonify(True)

		@app.route("/simulation/setTime", methods=["POST"])
		def set_time():
			data = json.loads(request.data.decode("utf-8"))
			time = data["time"]

			if self.composer.host.inner.currentTime > time:
				return Response("Time cannot be set to the past", status=400, content_type="text/plain")

			self.composer.host.inner.setTime(time)
			return jsonify(True)

		return app

	def addConfigRoutes(self):
		app = Blueprint(name="composer", url_prefix="/composer", import_name="composer")

		@app.before_request
		def check_sim():
			if self.composer.status != ComposerStatus.INACTIVE:
				return Response("Simulation is either loaded or active", status=503, content_type="text/plain")

		@app.route("/config", methods=["POST"])
		def set_config():
			data = json.loads(request.data.decode("utf-8"))
			self.composer.sim_params = data
			return jsonify(data)

		@app.route("/entities", methods=["PUT"])
		def add_entity():
			data = json.loads(request.data.decode("utf-8"))
			try:
				entity: ModelRestEntity = EntityDeserializer.deserialize(data)
				self.composer.add(entity)
			except Exception as e:
				print(f"Error adding entity: {e}")
				return Response(f"Error adding entity: {e}", status=400, content_type="text/plain")
			return jsonify(True)

		@app.route("/entities/<entity_name>", methods=["DELETE"])
		def remove_entity(entity_name):
			if entity_name is None:
				return Response(status=400, content_type="text/plain")

			success: bool = self.composer.remove(entity_name)

			if success:
				return Response(status=200, content_type="text/plain")

			return Response(status=404, content_type="text/plain")

		@app.route("/entities", methods=["GET"])
		def get_entities():
			entities = self.composer.entities
			return jsonify(map()(lambda x: x.name, entities))

		@app.route("/load", methods=["POST"])
		def load_entities():
			try:
				self.composer.load()
			except Exception as e:
				print(f"Error loading entities: {e}")
				return Response(f"Error loading entities: {e}", status=500, content_type="text/plain")
			return jsonify(True)

		return app

	def addSimRoutes(self):
		app = Blueprint(name="sim", import_name="sim")

		@app.route("/entity", methods=['POST'])
		def addEntity():
			data = json.loads(request.data.decode("utf-8"))
			haEntity = data['entity_id']
			baseURL = demCfg['coreURL']
			dev = HADev(f"HALoad-{haEntity}", self.composer.host.inner, baseURL, f'houses/0/entity/{haEntity}/consumption')
			dev.startup()

			# TODO: FIX ME:
			self.composer.meters[0].inner.addDevice(dev)
			
			return json.dumps({"success": True})

		@app.before_request
		def check_host():
			self.host = self.composer.host.inner if self.composer.host is not None else None
			if self.host is None:
				return Response("Host is not available", status=503, content_type="text/plain")

		# Get the current host time
		@app.route("/time")
		def get_time():
			current_time = str(self.host.time())
			return Response(current_time, status=200, content_type="text/plain")

		# List all loaded entities in host environment
		@app.route("/list")
		def list_entities():
			entity_names = list(map(lambda x: x.name, self.host.entities))
			return jsonify(entity_names)

		# Call a function without parameters
		@app.route("/call/<entity>/<function>")
		def call_func(entity, function):
			print(f"Call {entity}.{function}")
			result = self.host.callFunction(entity, function)

			return send_func_result(result)

		# Call a function with parameters
		@app.route("/callp/<entity>/<function>", methods=["PUT"])
		def call_func_params(entity, function):
			print(f"Call {entity}.{function} with parameters")
			args = json.loads(request.data.decode("utf-8"))
			result = self.host.callFunction(entity, function, args)

			return send_func_result(result)

		# Set a variable value
		@app.route("/set/<entity>/<var>/<val>")
		def set_var(entity, var, val):
			print(f"Set {entity}.{var} = {val}")
			success = self.host.setVar(entity, var, val)

			if success:
				return Response(str(success), status=200, content_type="text/plain")
			else:
				return Response(status=500, content_type="text/plain")

		@app.route("/get/<entity>/<var>")
		def get_var(entity, var):
			print(f"Get {entity}.{var}")
			val = self.host.getVar(entity, var)

			if val is not None:
				return jsonify(replace_complex(val))
			else:
				return Response(status=404, content_type="text/plain")

		return app
