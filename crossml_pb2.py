# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: crossml.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='crossml.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=b'\n\rcrossml.proto\"\xd7\x03\n\x11\x43rossoutMLSetting\x12\x14\n\x0c\x64isplayIndex\x18\x01 \x01(\x05\x12\x10\n\x08\x66ullAuto\x18\x02 \x01(\x08\x12\x15\n\rdisplayShiftX\x18\x03 \x01(\x05\x12\x15\n\rdisplayShiftY\x18\x04 \x01(\x05\x12\x13\n\x0bmouseShiftX\x18\x05 \x01(\x05\x12\x13\n\x0bmouseShiftY\x18\x06 \x01(\x05\x12\x13\n\x0b\x63\x61rMaxSpeed\x18\x07 \x01(\x05\x12\x1f\n\x17\x63\x65nterFarDetectDistance\x18\x08 \x01(\x05\x12\x1f\n\x17\x63\x65nterLowDetectDistance\x18\t \x01(\x05\x12\x18\n\x10lrDetectDistance\x18\n \x01(\x05\x12\x19\n\x11\x66rontDetectDegree\x18\x0b \x01(\x05\x12\x18\n\x10targetDisplayFPS\x18\x0c \x01(\x05\x12\x14\n\x0c\x64\x65tectionFPS\x18\r \x01(\x05\x12\x17\n\x0fshowDebugWindow\x18\x0e \x01(\x08\x12\x1c\n\x14\x63heckStuckFrameCount\x18\x0f \x01(\x05\x12\x14\n\x0cisFullScreen\x18\x10 \x01(\x08\x12\x13\n\x0bstartScreen\x18\x11 \x01(\x05\x12$\n\x08\x61\x63\x63ounts\x18\x12 \x03(\x0b\x32\x12.CrossoutMLAccount\"7\n\x11\x43rossoutMLAccount\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\tb\x06proto3'
)




_CROSSOUTMLSETTING = _descriptor.Descriptor(
  name='CrossoutMLSetting',
  full_name='CrossoutMLSetting',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='displayIndex', full_name='CrossoutMLSetting.displayIndex', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='fullAuto', full_name='CrossoutMLSetting.fullAuto', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='displayShiftX', full_name='CrossoutMLSetting.displayShiftX', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='displayShiftY', full_name='CrossoutMLSetting.displayShiftY', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='mouseShiftX', full_name='CrossoutMLSetting.mouseShiftX', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='mouseShiftY', full_name='CrossoutMLSetting.mouseShiftY', index=5,
      number=6, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='carMaxSpeed', full_name='CrossoutMLSetting.carMaxSpeed', index=6,
      number=7, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='centerFarDetectDistance', full_name='CrossoutMLSetting.centerFarDetectDistance', index=7,
      number=8, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='centerLowDetectDistance', full_name='CrossoutMLSetting.centerLowDetectDistance', index=8,
      number=9, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='lrDetectDistance', full_name='CrossoutMLSetting.lrDetectDistance', index=9,
      number=10, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='frontDetectDegree', full_name='CrossoutMLSetting.frontDetectDegree', index=10,
      number=11, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='targetDisplayFPS', full_name='CrossoutMLSetting.targetDisplayFPS', index=11,
      number=12, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='detectionFPS', full_name='CrossoutMLSetting.detectionFPS', index=12,
      number=13, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='showDebugWindow', full_name='CrossoutMLSetting.showDebugWindow', index=13,
      number=14, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='checkStuckFrameCount', full_name='CrossoutMLSetting.checkStuckFrameCount', index=14,
      number=15, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='isFullScreen', full_name='CrossoutMLSetting.isFullScreen', index=15,
      number=16, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='startScreen', full_name='CrossoutMLSetting.startScreen', index=16,
      number=17, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='accounts', full_name='CrossoutMLSetting.accounts', index=17,
      number=18, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=18,
  serialized_end=489,
)


_CROSSOUTMLACCOUNT = _descriptor.Descriptor(
  name='CrossoutMLAccount',
  full_name='CrossoutMLAccount',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='username', full_name='CrossoutMLAccount.username', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='password', full_name='CrossoutMLAccount.password', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=491,
  serialized_end=546,
)

_CROSSOUTMLSETTING.fields_by_name['accounts'].message_type = _CROSSOUTMLACCOUNT
DESCRIPTOR.message_types_by_name['CrossoutMLSetting'] = _CROSSOUTMLSETTING
DESCRIPTOR.message_types_by_name['CrossoutMLAccount'] = _CROSSOUTMLACCOUNT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

CrossoutMLSetting = _reflection.GeneratedProtocolMessageType('CrossoutMLSetting', (_message.Message,), {
  'DESCRIPTOR' : _CROSSOUTMLSETTING,
  '__module__' : 'crossml_pb2'
  # @@protoc_insertion_point(class_scope:CrossoutMLSetting)
  })
_sym_db.RegisterMessage(CrossoutMLSetting)

CrossoutMLAccount = _reflection.GeneratedProtocolMessageType('CrossoutMLAccount', (_message.Message,), {
  'DESCRIPTOR' : _CROSSOUTMLACCOUNT,
  '__module__' : 'crossml_pb2'
  # @@protoc_insertion_point(class_scope:CrossoutMLAccount)
  })
_sym_db.RegisterMessage(CrossoutMLAccount)


# @@protoc_insertion_point(module_scope)
