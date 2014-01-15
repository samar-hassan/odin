# coding=utf-8
import datetime
from odin import serializers
from odin import resources

try:
    import simplejson as json
except ImportError:
    import json

JSON_TYPES = {
    datetime.date: serializers.date_iso_format,
    datetime.time: serializers.time_iso_format,
    datetime.datetime: serializers.datetime_iso_format,
}


class OdinEncoder(json.JSONEncoder):
    """
    Encoder for Odin resources.
    """
    def default(self, o):
        if isinstance(o, resources.Resource):
            obj = o.to_dict()
            obj[resources.RESOURCE_TYPE_FIELD] = o._meta.resource_name
            return obj
        elif o.__class__ in JSON_TYPES:
            return JSON_TYPES[o.__class__](o)
        else:
            return super(OdinEncoder, self)


def load(fp, resource=None):
    """
    Load a from a JSON encoded file.

    See :py:meth:`loads` for more details of the loading operation.

    :param fp: a file pointer to read JSON data from.
    :param resource: A resource instance or a resource name to use as the base for creating a resource.
    :returns: A resource object or object graph of resources loaded from file.
    """
    return loads(fp.read(), resource)


def loads(s, resource=None):
    """
    Load from a JSON encoded string.

    If a ``resource`` value is supplied it is used as the base resource for the supplied JSON. I one is not supplied a
    resource type field ``$`` is used to obtain the type represented by the dictionary. A ``ValidationError`` will be
    raised if either of these values are supplied and not compatible. It is valid for a type to be supplied in the file
    to be a child object from within the inheritance tree.

    :param s: String to load and parse.
    :param resource: A resource instance or a resource name to use as the base for creating a resource.
    :returns: A resource object or object graph of resources parsed from supplied string.
    """
    if isinstance(resource, type) and issubclass(resource, resources.Resource):
        resource_name = resource._meta.resource_name
    else:
        resource_name = resource
    return resources.build_object_graph(json.loads(s), resource_name)


def dump(resource, fp, cls=OdinEncoder, **kwargs):
    """
    Dump to a JSON encoded file.

    :param resource: The root resource to dump to a JSON encoded file.
    :param cls: Encoder to use serializing to a string; default is the :py:class:`OdinEncoder`.
    :param fp: The file pointer that represents the output file.
    """
    json.dump(resource, fp, cls=cls, **kwargs)


def dumps(resource, cls=OdinEncoder, **kwargs):
    """
    Dump to a JSON encoded string.

    :param resource: The root resource to dump to a JSON encoded file.
    :param cls: Encoder to use serializing to a string; default is the :py:class:`OdinEncoder`.
    :returns: JSON encoded string.
    """
    return json.dumps(resource, cls=cls, **kwargs)
