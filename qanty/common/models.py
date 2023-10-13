# -*- coding: UTF-8 -*-

import pydantic
from typing import Optional


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


class Line(pydantic.BaseModel):
    id: str
    name: str
    chars: str
    waiting_tickets: int
    last_event: int
    enabled: bool
    deleted: bool
    metrics: LineMetrics

    model_config = {"frozen": True}
