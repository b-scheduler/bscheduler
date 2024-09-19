from functools import partial
from typing import Callable

from bscheduler.bscheduler.bfuture import BFuture
from bscheduler.configs import BSchedulerSettings
from bscheduler.log import logger


def workflow(
    _func=None,
    *,
    name: str | None = None,
    config: BSchedulerSettings | None = None,
    auto_parallel: bool = False,
):
    def _wrapper(
        func,
        name: str | None = None,
        config: BSchedulerSettings | None = None,
        auto_parallel: bool = False,
    ):

        return Workflow(
            func,
            name=name or func.__name__,
            config=config,
        )

    if not config:
        logger.info("Initializing config from environment variables and .env file")
        config = BSchedulerSettings()
    else:
        logger.info("Using custom config")
        config = config

    name = name or _func.__name__

    if _func is None:
        return partial(
            _wrapper,
            name=name,
            config=config,
            auto_parallel=auto_parallel,
        )
    else:
        return _wrapper(_func, name=name, config=config, auto_parallel=auto_parallel)


class Workflow:
    def __init__(
        self,
        func: Callable,
        name: str,
        config: BSchedulerSettings,
        auto_parallel: bool = False,
    ):
        self.func = func
        self.name = name
        self.config = config
        self.auto_parallel = auto_parallel
        self.ctx = Context(self.config)

        self.futures = self._compile()

    def _compile(self) -> list[tuple[BFuture]]:
        try:
            self.func()
        except Exception as e:
            logger.error(f"{e} when compiling workflow: {self.name}")
            raise

        if not self.auto_parallel:
            return [(f,) for f in self.ctx.futures]
        else:
            return self._build_parallel_workflow(self.ctx.futures)

    def _build_parallel_workflow(self, futures: list[BFuture]) -> list[tuple[BFuture]]:
        pass

    def deploy(self):
        pass

    def run(self):
        pass


class Context:
    def __init__(self) -> None:
        self.futures = []

    def clear(self):
        self.futures.clear()

    def wait_for(self, seconds: int) -> BFuture:
        return self.run(
            "_none",
            _defer_seconds=seconds,
        )

    def run(
        self,
        func_name: str,
        _defer_until=None,
        _defer_hours: int = 0,
        _defer_minutes: int = 0,
        _defer_seconds: int = 0,
        *args,
        **kwargs,
    ) -> BFuture:
        bf = BFuture(
            func_name=func_name,
            defer_args={
                "defer_until": _defer_until,
                "defer_hours": _defer_hours,
                "defer_minutes": _defer_minutes,
                "defer_seconds": _defer_seconds,
            },
            args=args or [],
            kwargs=kwargs or {},
        )

        self.futures.append(bf)
        return bf


@workflow
def main(ctx: Context) -> BFuture | dict[str, BFuture]:
    a_stage_result = ctx.run(
        "a_stage",
        1,
        a=2,
    )

    b_stage_result = ctx.run(
        "b_stage",
        a_stage_result,
    )

    return {
        "a_stage": a_stage_result,
        "b_stage": b_stage_result,
    }


if __name__ == "__main__":
    main.deploy()  # Deploy the workflow to bscheduler
    main.run()  # Run the server locally, need to run every function manually
