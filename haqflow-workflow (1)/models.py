
from dataclasses import dataclass, asdict
from typing import Optional


VALID_STATUSES = {
    "PENDING",
    "IN_PROGRESS",
    "COMPLETED",
    "BLOCKED"
}


VALID_PRIORITIES = {
    "HIGH",
    "MEDIUM",
    "LOW"
}


@dataclass
class ActionItem:

    id: str
    title: str
    priority: str
    status: str
    related_program_id: Optional[str] = None
    related_program_name: Optional[str] = None
    source: Optional[str] = None

    def validate(self):

        if self.status not in VALID_STATUSES:
            raise ValueError(
                f"Invalid status: {self.status}. "
                f"Valid statuses are: {VALID_STATUSES}"
            )

        if self.priority not in VALID_PRIORITIES:
            raise ValueError(
                f"Invalid priority: {self.priority}. "
                f"Valid priorities are: {VALID_PRIORITIES}"
            )

        if not self.id:
            raise ValueError("ActionItem must have an id.")

        if not self.title:
            raise ValueError("ActionItem must have a title.")

        return True

    def to_dict(self):

        self.validate()

        return asdict(self)
