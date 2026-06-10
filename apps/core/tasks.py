from celery import Task


class TenantTask(Task):
    def __call__(self, *args, **kwargs):
        self.organization_id = kwargs.pop("organization_id", None)
        return self.run(*args, **kwargs)
