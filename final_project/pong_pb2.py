# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: pong.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\npong.proto\x12\x04pong\"\x07\n\x05\x45mpty\"T\n\tGameReady\x12\r\n\x05ready\x18\x01 \x01(\x08\x12\x10\n\x08player_1\x18\x02 \x01(\t\x12\x10\n\x08player_2\x18\x03 \x01(\t\x12\x14\n\x0c\x66irst_player\x18\x04 \x01(\x08\")\n\x05Score\x12\x11\n\tplayer_id\x18\x01 \x01(\t\x12\r\n\x05score\x18\x02 \x01(\x05\".\n\x0ePaddlePosition\x12\x11\n\tplayer_id\x18\x01 \x01(\t\x12\t\n\x01x\x18\x02 \x01(\x02\"0\n\x0ePaddleMovement\x12\x11\n\tplayer_id\x18\x01 \x01(\t\x12\x0b\n\x03key\x18\x02 \x01(\x05\x32j\n\nPongServer\x12)\n\x04move\x12\x14.pong.PaddleMovement\x1a\x0b.pong.Empty\x12\x31\n\x0finitialize_game\x12\x0b.pong.Empty\x1a\x0f.pong.GameReady0\x01\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'pong_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _EMPTY._serialized_start=20
  _EMPTY._serialized_end=27
  _GAMEREADY._serialized_start=29
  _GAMEREADY._serialized_end=113
  _SCORE._serialized_start=115
  _SCORE._serialized_end=156
  _PADDLEPOSITION._serialized_start=158
  _PADDLEPOSITION._serialized_end=204
  _PADDLEMOVEMENT._serialized_start=206
  _PADDLEMOVEMENT._serialized_end=254
  _PONGSERVER._serialized_start=256
  _PONGSERVER._serialized_end=362
# @@protoc_insertion_point(module_scope)
