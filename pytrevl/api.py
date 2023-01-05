"""Wrapper around x-middle API."""
from json import dumps
from os import environ
from posixpath import join as url_join
from typing import Optional, TYPE_CHECKING
from cube_js_client import CubeJsClient

import requests

if TYPE_CHECKING:
    from .dashboard import Dashboard


_xmiddle = None
_cube = None

def cube(server: str="CUBE_SERVER", secret: str="CUBE_SECRET"):
    global _cube
    if not _cube:
        _cube = CubeJsClient(server=environ[server], secret=environ[secret])
    return _cube

def xmiddle(*args, **kwargs):
    global _xmiddle
    if not _xmiddle:
        _xmiddle = XMiddleService.from_env(*args, **kwargs)
    return _xmiddle

class RenderError(Exception):
    def __init__(self, parent_error):
        try:
            super().__init__(f'Rendering failed ({parent_error.request.url}):\n{dumps(parent_error.response.json(), indent=2)}')
        except:
            super().__init__(str(parent_error))
        self.parent_error = parent_error

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

    # The schemaVersion used when requesting x-middle API.
    schema_version: str = "v2"

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
        try:
            return self._session.get(url_join(self.api_root, 'status')).json()
        except ValueError:
            raise Exception("Empty response body. Have you provided the correct authentication username and/or password?")

    def __call__(self, dashboard: "Dashboard", event=None, state=None) -> dict:
        """Render a dashboard through the API."""
        body = {
            'schemaVersion': self.schema_version,
            'abstractConfig': dashboard.serialize(),
        }
        if event:
            body['event'] = event
        if state:
            body['state'] = state
        resp = self._session.post(self.api_root, json=body)
        try:
            resp.raise_for_status()
        except requests.HTTPError as e:
            raise RenderError(e)
        return resp.json()