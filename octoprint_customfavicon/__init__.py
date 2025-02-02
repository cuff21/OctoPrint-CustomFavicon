# coding=utf-8

import octoprint.plugin
import os
import octoprint.filemanager
import octoprint.filemanager.util
import datetime

class customfavicon(octoprint.plugin.AssetPlugin,
				octoprint.plugin.TemplatePlugin,
                octoprint.plugin.SettingsPlugin):
	
	##-- AssetPlugin mixin
	def get_assets(self):
		return dict(js=["js/customfavicon.js"])

	##-- Settings mixin
	def get_settings_defaults(self):
		return dict(favicon_url="/static/img/apple-touch-icon-114x114.png", icon_url="/static/img/tentacle-20x20.png", uploaded_url="")

	def get_settings_version(self):
		return 1
		
	def on_settings_migrate(self, target, current=None):
		if current is None or current < 1:
			migration_url = self._settings.get(["favicon_url"])
			self._logger.info(migration_url)
			if migration_url.startswith("/plugin/customfavicon/uploaded"):
				new_favicon_url = migration_url.replace("/plugin/custombfavicon/uploaded", "/plugin/customfavicon/custom/uploaded")
				self._logger.info(new_favicon_url)
				self._settings.set(["favicon_url"], new_favicon_url)
				self._settings.set(["uploaded_url"], new_favicon_url)

	##-- Template mixin
	def get_template_configs(self):
		return [dict(type="settings",custom_bindings=True)]

	##-- Image upload extenstion tree hook
	def get_extension_tree(self, *args, **kwargs):
		return dict(
			machinecode=dict(
				customfavicon=["png", "PNG"]
			)
		)
	
	##~~ Image upload preprocessor hook	
	def customfaviconupload(self, path, file_object, links=None, printer_profile=None, allow_overwrite=True, *args, **kwargs):
		img_extension_tree = self.get_extension_tree()
		img_extensions = img_extension_tree.get("machinecode").get("customfavicon")
		name, extension = os.path.splitext(file_object.filename)
		if name == "icon":
			self._logger.info("Setting icon url for " + path)
			#file_object.save(self.get_plugin_data_folder() + "/uploaded" + extension)
			octoprint.filemanager.util.StreamWrapper(self.get_plugin_data_folder() + "/icon" + extension, file_object.stream()).save(self.get_plugin_data_folder() + "/icon" + extension)
			self._logger.info(self.get_plugin_data_folder() + "/icon" + extension)
			self._settings.set(["icon_url"], "/plugin/customfavicon/custom/icon{}?{:%Y%m%d%H%M%S}".format(extension, datetime.datetime.now()))
			self._settings.save()
			self._plugin_manager.send_plugin_message(self._identifier, dict(type="reload"))
			return file_object
		if extension.replace(".", "") in img_extensions:
			self._logger.info("Setting favicon url for " + path)
			# file_object.save(self.get_plugin_data_folder() + "/uploaded" + extension)
			octoprint.filemanager.util.StreamWrapper(self.get_plugin_data_folder() + "/uploaded" + extension, file_object.stream()).save(self.get_plugin_data_folder() + "/uploaded" + extension)
			self._logger.info(self.get_plugin_data_folder() + "/uploaded" + extension)
			self._settings.set(["favicon_url"], "/plugin/customfavicon/custom/uploaded{}?{:%Y%m%d%H%M%S}".format(extension, datetime.datetime.now()))
			self._settings.set(["uploaded_url"], "/plugin/customfavicon/custom/uploaded{}?{:%Y%m%d%H%M%S}".format(extension, datetime.datetime.now()))
			self._settings.save()
			self._plugin_manager.send_plugin_message(self._identifier, dict(type="reload"))
		return file_object
		
	##~~ Routes hook
	def route_hook(self, server_routes, *args, **kwargs):
		from octoprint.server.util.tornado import LargeResponseHandler, UrlProxyHandler, path_validation_factory
		from octoprint.util import is_hidden_path
		return [
				(r"/custom/(.*)", LargeResponseHandler, dict(path=self.get_plugin_data_folder(),
																as_attachment=True,
																path_validation=path_validation_factory(lambda path: not is_hidden_path(path),status_code=404)))
				]
		
	##~~ Softwareupdate hook
	def get_version(self):
		return self._plugin_version
		
	def get_update_information(self):
		return dict(
			customfavicon=dict(
				displayName="Custom Favicon",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="cuff21",
				repo="OctoPrint-CustomFavicon",
				current=self._plugin_version,
				stable_branch=dict(
					name="Stable", branch="master", comittish=["master"]
				),
				prerelease_branches=[
					dict(
						name="Release Candidate",
						branch="rc",
						comittish=["rc", "master"],
					)
				],

				# update method: pip
				pip="https://github.com/cuff21/OctoPrint-CustomFavicon/archive/{target_version}.zip"
			)
		)

__plugin_name__ = "Custom Favicon"
__plugin_pythoncompat__ = ">=2.7,<4"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = customfavicon()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
		"octoprint.filemanager.extension_tree": __plugin_implementation__.get_extension_tree,
		"octoprint.filemanager.preprocessor": __plugin_implementation__.customfaviconupload,
		"octoprint.server.http.routes": __plugin_implementation__.route_hook
	}
