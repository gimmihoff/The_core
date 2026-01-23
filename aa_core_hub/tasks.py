from celery import shared_task

@shared_task
def ping_core_hub() -> str:
    return "aa_core_hub ok"
