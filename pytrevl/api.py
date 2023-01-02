"""Wrapper around x-middle API."""
from os import environ
from posixpath import join as url_join
from typing import Optional, TYPE_CHECKING

import requests

if TYPE_CHECKING:
    from .dashboard import Dashboard


_xmiddle = None


def xmiddle(*args, **kwargs):
    global _xmiddle
    if not _xmiddle:
        _xmiddle = XMiddleService.from_env(*args, **kwargs)
    return _xmiddle


class XMiddleService:
    """Simple wrapper for x-middle API endpoints.

    Examples
    --------
    >>> # Load configuration from environment
    >>> api = XMiddleService.from_env()
    >>> dashboard = # ...
    >>> # Call API with a dashboard ("rendering")
    >>> api(dashboard)
    {
        components: [ ... ],
        events: [ ... ],
        parameters: { ... },
    }
    """
    def __init__(self, base_url: str, auth_password: Optional[str]=None, auth_username: str="pytrevl"):
        """
        Use :method:`~XMiddleService.from_env` to create an instance using
        configuration from environment variables.

        Parameters
        ----------
        base_url
            The URL of the base of dashboard-API endpoint, i.e. without the
            final ``'dashboards'``.
        auth_password
            The password for HTTP-Basic auth for the API.
        auth_username
            The username for HTTP-Basic auth for the API.
        """
        self.api_root = url_join(base_url, 'dashboards')
        self._session = requests.Session()
        if auth_password:
            self._session.auth = requests.auth.HTTPBasicAuth(auth_username, auth_password)
        else:
            self._session = requests.Session()

    @classmethod
    def from_env(cls, base_url: str="X_MIDDLE_BASEURL", auth_password: str="X_MIDDLE_PASSWORD", **kwargs):
        base_url = environ[base_url]
        auth_password = environ[auth_password]
        return cls(base_url, auth_password, **kwargs)

    def status(self):
        return self._session.get(url_join(self.api_root, 'status')).json()

    def __call__(self, dashboard: "Dashboard", event=None, parameters=None) -> dict:
        """Render a dashboard through the API."""
        body = {
            'abstractDashoboardConfig': dashboard.serialize(),
        }
        if event:
            body['event'] = event
        if parameters:
            body['parameters'] = parameters
        resp = self._session.post(self.api_root, json=body)
        resp.raise_for_status()
        return resp.json()
