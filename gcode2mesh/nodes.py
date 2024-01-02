import bpy

def add_3dprinting_modifier(active_object):
    try:
        geo_node_modifier = active_object.modifiers["3DPrinted"]
    except KeyError:
        geo_node_modifier = active_object.modifiers.new(name="3DPrinted", type='NODES')
    else:
        print("Modifier already added.")

    printed_node_group_name = "3DPrintedGeoNodes"
    try:
        node_tree = bpy.data.node_groups[printed_node_group_name]
    except KeyError:
        node_tree = bpy.data.node_groups.new(name=printed_node_group_name, type='GeometryNodeTree')
        add_nodes(node_tree)
    finally:
        geo_node_modifier.node_group = node_tree

def add_nodes(node_tree):
    group_input_node = node_tree.nodes.new(type='NodeGroupInput')
    node_tree.outputs.new('NodeSocketVector', 'Line Width')
    group_input_node.location = (-600, 0)
    
    combine_xyz_node = node_tree.nodes.new(type='ShaderNodeCombineXYZ')
    combine_xyz_node.inputs[0].default_value = 1
    combine_xyz_node.inputs[1].default_value = 1
    combine_xyz_node.location = (-300, -200)
    
    collection_info_node = node_tree.nodes.new(type='GeometryNodeCollectionInfo')
    collection_info_node.location = (-300, 0)

    resample_curve_node = node_tree.nodes.new(type='GeometryNodeResampleCurve')
    resample_curve_node.mode = "EVALUATED"
    resample_curve_node.location = (0, 0)
    
    curve_to_mesh_node = node_tree.nodes.new(type='GeometryNodeCurveToMesh')
    curve_to_mesh_node.location = (600, 0)
    
    mesh_circle_node = node_tree.nodes.new(type='GeometryNodeMeshCircle')
    mesh_circle_node.location = (0, -200)
    
    transform_geometry_node = node_tree.nodes.new(type='GeometryNodeTransform')
    transform_geometry_node.location = (300, -200)
    
    realize_instances_node = node_tree.nodes.new(type='GeometryNodeRealizeInstances')
    realize_instances_node.location = (900, 0)
    
    group_output_node = node_tree.nodes.new(type='NodeGroupOutput')
    group_output_node.location = (1200, 0)

    for node in node_tree.nodes:
        node.select = False

    links = node_tree.links
    links.new(group_input_node.outputs[0], combine_xyz_node.inputs[2])
    links.new(collection_info_node.outputs['Instances'], resample_curve_node.inputs['Curve'])
    links.new(resample_curve_node.outputs['Curve'], curve_to_mesh_node.inputs['Curve'])
    links.new(mesh_circle_node.outputs['Mesh'], transform_geometry_node.inputs['Geometry'])
    links.new(transform_geometry_node.outputs['Geometry'], curve_to_mesh_node.inputs['Profile Curve'])


if __name__ == '__main__':
    if bpy.context.selected_objects:
        active_object = bpy.context.active_object
        add_3dprinting_modifier(active_object)
    else:
        print("No object selected. Please select an object.")
