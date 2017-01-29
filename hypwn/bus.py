import serial
import struct
from os import path

class Request:
    def serialize(self):
        raise NotImplementedError('Request.serialize')

class Put:
    ENDIANNESS = 'little'

    def __init__(self, serializer, endianness=ENDIANNESS):
        self._serializer = serializer
        self._endianness = endianness

    def byte(self, n):
        self._serializer._add_piece('byte', n.to_bytes(1, self._endianness))

    def short(self, n):
        self._serializer._add_piece('short', n.to_bytes(2, self._endianness))

    def int(self, n):
        self._serializer._add_piece('int', n.to_bytes(4, self._endianness))

    def float(self, n):
        self._serializer._add_piece(
            'float',
            bytearray(struct.pack('f', n)),
        )

    def double(self, n):
        self._serializer._add_piece(
            'double',
            bytearray(struct.pack('d', n)),
        )

class RequestSerializer:
    def __init__(self, device_id, action_code):
        self.device_id = device_id;
        self.action_code = action_code;
        self.pieces = []
        self._put = Put(self)

        self._put.byte(device_id)
        self._put.byte(action_code)

    def _add_piece(self, name, bytes):
        self.pieces.append( (name, bytes) )

    @property
    def put(self):
        return self._put

    def dump(self):
        print('dumped', self.pieces)
        return bytearray(b''.join(b for name, b in self.pieces))

class Cached:
    def __init__(self, f):
        self.f = f
        self._value = None
        self.computed = False

    @property
    def value(self):
        if self.computed:
            return self._value

        self._value = self.f()
        return self._value

class ResponseDeserializer:
    ENDIANNESS = 'little'

    def __init__(self, data, offset=0, endianness=ENDIANNESS):
        self.data = data
        self.offset = offset
        self.endianness = endianness

    def _get_noincrement(self, count):
        return self.data[self.offset:self.offset+count]

    def _get(self, count):
        d = self._get_noincrement(count)
        self.offset += count
        return d

    def split(self):
        return self.__class__(
            data,
            offset=self.offset,
            endianness=self.endianness,
        )

    def uint8(self):
        return int.from_bytes(
            self._get(1),
            self.endianness,
            signed=False,
        )

    def int8(self):
        return int.from_bytes(
            self._get(1),
            self.endianness,
            signed=True,
        )

    def uint16(self):
        return int.from_bytes(
            self._get(2),
            self.endianness,
            signed=False,
        )

    def int16(self):
        return int.from_bytes(
            self._get(2),
            self.endianness,
            signed=True,
        )

    def uint32(self):
        return int.from_bytes(
            self._get(4),
            self.endianness,
            signed=False,
        )

    def int32(self):
        return int.from_bytes(
            self._get(4),
            self.endianness,
            signed=True,
        )

    def float(self):
        return struct.pack(
            'f',
            self._get(4),
        )[0]

    def double(self):
        return struct.pack(
            'd',
            self._get(8),
        )[0]

class Response:
    @classmethod
    def deserialize(cls, data):
        raise NotImplementedError('Response.deserialize')

#PumpRelayStatus - uint8()

#PumpRelayRequest - short(1)

class NoArgsMixin:
    def _serialize(self):
        self._serializer.put.short(0)
        return self._serializer.dump()

class PumpRelayRequest(Request, NoArgsMixin):
    DEVICE_ID = 0
    ACTION_CODE = 0 #0 means information, 1 means setting on device

    def __init__(self, serializer=None):
        self._serializer = serializer or RequestSerializer(
            self.DEVICE_ID,
            self.ACTION_CODE,
        )
        self.serialized = Cached(self._serialize)

class PumpRelaySet(Request):
    DEVICE_ID = 0
    ACTION_CODE = 1 #0 means information, 1 means setting on device

    def __init__(self, setting=0, serializer=None):
        self._serializer = serializer or RequestSerializer(
            self.DEVICE_ID,
            self.ACTION_CODE,
        )
        self.setting = setting
        self.serialized = Cached(self._serialize)

    def _serialize(self):
        self._serializer.put.short(1) #arg len
        self._serializer.put.byte(self.setting)
        return self._serializer.dump()

class BooleanResponse:
    @classmethod
    def deserialize(cls, data):
        d = ResponseDeserializer(data)
        n = d.uint8()
        return cls(n)

    def __init__(self, ok):
        self.ok = ok

class DoubleResponse:
    @classmethod
    def deserialize(cls, data):
        d = ResponseDeserializer(data)
        n = d.double()
        return cls(n)

    def __init__(self, value):
        self.value = value

