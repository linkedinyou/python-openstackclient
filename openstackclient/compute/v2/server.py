# Copyright 2012 OpenStack LLC.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from glanceclient.common import utils


def _find_server(cs, server):
    """Get a server by name or ID."""
    return utils.find_resource(cs.servers, server)

def _print_server(cs, server):
    # By default when searching via name we will do a
    # findall(name=blah) and due a REST /details which is not the same
    # as a .get() and doesn't get the information about flavors and
    # images. This fix it as we redo the call with the id which does a
    # .get() to get all informations.
    if not 'flavor' in server._info:
        server = _find_server(cs, server.id)

    networks = server.networks
    info = server._info.copy()
    for network_label, address_list in networks.items():
        info['%s network' % network_label] = ', '.join(address_list)

    flavor = info.get('flavor', {})
    flavor_id = flavor.get('id', '')
    info['flavor'] = _find_flavor(cs, flavor_id).name

    image = info.get('image', {})
    image_id = image.get('id', '')
    info['image'] = _find_image(cs, image_id).name

    info.pop('links', None)
    info.pop('addresses', None)

    utils.print_dict(info)

@utils.arg('server', metavar='<server>', help='Name or ID of server.')
def do_show_server(cs, args):
    """Show details about the given server."""
    print "do_show_server(%s)" % args.server
    #s = _find_server(cs, args.server)
    #_print_server(cs, s)