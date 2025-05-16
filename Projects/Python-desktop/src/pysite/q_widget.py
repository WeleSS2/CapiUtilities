class q_widget:
    """
    Base widget class that can be configured with a title, color, size, and data source.
    Additional customization can be added by subclassing this class or extending its methods.
    """

    def __init__(self, title=None, color=None, size=None, data_source=None, **kwargs):
        # Initialize widget properties with provided values or defaults
        self.title = title if title is not None else "Untitled Widget"
        self.color = color if color is not None else "white"
        self.size = size if size is not None else (100, 100)  # size as (width, height)
        self.data_source = data_source if data_source is not None else None

        # Store any additional configuration parameters
        self._extra_config = kwargs

    def __repr__(self):
        return f"<q_widget title='{self.title}' color='{self.color}' size={self.size} data_source='{self.data_source}'>"

    def configure(self, config):
        """
        Update widget properties from a configuration dictionary.
        """
        if not isinstance(config, dict):
            raise ValueError("Configuration must be a dictionary.")

        self.title = config.get('title', self.title)
        self.color = config.get('color', self.color)
        self.size = config.get('size', self.size)
        self.data_source = config.get('data_source', self.data_source)

        # Update any extra configurations not covered by the main attributes
        for key, value in config.items():
            if not hasattr(self, key):
                self._extra_config[key] = value

    def render(self):
        """
        Placeholder method to 'render' the widget.
        Actual UI rendering would be implemented in a subclass or a GUI framework.
        """
        print(f"Rendering Widget - Title: {self.title}, Color: {self.color}, Size: {self.size}, Data: {self.data_source}")