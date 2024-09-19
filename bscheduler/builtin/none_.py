from bscheduler.task import task

FUNCTION_NAME = "_none"


@task(register_function_name=FUNCTION_NAME)
def none(*args, **kwargs):
    return
