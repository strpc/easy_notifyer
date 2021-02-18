class ConfigError(Exception):
    """Erorr configuration"""
    def __init__(self, **kwargs):
        self.message = f'Configuration error. {kwargs}'
        super().__init__(self.message)