class PumpRelayResponse(BooleanResponse):
    pass

class LightRelaySet(Request):
    DEVICE_ID = 1
    ACTION_CODE = 1 #0 means information, 1 means setting on device

    def __init__(self, setting=0, serializer=None):
        self._serializer = serializer or RequestSerializer(
            self.DEVICE_ID,
            self.ACTION_CODE,
        )
        self.setting = setting
        self.serialized = Cached(self._serialize)

    def _serialize(self):
        self._serializer.put.short(1) #arg len
        self._serializer.put.byte(self.setting)
        return self._serializer.dump()

class LightRelayRequest(Request, NoArgsMixin):
    DEVICE_ID = 1
    ACTION_CODE = 0 #0 means information, 1 means setting on device

    def __init__(self, serializer=None):
        self._serializer = serializer or RequestSerializer(
            self.DEVICE_ID,
            self.ACTION_CODE,
        )
        self.serialized = Cached(self._serialize)

class LightRelayResponse(BooleanResponse):
    pass

class LightSensorRequest(Request, NoArgsMixin):
    DEVICE_ID = 2
    ACTION_CODE = 0

    def __init__(self, serializer=None):
        self._serializer = serializer or RequestSerializer(
            self.DEVICE_ID,
            self.ACTION_CODE,
        )
        self.serialized = Cached(self._serialize)

class LightSensorResponse(DoubleResponse):
    pass

class TempSensorRequest(Request, NoArgsMixin):
    DEVICE_ID = 4
    ACTION_CODE = 0

    def __init__(self, serializer=None):
        self._serializer = serializer or RequestSerializer(
            self.DEVICE_ID,
            self.ACTION_CODE,
        )
        self.serialized = Cached(self._serialize)

class TempSensorResponse(DoubleResponse):
    pass

class EchoRequest(Request):
    DEVICE_ID = 255
    ACTION_CODE = 0

    def __init__(self, echo=0xff, serializer=None):
        self._serializer = serializer or RequestSerializer(
            self.DEVICE_ID,
            self.ACTION_CODE,
        )
        self.serialized = Cached(self._serialize)
        self.echo = echo

    def _serialize(self):
        self._serializer.put.short(1) #arg len
        self._serializer.put.byte(self.echo)
        return self._serializer.dump()

class EchoResponse(Response):
    @classmethod
    def deserialize(cls, data):
        d = ResponseDeserializer(data)
        n = d.uint8()
        return cls(n)

    def __init__(self, echo):
        self.echo = echo

class Hype:
    class InternalServerError(Exception):
        pass

    TTY = [
        p
        for p
        in ('/dev/ttyUSB%d' % (n,) for n in (0,1,2,3,4))
        if path.exists(p)
    ][0]

    def __init__(
        self,
        tty=TTY,
    ):
        self.bus = serial.Serial(tty)

    def _write_byte(self, byte):
        self.bus.write(bytearray((byte,)))

    def _read_byte(self):
        b = self.bus.read(1)[0]
        print('>', b)
        return b

    def write(self, data):
        self.bus.write(data)

    def send(self, request):
        d = request.serialized.value
        print(d)
        self.write(d)

    def read(self):
        rb = self._read_byte

        data = []
        status = rb()

        if status != 0:
            print('got nonzero status', status)
            while True:
                rb()
            raise self.InternalServerError()

        length = int.from_bytes(
            bytearray([rb(), rb()]),
            'little',
        )
        body = bytearray(rb() for _ in range(length))

        print('read body', body, '- length', length)

        return body

    def echo(self, value):
        self.send(EchoRequest(value))
        return EchoResponse.deserialize(self.read())

    def set_light_level(self, state):
        self.send(LightRelaySet(state))
        return LightRelayResponse.deserialize(self.read())

    def get_light_level(self, location):
        if location == 'ambient':
            self.send(LightSensorRequest())
            return LightSensorResponse.deserialize(self.read())
        elif location == 'internal':
            self.send(LightRelayRequest())
            return LightRelayResponse.deserialize(self.read())
        else:
            raise Exception('Invalid location.')

    def get_temperature(self, location):
        self.send(TempSensorRequest())
        return TempSensorResponse.deserialize(self.read())

    def set_pump(self, state):
        self.send(PumpRelaySet(state))
        return PumpRelayResponse.deserialize(self.read())

    def get_pump(self):
        self.send(PumpRelayRequest())
        return PumpRelayResponse.deserialize(self.read())
