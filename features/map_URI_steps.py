from lettuce import step
from lettuce import world
from http_server import map_URI, NotFoundError


@step('a URI (.+)')
def a_URI(step, resource):
    world.resource = resource


@step('I call the function')
def call_map_URI(step):
    try:
        world.map = map_URI(world.resource)
    except NotFoundError:
        world.map = "404 Exception"


@step('I have (.+)')
def compare(step, expected):
    assert world.map == expected, "Got %s" % world.map
