import ezdxf
from ezdxf import math




Barrier_vertices=(math.Vec2(836961.3903, 822327.538),math.Vec2(836964.055, 822326.678),math.Vec2(836962.6729, 822322.3955),math.Vec2(836965.2234, 822321.5724),math.Vec2(836964.2167, 822318.5611),math.Vec2(836966.4838, 822317.7611),math.Vec2(836966.8571, 822318.9829),math.Vec2(836969.6736, 822318.0399),math.Vec2(836969.8179, 822318.4872),math.Vec2(836972.1597, 822317.8313),math.Vec2(836970.7791, 822313.5536),math.Vec2(836973.0965, 822312.8057),math.Vec2(836974.3961, 822317.1096),math.Vec2(836976.6509, 822316.2821),math.Vec2(836976.5563, 822315.7609),math.Vec2(836979.4184, 822315.0894),math.Vec2(836978.9801, 822313.7966),math.Vec2(836981.4735, 822312.9919),math.Vec2(836980.7825, 822310.8506),math.Vec2(836982.3051, 822310.3592),math.Vec2(836981.6156, 822308.0599),math.Vec2(836983.0201, 822307.5278),math.Vec2(836983.4193, 822308.7647),math.Vec2(836985.3597, 822310.6288),math.Vec2(836983.7491, 822312.3055),math.Vec2(836985.6905, 822314.0664),math.Vec2(836984.9426, 822314.845),math.Vec2(836987.0351, 822316.925),math.Vec2(836986.7095, 822317.2639),math.Vec2(836988.3961, 822319.0159),math.Vec2(836991.4488, 822315.7154),math.Vec2(836992.5426, 822316.8285),math.Vec2(836996.4498, 822312.7612),math.Vec2(836995.3861, 822311.7393),math.Vec2(836998.4689, 822308.5301),math.Vec2(836996.7788, 822306.7818),math.Vec2(836996.4532, 822307.1208),math.Vec2(836992.3498, 822303.1789),math.Vec2(836992.5256, 822302.9526),math.Vec2(836990.8606, 822301.2215),math.Vec2(836987.7777, 822304.4305),math.Vec2(836986.7862, 822303.4781),math.Vec2(836985.6435, 822304.6677),math.Vec2(836985.1202, 822303.0462),math.Vec2(836983.8116, 822303.4685),math.Vec2(836982.3758, 822299.0195),math.Vec2(836980.1165, 822299.7647),math.Vec2(836980.3045, 822300.611),math.Vec2(836977.5055, 822301.5107),math.Vec2(836977.6591, 822301.9865),math.Vec2(836975.4227, 822302.7082),math.Vec2(836975.2, 822302.0183),math.Vec2(836972.4021, 822302.9212),math.Vec2(836972.2255, 822302.374),math.Vec2(836969.8844, 822303.1295),math.Vec2(836971.2972, 822307.5072),math.Vec2(836969.0608, 822308.229),math.Vec2(836967.625, 822303.7799),math.Vec2(836965.3069, 822304.6068),math.Vec2(836965.5406, 822305.5591),math.Vec2(836962.8093, 822306.4405),math.Vec2(836963.8075, 822309.5334),math.Vec2(836961.3332, 822310.332),math.Vec2(836962.0294, 822312.4894),math.Vec2(836957.0522, 822314.0957),math.Vec2(836961.3903, 822327.538))

NSRs=[math.Vec2(836971.22, 822319.2695),math.Vec2(836990.5708, 822318.5416),math.Vec2(836992.6384, 822301.4693),math.Vec2(836969.4598, 822305.8799)]

def line_ext300m(SourcePT,EndPT):
    Sx,Sy=float(SourcePT[0]),float(SourcePT[1])

    Ex,Ey=float(EndPT[0]),float(EndPT[1])

    Dist_SE= ((Sx-Ex)**2+(Sy-Ey)**2)**0.5
    Ext_x,Ext_y=round(Sx-(300/Dist_SE)*(Sx-Ex),1),round(Sy-(300/Dist_SE)*(Sy-Ey),1)

    # print("Sx, Sy, Ex, Ey, Ext_x, Ext_y")
    # print(Sx,Sy,Ex,Ey,Ext_x,Ext_y)
    return [math.Vec2(Sx,Sy),math.Vec2(Ext_x,Ext_y)]



print ("NSR, Barrier_vertice, No. of intersect, Line for visible angle")
for y in range(4):
    for x in range(65):

        intersection_pts = math.intersect_polylines_2d(Barrier_vertices,
                                                       (line_ext300m(NSRs[y],Barrier_vertices[x])),0.01)
        print("NSR"+str(y+1),", Barrier_vertices"+str(x+1),",",len(intersection_pts),",",len(intersection_pts)<=1)



