from scouterx.common.constants.packconstant.packconstants import OBJECT
from scouterx.common.netdata.mapvalue import MapValue
from scouterx.common.netdata.pack import Pack


class ObjectPack(Pack):
    def __init__(self):
        self.obj_type = ""
        self.obj_hash = 0
        self.obj_name = ""
        self.address = ""
        self.version = ""
        self.alive = True
        self.wakeup = 0
        self.tags = MapValue()

    def write(self, out):
        out.write_string(self.obj_type)
        out.write_decimal32(self.obj_hash)
        out.write_string(self.obj_name)
        out.write_string(self.address)
        out.write_string(self.version)
        out.write_boolean(self.alive)
        out.write_decimal(self.wakeup)
        out.write_value(self.tags)

    def read(self, inp):
        self.obj_type, err = inp.read_string()

        obj_hash, err = inp.read_decimal()
        self.obj_hash = int(obj_hash)

        self.obj_name, err = inp.read_string()
        self.address, err = inp.read_string()
        self.version, err = inp.read_string()
        self.alive, err = inp.read_boolean()
        self.wakeup, err = inp.read_decimal()

        value, err = inp.read_value()
        self.tags = value

    def __str__(self):
        return (f"object name: {self.obj_name} "
                f"type: {self.obj_type} "
                f"hash: {self.obj_hash} "
                f"version: {self.version} "
                f"alive: {str(self.alive)} "
                f"tags: {self.tags}")

    def set_status(self, status):
        self.tags.put("status", status)

    @classmethod
    def get_pack_type(cls):
        return OBJECT

    def to_string(self) -> str:
        return str(self)


class ObjectPack2(ObjectPack):
    def __init__(self):
        super().__init__()
        self.site_id = "Default"
        self.family = 0

    def write(self, out):
        try:
            out.write_string(self.site_id)
            out.write_string(self.obj_type)
            out.write_decimal32(self.obj_hash)
            out.write_string(self.obj_name)
            out.write_string(self.address)
            out.write_string(self.version)
            out.write_boolean(self.alive)
            out.write_decimal(self.wakeup)
            out.write_int8(self.family)
            out.write_value(self.tags)
            return None
        except Exception as e:
            return e

    def read(self, inp):
        try:
            self.site_id, err = inp.read_string()
            self.obj_type, err = inp.read_string()

            obj_hash, err = inp.read_decimal()
            self.obj_hash = int(obj_hash)

            self.obj_name, err = inp.read_string()
            self.address, err = inp.read_string()
            self.version, err = inp.read_string()
            self.alive, err = inp.read_boolean()
            self.wakeup, err = inp.read_decimal()
            self.family, err = inp.read_int8()
            value, err = inp.read_value()
            self.tags = value
            return self, None
        except Exception as e:
            return None, e

    def __str__(self):
        return (f"object siteID: {self.site_id} "
                f"name: {self.obj_name} "
                f"type: {self.obj_type} "
                f"hash: {self.obj_hash} "
                f"version: {self.version} "
                f"alive: {str(self.alive)} "
                f"family: {self.family} "
                f"tags: {self.tags}")
