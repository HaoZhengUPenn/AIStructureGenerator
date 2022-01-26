import clr
clr.AddReferenceToFile("PolyFramework.dll")

import os
import PolyFramework as pf
import rhinoscriptsyntax as rs
from Rhino.Geometry import Vector3d


TOLERANCE = 0.001
PIPE_FACTOR = 0.00003
path = os.getcwd()+"\\"

def pfoam_equilibrium_matrix(pfoam, supports = []):
    """
    inputs:
        pfoam: PFoam object
        supports: list of Point3d
    returns the equilibrium matrix
    """
    internal_vertices = []
    unsupported_vertices = []
    for vertex in pfoam.Vertices:
        if vertex.External: continue
        internal_vertices.append(vertex)
        supported_flag = False
        for support in supports:
            support_pt = rs.coerce3dpoint(support)
            dist = vertex.Point.DistanceTo(support_pt)
            if dist < TOLERANCE:
                supported_flag = True
                break
        if not supported_flag: unsupported_vertices.append(vertex)
    
    internal_edges = []
    for edge in pfoam.Edges:
        if edge.Id < 0: continue
        if edge.External: continue
        internal_edges.append(edge)
        # MAY NEED TO: REMOVE THE EDGES IF BOTH ENDS ARE SUPPORTED
    matrix_path = path + "equilibrium_matrix.txt"
    file_matrix = open(matrix_path,"w")
    lines = []
    for vertex in unsupported_vertices:
        vertex_pt = vertex.Point
        line_x = []
        line_y = []
        line_z = []
        for edge in internal_edges:
            if vertex not in edge.Vertices:
                line_x.append(0)
                line_y.append(0)
                line_z.append(0)
            else:
                other_pt = get_other_vertex(vertex, edge).Point
                line_x.append(vertex_pt.X - other_pt.X)
                line_y.append(vertex_pt.Y - other_pt.Y)
                line_z.append(vertex_pt.Z - other_pt.Z)
        lines.append(",".join(map(str,line_x)))
        lines.append(",".join(map(str,line_y)))
        lines.append(",".join(map(str,line_z)))
    for line in lines:
        file_matrix.write(line+"\n")
    file_matrix.close()
    
    file_applied_load = open(path+"pellegrino_applied_load.txt", "w")
    lines_force = []
    for vertex in unsupported_vertices:
        total_force = Vector3d(0,0,0)
        for edge in vertex.Edges:
            if edge.Id <0: continue
            if not is_half_external_edge(edge): continue
            force = vertex.Point-get_other_vertex(vertex, edge).Point
            force.Unitize()
            #remove non-vertical forces
            if force*Vector3d(0,0,1)<0.99 and force*Vector3d(0,0,1)>-0.99: continue
            if force*Vector3d(0,0,1)>0.99 :continue
            total_force += force * edge.Dual.Area
#        lines_force.append(total_force.X)
#        lines_force.append(total_force.Y)
        lines_force.append(0)
        lines_force.append(0)
        lines_force.append(total_force.Z)
    for line in lines_force:
        file_applied_load.write(str(line)+"\n")
    file_applied_load.close()
    
    file_original_compressions = open(path+"pellegrino_original_compression.txt", "w")
    compressions = []
    for edge in internal_edges:
        length = edge.Vertices[0].Point.DistanceTo(edge.Vertices[1].Point)
        compressions.append(edge.Dual.Area/length)
    for line in compressions:
        file_original_compressions.write(str(line)+"\n")
    file_original_compressions.close()
    return unsupported_vertices, internal_edges

    
def get_other_vertex(vertex, edge):
    for v in edge.Vertices:
        if vertex == v: continue
        return v
        
def is_half_external_edge(edge):
    v0 = edge.Vertices[0].External
    v1 = edge.Vertices[1].External
    if v0 and v1: return False
    if (not v0) and (not v1): return False
    return True

def import_vector_from_text(path):
    result = []
    file = open(path,"r")
    lines = file.readlines()
    for line in lines:
        result.append(float(line.strip()))
    file.close()
    return result

objects, primal, dual, container_type = pf.LoadData.LoadPrimalDual(True)


for face in dual.Faces:
    face.ComputeArea()
#    print(face.Area)
#    print(face.Dual)

supports = rs.GetObjects("Select points", 1)
unsupported_vertices, internal_edges = pfoam_equilibrium_matrix(primal, supports)
rs.EnableRedraw(False)
os.system("python Pellegrino_Calculate_Rank.py")
modified_tensions = import_vector_from_text(path+"pellegrino_modified_tension.txt")
#print(len(modified_tensions))
#print(len(internal_edges))
tensile_layer = rs.AddLayer(name = "tensile elements", color = [200,50,50])
compressive_layer = rs.AddLayer(name = "compressive elements", color = [50,50,200])
group = rs.AddGroup()
for i in range(len(internal_edges)):
    edge = internal_edges[i]
    length = edge.Vertices[0].Point.DistanceTo(edge.Vertices[1].Point)
    force = length * modified_tensions[i]
    radius = abs(force)*PIPE_FACTOR
    line = rs.AddLine(edge.Vertices[0].Point,edge.Vertices[1].Point)
    pipe = rs.AddPipe(line, [0,1], [radius,radius],cap = 0)
    if force>0:
        rs.ObjectLayer(pipe, tensile_layer)
    else:
        rs.ObjectLayer(pipe, compressive_layer)
    rs.AddObjectToGroup(pipe, group)
    rs.DeleteObject(line)


