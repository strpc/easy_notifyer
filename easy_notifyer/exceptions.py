class ConfigError(Exception):
    def __init__(self, **kwargs):
        self.message = f'Configuration error. {kwargs}'
        super().__init__(self.message)
