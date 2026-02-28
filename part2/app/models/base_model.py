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

        # timestamps (keep provided values when rebuilding from persisted data)
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
        ``setattr`` is used so property setters on subclasses are
        triggered, keeping validation in one place.
        """
        for key, value in data.items():
            if key in {'id', 'created_at'}:
                continue
            setattr(self, key, value)
        self.save()

    def to_dict(self):
        """Return a dict representation with ISO-formatted timestamps.

        Private backing attributes (``_name``, ``_description``, …) are
        skipped — subclasses expose those fields through their own
        ``to_dict()`` via property access, avoiding double-serialization
        of the same data under a mangled name.
        """
        result = {}
        for k, v in self.__dict__.items():
            if k.startswith('_'):
                continue            # exposed cleanly by subclass to_dict()
            result[k] = v.isoformat() if isinstance(v, datetime) else v
        return result
