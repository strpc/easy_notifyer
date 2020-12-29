from typing import Dict, Optional
from uuid import uuid4


class MultiPartForm:
    """Creating body of request"""
    def __init__(self, body: Optional[Dict] = None, files: Optional[Dict] = None):
        self._body = body
        self._files = files
        self.boundary = uuid4().hex

    def __bytes__(self):
        return self.encode()

    @staticmethod
    def _form_data(name: str) -> str:
        """Get formdata for input in body"""
        return f'Content-Disposition: form-data; name="{name}"'

    @staticmethod
    def _attached_file(name: str, filename: str) -> str:
        """Get formdata of file for input in body"""
        return f'Content-Disposition: form-data; name="{name}"; filename="{filename}"'

    @property
    def header(self) -> Dict[str, str]:
        """Get a header request"""
        return {'Content-type': f'multipart/form-data; boundary={self.boundary}'}

    def encode(self) -> bytes:
        """Create a body request."""
        body = []
        boundary = b'--' + self.boundary.encode('utf-8')
        if self._body is not None and isinstance(self._body, dict):
            for name, value in self._body.items():
                body.append(boundary)
                body.append(self._form_data(name).encode('utf-8'))
                body.append(b'')
                body.append(str(value).encode('utf-8'))

        if self._files is not None and isinstance(self._files, dict):
            for fieldname in self._files:
                if len(self._files[fieldname]) != 2:
                    continue
                filename, data = self._files[fieldname]
                body.append(boundary)
                body.append(self._attached_file(fieldname, filename).encode('utf-8'))
                body.append(b'')
                if hasattr(data, 'read') is True:
                    body.append(data.read())
                elif hasattr(data, 'encode') is True:
                    body.append(data.encode('utf-8'))

        body.append(boundary + b'--')
        return b"\r\n".join(body)
