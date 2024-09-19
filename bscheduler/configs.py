from brq.configs import BrqConfig


class SQLSettingsMixin:
    pass


class BSchedulerSettings(BrqConfig, SQLSettingsMixin):
    """
    Here we extend the BrqConfig with SQLSettingsMixin.

    The `env_prefix` is still `brq_` and `env_file` is still `.env`.
    """

    redis_key_prefix: str = "bscheduler"
