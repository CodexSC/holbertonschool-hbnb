# UUID for unique identifiers and datetime utilities (UTC-aware)
import uuid
from datetime import datetime, timezone


class BaseModel:
    """
    Base class for HBnB models.

    Provides a UUID `id` plus `created_at`/`updated_at` timestamps
    (UTC-aware) and common helpers used throughout the project. The
    constructor accepts ``**kwargs`` so instances can be reconstructed
    from persisted data.
    """

    def __init__(self, **kwargs):
        # identifier
        self.id = kwargs.get('id', str(uuid.uuid4()))

        # timestamps (keep provided values when rebuilding)
        now = datetime.now(timezone.utc)
        self.created_at = kwargs.get('created_at', now)
        self.updated_at = kwargs.get('updated_at', now)

        # assign any extra attributes passed via kwargs
        for key, value in kwargs.items():
            if key not in {'id', 'created_at', 'updated_at'}:
                setattr(self, key, value)

    def save(self):
        """Refresh the ``updated_at`` timestamp to current UTC time."""
        self.updated_at = datetime.now(timezone.utc)

    def update(self, data: dict):
        """Update attributes from a dict and bump ``updated_at``.

        Reserved fields ``id`` and ``created_at`` are ignored to avoid
        inadvertently altering identity or creation time.
        """
        for key, value in data.items():
            if key in {'id', 'created_at'}:
                continue
            setattr(self, key, value)
        self.save()

    def to_dict(self):
        """Return a dict representation with ISO‑formatted timestamps.

        Any :class:`datetime` values are converted to ``ISO`` strings so
        the result is JSON-serializable.
        """
        result = {}
        for k, v in self.__dict__.items():
            if isinstance(v, datetime):
                result[k] = v.isoformat()
            else:
                result[k] = v
        return result
