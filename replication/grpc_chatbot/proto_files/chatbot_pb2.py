# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chatbot.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rchatbot.proto\x12\x07\x63hatbot\"\x1f\n\x0bUserRequest\x12\x10\n\x08username\x18\x01 \x01(\t\"K\n\x0eMessageRequest\x12\x16\n\x0elogged_in_user\x18\x01 \x01(\t\x12\x10\n\x08username\x18\x02 \x01(\t\x12\x0f\n\x07message\x18\x03 \x01(\t\"$\n\nGetRequest\x12\x16\n\x0elogged_in_user\x18\x01 \x01(\t\"\x1f\n\x0bListRequest\x12\x10\n\x08wildcard\x18\x01 \x01(\t\"?\n\x0bSyncRequest\x12\x11\n\tfrom_hash\x18\x01 \x01(\t\x12\x0f\n\x07to_hash\x18\x02 \x01(\t\x12\x0c\n\x04\x64iff\x18\x03 \x01(\t\"\x1f\n\x0e\x46ullStateReply\x12\r\n\x05state\x18\x01 \x01(\t\"\x1e\n\tHeartbeat\x12\x11\n\tserver_id\x18\x01 \x01(\t\"\x07\n\x05\x45mpty\"7\n\x0c\x43hatbotReply\x12\x0f\n\x07message\x18\x01 \x01(\t\x12\x16\n\x0eSET_LOGIN_USER\x18\x02 \x01(\t2\xa4\x04\n\x07\x43hatBot\x12<\n\x0b\x63reate_user\x12\x14.chatbot.UserRequest\x1a\x15.chatbot.ChatbotReply\"\x00\x12@\n\x0csend_message\x12\x17.chatbot.MessageRequest\x1a\x15.chatbot.ChatbotReply\"\x00\x12;\n\x0bget_message\x12\x13.chatbot.GetRequest\x1a\x15.chatbot.ChatbotReply\"\x00\x12;\n\nlist_users\x12\x14.chatbot.ListRequest\x1a\x15.chatbot.ChatbotReply\"\x00\x12<\n\x0b\x64\x65lete_user\x12\x14.chatbot.UserRequest\x1a\x15.chatbot.ChatbotReply\"\x00\x12;\n\nlogin_user\x12\x14.chatbot.UserRequest\x1a\x15.chatbot.ChatbotReply\"\x00\x12\x34\n\nsync_state\x12\x14.chatbot.SyncRequest\x1a\x0e.chatbot.Empty\"\x00\x12;\n\x0eget_full_state\x12\x0e.chatbot.Empty\x1a\x17.chatbot.FullStateReply\"\x00\x12\x31\n\theartbeat\x12\x12.chatbot.Heartbeat\x1a\x0e.chatbot.Empty\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'chatbot_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _USERREQUEST._serialized_start=26
  _USERREQUEST._serialized_end=57
  _MESSAGEREQUEST._serialized_start=59
  _MESSAGEREQUEST._serialized_end=134
  _GETREQUEST._serialized_start=136
  _GETREQUEST._serialized_end=172
  _LISTREQUEST._serialized_start=174
  _LISTREQUEST._serialized_end=205
  _SYNCREQUEST._serialized_start=207
  _SYNCREQUEST._serialized_end=270
  _FULLSTATEREPLY._serialized_start=272
  _FULLSTATEREPLY._serialized_end=303
  _HEARTBEAT._serialized_start=305
  _HEARTBEAT._serialized_end=335
  _EMPTY._serialized_start=337
  _EMPTY._serialized_end=344
  _CHATBOTREPLY._serialized_start=346
  _CHATBOTREPLY._serialized_end=401
  _CHATBOT._serialized_start=404
  _CHATBOT._serialized_end=952
# @@protoc_insertion_point(module_scope)
