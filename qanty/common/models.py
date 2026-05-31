# -*- coding: UTF-8 -*-

import datetime
from urllib.parse import urlencode, urljoin

import pydantic
from typing import Any, Dict, List, Optional


class BranchLocation(pydantic.BaseModel):
    longitude: float
    latitude: float
    name: str
    address: str

    model_config = {"frozen": True}

    @classmethod
    @pydantic.field_validator("longitude")
    def validate_longitude(cls, value: float):
        if value < -180 or value > 180:
            raise ValueError("Longitude must be between -180 and 180")
        return value

    @classmethod
    @pydantic.field_validator("latitude")
    def validate_latitude(cls, value: float):
        if value < -90 or value > 90:
            raise ValueError("Latitude must be between -90 and 90")
        return value


class Branch(pydantic.BaseModel):
    id: str
    name: str
    gmt: str
    enabled: bool
    deleted: bool
    location: BranchLocation

    model_config = {"frozen": True}


class LineMetrics(pydantic.BaseModel):
    wait_avg: float
    wait_time: float
    min_wait_time: float
    max_wait_time: float
    serve_avg: float
    serve_time: float
    min_serve_time: float
    max_serve_time: float
    waiting_time_estimation: float

    model_config = {"frozen": True}


class AppointmentSettingsOperationRange(pydantic.BaseModel):
    howManyDays: int
    daysAhead: int


# TODO: This is incomplete
class AppointmentSettingsSetCalendars(pydantic.BaseModel):
    pass


class LineAppointmentSettings(pydantic.BaseModel):
    operationRange: AppointmentSettingsOperationRange
    setCalendars: List[AppointmentSettingsSetCalendars] = []
    cancelWindow: int
    sets: Dict[str, Any]
    enabled: bool


class Line(pydantic.BaseModel):
    id: str
    name: str
    chars: str
    waiting_tickets: int
    enabled: bool
    deleted: bool
    metrics: LineMetrics
    appointment_settings: LineAppointmentSettings
    color: Optional[str]

    model_config = {"frozen": True}


class AppointmentSlot(pydantic.BaseModel):
    index: str
    indexInsideSet: int
    duration: int
    appointment_slot_idx: int
    appointment_set: str
    attending_slot: str
    serve_as_group: bool
    status: str
    name: str


class AppointmentDaySchedule(pydantic.BaseModel):
    date_time: datetime.datetime
    slots: List[AppointmentSlot]

    model_config = {"frozen": True}


class Customer(pydantic.BaseModel):
    name: Optional[str] = None
    last_name: Optional[str] = None
    doc_type: Optional[str] = None
    doc_type_id: Optional[str] = None
    doc_id: Optional[str] = None
    email: Optional[str] = None
    phone_numbers: Optional[Dict[str, Any]] = None

    model_config = {"frozen": True}


class CreatedTicket(pydantic.BaseModel):
    ticket_name: str
    ticket_id: str
    video_call_id: Optional[str] = None
    vc_jwt: Optional[str] = None

    model_config = {"frozen": True}

    def video_call_url(self, company_id: str, portal_base_url: str = "https://qanty.com/") -> Optional[str]:
        if not self.video_call_id or not self.vc_jwt:
            return None

        portal_url = urljoin(portal_base_url.rstrip("/") + "/", "portals/tickets")
        query = urlencode({"c": company_id, "v": self.video_call_id, "j": self.vc_jwt})
        return f"{portal_url}?{query}"


class AssignedAppointment(pydantic.BaseModel):
    name: str
    status: str
    issue_date: int
    appointment_set: str
    appointment_slot_idx: int
    duration: int
    attending_slot: str
    video_call_id: str

    model_config = {"frozen": True}


class UserRole(pydantic.BaseModel):
    id: str
    name: str
    roleGroup: str
    enabled: bool
    hidden: bool
    deleted: bool
    rules: Dict[str, Any]

    model_config = {"frozen": True}


class User(pydantic.BaseModel):
    id: str
    name: str
    docId: str
    email: str
    enabled: bool
    hidden: bool
    deleted: bool
    role: UserRole
    lastName: Optional[str]
    docType: Optional[str]
    docTypeId: Optional[str]
    branches: Optional[List[str]]

    model_config = {"frozen": True}
