$(function() {
	function customfaviconViewModel(parameters) {
		var self = this;

		self.settings = parameters[0];

		self.favicon_url = ko.observable();
		self.icon_url = ko.observable();
		self.fillMethod = ko.observable();
		self.fillOptions = ko.observableArray([{
						name : 'auto',
						value : 'auto'
					}, {
						name : 'cover',
						value : 'cover'
					}, {
						name : 'contain',
						value : 'contain'
					}
				]);
		self.position = ko.observable();
		self.selectedBundledImage = ko.observable('')

		self.onBeforeBinding = function() {
			self.bundledImages = ko.observableArray([{
							name : 'OctoPrint',
							path : '/static/img/favicon.png'
						}, {
							name : 'Custom',
							path : self.settings.settings.plugins.customfavicon.uploaded_url()
						}, {
							name : 'jneilliii',
							path : '/plugin/customfavicon/static/img/jneilliii.png'
						}
					]);
			self.favicon_url(self.settings.settings.plugins.customfavicon.favicon_url());
			self.selectedBundledImage(self.settings.settings.plugins.customfavicon.favicon_url());
			self.icon_url(self.settings.settings.plugins.customfavicon.icon_url());
		}

		self.onAfterBinding = function() {
			//$("#temperature-graph").css({"background-image":"url('" + window.location.pathname.replace(/\/$/, '') + self.settings.settings.plugins.customfavicon.favicon_url() + "')"});
			$("#navbar .navbar-inner .brand span").css({"background-image":"url('" + window.location.pathname.replace(/\/$/, '') + self.settings.settings.plugins.customfavicon.icon_url() + "')"});
			
			$('head > link[rel="mask-icon-theme"][rel="mask-icon"][rel="apple-touch-icon"][rel="shortcut icon"][rel="manifest"][rel="icon"]').remove();
			$('head').append({'<link rel="icon" type="image/png" href="' + window.location.pathname.replace(/\/$/, '') + self.settings.settings.plugins.customfavicon.favicon_url() + '">'});
		}

		self.onSettingsSaved = function() {
			if(self.settings.settings.plugins.customfavicon.favicon_url() == '/static/img/favicon.png' || self.settings.settings.plugins.customfavicon.favicon_url() == '/plugin/customfavicon/static/img/jneilliii.png'){
				self.settings.settings.plugins.customfavicon.icon_url('/static/img/tentacle-20x20.png');
			}
		}

		self.onEventSettingsUpdated = function (payload) {
			self.favicon_url(self.settings.settings.plugins.customfavicon.favicon_url());
			self.icon_url(self.settings.settings.plugins.customfavicon.icon_url());
			self.bundledImages = ko.observableArray([{
							name : 'OctoPrint',
							path : '/static/img/favicon.png'
						}, {
							name : 'Custom',
							path : self.settings.settings.plugins.customfavicon.uploaded_url()
						}, {
							name : 'jneilliii',
							path : '/plugin/customfavicon/static/img/jneilliii.png'
						}
					]);

			//$("#temperature-graph").css({"background-image":"url('" + window.location.pathname.replace(/\/$/, '') + self.settings.settings.plugins.customfavicon.background_url() + "')"});
			$("#navbar .navbar-inner .brand span").css({"background-image":"url('" + window.location.pathname.replace(/\/$/, '') + self.settings.settings.plugins.customfavicon.icon_url() + "')"});
			
			$('head > link[rel="mask-icon-theme"][rel="mask-icon"][rel="apple-touch-icon"][rel="shortcut icon"][rel="manifest"][rel="icon"]').remove();
			$('head').append({'<link rel="icon" type="image/png" href="' + window.location.pathname.replace(/\/$/, '') + self.settings.settings.plugins.customfavicon.favicon_url() + '">'});
		
		}

		self.onDataUpdaterPluginMessage = function(plugin, data) {
			if (plugin != "customfavicon") {
				return;
			}

			if(data.type == "reload") {
				window.location.reload(true);
			}
		}
	}

	// This is how our plugin registers itself with the application, by adding some configuration
	// information to the global variable OCTOPRINT_VIEWMODELS
	ADDITIONAL_VIEWMODELS.push([
		// This is the constructor to call for instantiating the plugin
		customfaviconViewModel,

		// This is a list of dependencies to inject into the plugin, the order which you request
		// here is the order in which the dependencies will be injected into your view model upon
		// instantiation via the parameters argument
		["settingsViewModel"],

		// Finally, this is the list of selectors for all elements we want this view model to be bound to.
		["#settings_plugin_customfavicon_form"]
	]);
});
