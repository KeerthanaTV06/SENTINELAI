"""Pydantic schemas for dataset events.

Defines NetworkEvent, PhishingEvent, MalwareEvent, ThreatEvent models used for
validation and pipeline processing.
"""
from __future__ import annotations

from typing import Optional
from pydantic import BaseModel, Field, validator


class NetworkEvent(BaseModel):
    """Schema for a network flow / connection event (NSL-KDD like).

    Fields are intentionally permissive to accommodate common dataset
    variations; downstream preprocessing will normalize names.
    """
    duration: Optional[float] = Field(None, description="Flow duration in seconds")
    protocol_type: Optional[str] = Field(None, description="Protocol (tcp/udp/icmp)")
    service: Optional[str] = Field(None, description="Service name")
    flag: Optional[str] = Field(None, description="Connection status flags")
    src_bytes: Optional[int] = Field(None, description="Source bytes")
    dst_bytes: Optional[int] = Field(None, description="Destination bytes")
    land: Optional[int] = Field(None)
    wrong_fragment: Optional[int] = Field(None)
    urgent: Optional[int] = Field(None)
    hot: Optional[int] = Field(None)
    num_failed_logins: Optional[int] = Field(None)
    logged_in: Optional[int] = Field(None)
    num_compromised: Optional[int] = Field(None)
    root_shell: Optional[int] = Field(None)
    su_attempted: Optional[int] = Field(None)
    num_root: Optional[int] = Field(None)
    num_file_creations: Optional[int] = Field(None)
    num_shells: Optional[int] = Field(None)
    num_access_files: Optional[int] = Field(None)
    num_outbound_cmds: Optional[int] = Field(None)
    is_hot_login: Optional[int] = Field(None)
    is_guest_login: Optional[int] = Field(None)
    count: Optional[int] = Field(None)
    srv_count: Optional[int] = Field(None)
    serror_rate: Optional[float] = Field(None)
    srv_serror_rate: Optional[float] = Field(None)
    rerror_rate: Optional[float] = Field(None)
    srv_rerror_rate: Optional[float] = Field(None)
    same_srv_rate: Optional[float] = Field(None)
    diff_srv_rate: Optional[float] = Field(None)
    srv_diff_host_rate: Optional[float] = Field(None)
    dst_host_count: Optional[int] = Field(None)
    dst_host_srv_count: Optional[int] = Field(None)
    dst_host_same_srv_rate: Optional[float] = Field(None)
    dst_host_diff_srv_rate: Optional[float] = Field(None)
    dst_host_same_src_port_rate: Optional[float] = Field(None)
    dst_host_srv_diff_host_rate: Optional[float] = Field(None)
    dst_host_serror_rate: Optional[float] = Field(None)
    dst_host_srv_serror_rate: Optional[float] = Field(None)
    dst_host_rerror_rate: Optional[float] = Field(None)
    dst_host_srv_rerror_rate: Optional[float] = Field(None)
    label: Optional[str] = Field(None, description="Attack label or 'normal'")

    @validator("protocol_type", "service", "flag", pre=True, always=True)
    def strip_strings(cls, v):
        if v is None:
            return v
        return str(v).strip().lower()


class PhishingEvent(BaseModel):
    """Schema for phishing dataset records (PhishTank).

    Fields cover common attributes for phishing URLs and metadata.
    """
    url: str = Field(..., description="Suspected phishing URL")
    phishtank_id: Optional[int] = None
    in_database: Optional[bool] = None
    valid: Optional[bool] = None
    submission_time: Optional[str] = None
    verification_time: Optional[str] = None
    details: Optional[str] = None


class MalwareEvent(BaseModel):
    """Schema for basic malware event metadata."""
    sample_id: Optional[str]
    md5: Optional[str]
    sha1: Optional[str]
    sha256: Optional[str]
    family: Optional[str]
    tags: Optional[str]
    first_seen: Optional[str]
    last_seen: Optional[str]


class ThreatEvent(BaseModel):
    """Generic threat event container used by pipelines to unify events."""
    event_id: Optional[str]
    source: Optional[str]
    timestamp: Optional[str]
    network: Optional[NetworkEvent]
    phishing: Optional[PhishingEvent]
    malware: Optional[MalwareEvent]
    meta: Optional[dict] = Field(default_factory=dict)
