import smbus
import struct

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
        self._value
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
        return self.data[self.offset, self.offset+count]

    def _get(self, count):
        d = self._get_noincrement(count)
        offset += d
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
        return from_bytes(
            self._get(2),
            self.endianness,
            signed=False,
        )

    def int16(self):
        return from_bytes(
            self._get(2),
            self.endianness,
            signed=True,
        )

    def uint32(self):
        return from_bytes(
            self._get(4),
            self.endianness,
            signed=False,
        )

    def int32(self):
        return from_bytes(
            self._get(4),
            self.endianness,
            signed=True,
        )

class Response:
    @classmethod
    def deserialize(cls, data):
        raise NotImplementedError('Response.deserialize')

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
        self.serializer.put.byte(self.echo)
        return self.serialized.dump()

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

    ADDRESS = 0x04
    BUS_NUMBER = 0x01

    def __init__(
        self,
        bus_number=BUS_NUMBER,
        address=ADDRESS,
        response_deserializer=None,
    ):
        self.bus = smbus.SMBus(bus_number)
        self.address = address
        self.deserializer = response_deserializer

    def _write_byte(self, byte):
        self.bus.write_byte(self.address, byte)

    def _read_byte(self):
        self.bus.read_byte(self.address)

    def write(self, data):
        # TODO actually use a bulk write
        for b in data:
            self._write_byte(b)

    def send(self, request):
        self.write(request.serialized.value)

    def read(self):
        rb = self._read_byte

        data = []
        status = rb()

        if status != 0:
            raise self.InternalServerError()

        length = int.from_bytes(bytearray([rb(), rb()]))
        body = bytearray(rb() for _ in range(length))

        return body

    def read_response(self):
        return self.deserializer.deserialize(self.read())

    def echo(self, value):
        self.write(EchoRequest(value))
        return EchoResponse.parse(self.read_response())
