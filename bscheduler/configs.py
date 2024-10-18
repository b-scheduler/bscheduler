from brq.configs import BrqConfig


class DatabaseSettingsMixin:
    pass


class BSchedulerSettings(BrqConfig, DatabaseSettingsMixin):
    """
    Here we extend the BrqConfig with SQLSettingsMixin.

    The `env_prefix` is still `brq_` and `env_file` is still `.env`.
    """

    redis_key_prefix: str = "bscheduler"
