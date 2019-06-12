# Flask Peanut Butter & Jelly
Flask-Pbj provides support for [Google Protocol Buffers](https://developers.google.com/protocol-buffers/docs/overview)
and json formatted request and response data. The api decorator serializes 
and deserializes json or protobuf formatted messages to and from a python 
dictionary.

## Why Flask-Pbj
Flask Peanut Butter and Jelly to simplifies the creation of REST APIs for C++
clients. Flask-pbj decorated app.routes accept and return protobuf messages or
JSON. The JSON is useful for debugging and public API's while Google Protobuf
is a well-documented compact and efficient format, particularly useful for
C++/Python communication.

## Examples
*example_messages.proto*
```
message Person {
    required int32 id = 1;
    required string name = 2;
    optional string email = 3;
}

message Team {
    required int32 id = 1;
    required string name = 2;
    required Person leader = 3
    repeated Person members = 4;
}
```
*app.py*
```python
# The route function can access the added request.received_message data member
# for input and return a dictionary for output. The client's accept and
# content-type headers determine the format of the messages. Similar to flask,
# routes can avoid pbjs response serialization by directly returning a
# flask.Response object.
@app.route('/teams', methods=['POST'])
@api(json, protobuf(receives=Person, sends=Team, errors=Error))
def create_team():
    leader = request.received_message

    if len(leader['name']) < 3:
        # Optionally, return a tuple of the form dict, status_code, headers
        # A 4xx HTTP error will use the 'errors' protobuf message type
        return {"errorMessage": "Name too short"}, 400

    # For a 200 response, just return a dict
    return {
        'id': get_url(2),
        'name': "{0}'s Team".format(leader['name']),
        'leader': get_url(person[id]),
        'members': [],
    }
```
*Create a team with JSON:*
```
curl -X POST -H "Accept: application/json" \
    -H "Content-type: application/json" \
    http://127.0.0.1:5000/teams --data {'id': 1, 'name': 'Red Leader'}
{
    "id": 2,
    "name": "Red Leader's Team",
    "leader": "/people/1"
    "members": []
}
```
*Create a new team with google protobuf:*
```python
# Create and save a Person structure in python
from example_messages_pb2 import Person
leader = Person()
leader.id = 1
leader.name = 'Red Leader'
with open('person.pb', 'wb') as f:
    f.write(leader.SerializeToString())
```
```
curl -X POST -H "Accept: application/x-protobuf" \
    -H "Content-type: application/x-protobuf" \
    http://127.0.0.1:5000/teams --data-binary @person.pb > team.pb
```

## Adding new mimetypes
Codecs are classes see JsonCodec and ProtobufCodec for examples

## The Protobuf Message escape hatch
If you want your decorated function to get the raw Protobuf Message class instance instead of the converted dict, set the keyword arg `to_dict` to `False` in the `protobuf` constructor.

This is sometimes handy since this library doesn't support all the functionality in the Protobuf spec. For example, `oneof` fields; the generated Protobuf Classes ensure that only one of the oneof fields are set but the data dictionaries this library normally exposes do not.

Warning: If `to_dict` is set to `False` and a JSON message is received it will *not* be converted to an instance of the corresponding Protobuf Message class (it'll still be passed to your function as a dictionary). Also please note that receiving and sending JSONs aren't checked/type-safe operations. JSON inputs can have extra fields/be missing fields and dictionary to JSON outputs aren't checked to ensure they've got all the right fields (Protobuf Message -> JSON is verified since in order to be a Protobuf Message instance, the message must be valid).

You can also _return_ a raw Protobuf Message instead of a data dictionary; if you do so, it will be converted to JSON if required or simply passed through. The output type is entirely independent from the `to_dict` attribute on the `protobuf` constructor; you can receive incoming messages as Protobuf Messages and return outgoing messages as data dicts or vice versa (or Protobuf in _and_ out, or, as you'd expect, data dictionary in and out). Just about the only thing you _can't_ do is receive JSON inputs as Protobuf Message class instances.
