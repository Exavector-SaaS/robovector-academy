from contextvars import ContextVar

_current_organization: ContextVar = ContextVar("current_organization", default=None)


def set_current_organization(org):
    _current_organization.set(org)


def get_current_organization():
    return _current_organization.get()


def clear_current_organization():
    _current_organization.set(None)
