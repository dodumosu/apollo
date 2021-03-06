# -*- coding: utf-8 -*-
import networkx as nx
from sqlalchemy.orm.attributes import flag_modified

from apollo import services, utils
from apollo.core import db
from apollo.locations.models import LocationTypePath


def import_graph(graph, location_set, fresh_import=False):
    nodes = graph.get('nodes')
    edges = graph.get('edges')

    # convert any integral string IDs, because JavaScript
    for node in nodes:
        if not utils.validate_uuid(str(node.get('id'))):
            node['id'] = int(str(node.get('id')))
    for edge in edges:
        if not utils.validate_uuid(str(edge[0])):
            edge[0] = int(str(edge[0]))
        if not utils.validate_uuid(str(edge[1])):
            edge[1] = int(str(edge[1]))

    nx_graph = nx.DiGraph()

    for i, node in enumerate(nodes):
        # old implementation had ids as strings, current implementation
        # may be integers or integral strings
        if not utils.validate_uuid(str(node.get('id'))) and not fresh_import:
            # this is likely an existing division
            location_type = services.location_types.find(
                location_set=location_set,
                id=node.get('id')).first()

            if location_type:
                location_type.is_administrative = node.get(
                    'is_administrative')
                location_type.is_political = node.get('is_political')
                location_type.has_registered_voters = node.get(
                    'has_registered_voters')
                location_type.has_coordinates = node.get('has_coordinates')
                if node.get('nameTranslations'):
                    location_type.name_translations = node.get(
                        'nameTranslations')
                else:
                    location_type.name = node.get('name')

                # note: if only .name is changed, SQLA does not register
                # the object as being dirty or needing an update so we
                # force it to recognize the object as needing an update.
                flag_modified(location_type, 'name_translations')
                location_type.save()

            else:
                return

        else:
            location_type = services.location_types.create(
                is_administrative=node.get('is_administrative', False),
                is_political=node.get('is_political', False),
                has_registered_voters=node.get(
                    'has_registered_voters', False),
                location_set_id=location_set.id
            )
            if node.get('nameTranslations'):
                location_type.name_translations = node.get('nameTranslations')
            else:
                location_type.name = node.get('name')

            location_type.save()

        # update the edges
        for edge in edges:
            if edge[0] == node.get('id'):
                edge[0] = location_type.id
            if edge[1] == node.get('id'):
                edge[1] = location_type.id

    # build graph for the closure table
    nx_graph.add_edges_from(edges)
    sorted_nodes = list(nx.topological_sort(nx_graph))
    sorted_edges = list(nx_graph.edges(sorted_nodes))

    closure_graph = nx.DiGraph()
    closure_graph.add_edges_from(sorted_edges)

    # delete existing links
    LocationTypePath.query.filter_by(location_set=location_set).delete()
    db.session.commit()

    # build closure table
    path_lengths = dict(nx.all_pairs_shortest_path_length(closure_graph))

    for ancestor_id, paths in path_lengths.items():
        for descendant_id, depth in paths.items():
            path = LocationTypePath.query.filter_by(
                ancestor_id=ancestor_id,
                descendant_id=descendant_id,
                location_set_id=location_set.id
            ).first()

            # update the depth if we find an existing path
            if path:
                path.depth = depth
            else:
                path = LocationTypePath(
                    ancestor_id=ancestor_id, descendant_id=descendant_id,
                    depth=depth, location_set_id=location_set.id)

            db.session.add(path)
    db.session.commit()
