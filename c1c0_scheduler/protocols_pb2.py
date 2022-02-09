# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: protocols.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='protocols.proto',
  package='scheduler',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0fprotocols.proto\x12\tscheduler\"\x97\x01\n\nSysRequest\x12\x0e\n\x06sender\x18\x01 \x01(\t\x12\x0b\n\x03\x63md\x18\x02 \x01(\t\x12\x16\n\trecipient\x18\x03 \x01(\tH\x00\x88\x01\x01\x12\x11\n\x04\x64\x61ta\x18\x04 \x01(\tH\x01\x88\x01\x01\x12\x19\n\x0crefresh_rate\x18\x05 \x01(\x02H\x02\x88\x01\x01\x42\x0c\n\n_recipientB\x07\n\x05_dataB\x0f\n\r_refresh_rate\"\x1f\n\x0bSysResponse\x12\x10\n\x08response\x18\x01 \x01(\t2\x91\x01\n\tScheduler\x12=\n\nSysCommand\x12\x15.scheduler.SysRequest\x1a\x16.scheduler.SysResponse\"\x00\x12\x45\n\x10SysCommandStream\x12\x15.scheduler.SysRequest\x1a\x16.scheduler.SysResponse\"\x00\x30\x01\x62\x06proto3'
)




_SYSREQUEST = _descriptor.Descriptor(
  name='SysRequest',
  full_name='scheduler.SysRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='sender', full_name='scheduler.SysRequest.sender', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='cmd', full_name='scheduler.SysRequest.cmd', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='recipient', full_name='scheduler.SysRequest.recipient', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='data', full_name='scheduler.SysRequest.data', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='refresh_rate', full_name='scheduler.SysRequest.refresh_rate', index=4,
      number=5, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='_recipient', full_name='scheduler.SysRequest._recipient',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
    _descriptor.OneofDescriptor(
      name='_data', full_name='scheduler.SysRequest._data',
      index=1, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
    _descriptor.OneofDescriptor(
      name='_refresh_rate', full_name='scheduler.SysRequest._refresh_rate',
      index=2, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=31,
  serialized_end=182,
)


_SYSRESPONSE = _descriptor.Descriptor(
  name='SysResponse',
  full_name='scheduler.SysResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='response', full_name='scheduler.SysResponse.response', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=184,
  serialized_end=215,
)

_SYSREQUEST.oneofs_by_name['_recipient'].fields.append(
  _SYSREQUEST.fields_by_name['recipient'])
_SYSREQUEST.fields_by_name['recipient'].containing_oneof = _SYSREQUEST.oneofs_by_name['_recipient']
_SYSREQUEST.oneofs_by_name['_data'].fields.append(
  _SYSREQUEST.fields_by_name['data'])
_SYSREQUEST.fields_by_name['data'].containing_oneof = _SYSREQUEST.oneofs_by_name['_data']
_SYSREQUEST.oneofs_by_name['_refresh_rate'].fields.append(
  _SYSREQUEST.fields_by_name['refresh_rate'])
_SYSREQUEST.fields_by_name['refresh_rate'].containing_oneof = _SYSREQUEST.oneofs_by_name['_refresh_rate']
DESCRIPTOR.message_types_by_name['SysRequest'] = _SYSREQUEST
DESCRIPTOR.message_types_by_name['SysResponse'] = _SYSRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

SysRequest = _reflection.GeneratedProtocolMessageType('SysRequest', (_message.Message,), {
  'DESCRIPTOR' : _SYSREQUEST,
  '__module__' : 'protocols_pb2'
  # @@protoc_insertion_point(class_scope:scheduler.SysRequest)
  })
_sym_db.RegisterMessage(SysRequest)

SysResponse = _reflection.GeneratedProtocolMessageType('SysResponse', (_message.Message,), {
  'DESCRIPTOR' : _SYSRESPONSE,
  '__module__' : 'protocols_pb2'
  # @@protoc_insertion_point(class_scope:scheduler.SysResponse)
  })
_sym_db.RegisterMessage(SysResponse)



_SCHEDULER = _descriptor.ServiceDescriptor(
  name='Scheduler',
  full_name='scheduler.Scheduler',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=218,
  serialized_end=363,
  methods=[
  _descriptor.MethodDescriptor(
    name='SysCommand',
    full_name='scheduler.Scheduler.SysCommand',
    index=0,
    containing_service=None,
    input_type=_SYSREQUEST,
    output_type=_SYSRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='SysCommandStream',
    full_name='scheduler.Scheduler.SysCommandStream',
    index=1,
    containing_service=None,
    input_type=_SYSREQUEST,
    output_type=_SYSRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_SCHEDULER)

DESCRIPTOR.services_by_name['Scheduler'] = _SCHEDULER

# @@protoc_insertion_point(module_scope)
