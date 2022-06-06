import ezdxf
from ezdxf import math
import math as m
import numbers


doc = ezdxf.new("R2000")
msp = doc.modelspace()

Barrier_vertices=(math.Vec2(836961.3903, 822327.538),math.Vec2(836964.055, 822326.678),math.Vec2(836962.6729, 822322.3955),math.Vec2(836965.2234, 822321.5724),math.Vec2(836964.2167, 822318.5611),math.Vec2(836966.4838, 822317.7611),math.Vec2(836966.8571, 822318.9829),math.Vec2(836969.6736, 822318.0399),math.Vec2(836969.8179, 822318.4872),math.Vec2(836972.1597, 822317.8313),math.Vec2(836970.7791, 822313.5536),math.Vec2(836973.0965, 822312.8057),math.Vec2(836974.3961, 822317.1096),math.Vec2(836976.6509, 822316.2821),math.Vec2(836976.5563, 822315.7609),math.Vec2(836979.4184, 822315.0894),math.Vec2(836978.9801, 822313.7966),math.Vec2(836981.4735, 822312.9919),math.Vec2(836980.7825, 822310.8506),math.Vec2(836982.3051, 822310.3592),math.Vec2(836981.6156, 822308.0599),math.Vec2(836983.0201, 822307.5278),math.Vec2(836983.4193, 822308.7647),math.Vec2(836985.3597, 822310.6288),math.Vec2(836983.7491, 822312.3055),math.Vec2(836985.6905, 822314.0664),math.Vec2(836984.9426, 822314.845),math.Vec2(836987.0351, 822316.925),math.Vec2(836986.7095, 822317.2639),math.Vec2(836988.3961, 822319.0159),math.Vec2(836991.4488, 822315.7154),math.Vec2(836992.5426, 822316.8285),math.Vec2(836996.4498, 822312.7612),math.Vec2(836995.3861, 822311.7393),math.Vec2(836998.4689, 822308.5301),math.Vec2(836996.7788, 822306.7818),math.Vec2(836996.4532, 822307.1208),math.Vec2(836992.3498, 822303.1789),math.Vec2(836992.5256, 822302.9526),math.Vec2(836990.8606, 822301.2215),math.Vec2(836987.7777, 822304.4305),math.Vec2(836986.7862, 822303.4781),math.Vec2(836985.6435, 822304.6677),math.Vec2(836985.1202, 822303.0462),math.Vec2(836983.8116, 822303.4685),math.Vec2(836982.3758, 822299.0195),math.Vec2(836980.1165, 822299.7647),math.Vec2(836980.3045, 822300.611),math.Vec2(836977.5055, 822301.5107),math.Vec2(836977.6591, 822301.9865),math.Vec2(836975.4227, 822302.7082),math.Vec2(836975.2, 822302.0183),math.Vec2(836972.4021, 822302.9212),math.Vec2(836972.2255, 822302.374),math.Vec2(836969.8844, 822303.1295),math.Vec2(836971.2972, 822307.5072),math.Vec2(836969.0608, 822308.229),math.Vec2(836967.625, 822303.7799),math.Vec2(836965.3069, 822304.6068),math.Vec2(836965.5406, 822305.5591),math.Vec2(836962.8093, 822306.4405),math.Vec2(836963.8075, 822309.5334),math.Vec2(836961.3332, 822310.332),math.Vec2(836962.0294, 822312.4894),math.Vec2(836957.0522, 822314.0957),math.Vec2(836961.3903, 822327.538))

NSRs=[math.Vec2(836971.22, 822319.2695),math.Vec2(836990.5708, 822318.5416),math.Vec2(836992.6384, 822301.4693),math.Vec2(836969.4598, 822305.8799),math.Vec2(836980.8, 822298.6)]

## Output view line from NSR to barrier vertices
def line_ext300m(SourcePT,EndPT):
    Sx,Sy=float(SourcePT[0]),float(SourcePT[1])

    Ex,Ey=float(EndPT[0]),float(EndPT[1])

    Dist_SE= ((Sx-Ex)**2+(Sy-Ey)**2)**0.5
    Ext_x,Ext_y=round(Sx-(300/Dist_SE)*(Sx-Ex),1),round(Sy-(300/Dist_SE)*(Sy-Ey),1)

    # print("Sx, Sy, Ex, Ey, Ext_x, Ext_y")
    # print(Sx,Sy,Ex,Ey,Ext_x,Ext_y)
    return [math.Vec2(Sx,Sy),math.Vec2(Ext_x,Ext_y)]

def Angle_list(n):
    List=[i for i in range(-1800, n + 1)]
    new_list=[x/ 10 for x in List]
    return new_list


#Function to detect blocakge of imaginary rays from receiver and check blockage, return min and max view angle without blockage
def View_Finder(NSR_Coor,Barrier_List):
    NSR_x, NSR_y = round(float(NSR_Coor[0]),1), round(float(NSR_Coor[1]),1)
    NSR_PT=math.Vec2(NSR_x, NSR_y)
    # Angle_per_45deg=[-180,-135,-90,-45,0,45,90,135,180]
    Angle_per_45deg =Angle_list(1800)
    View_List=[]
    Previous_state=[]

    for n in Angle_per_45deg:

        Unit_vector =math.Vec2(m.cos(m.radians(n)),m.sin(m.radians(n)))
        Ray_300m=line_ext300m(NSR_PT,NSR_PT+Unit_vector)
        With_intersect=len(math.intersect_polylines_2d(Ray_300m,Barrier_List,0.1))>0
        View_List.append([n,With_intersect])
        if With_intersect!=Previous_state and Previous_state != []:
                if With_intersect== False:
                    Start_Angle = n
                else:
                    End_Angle=n

        Previous_state = With_intersect
    print(View_List)

    return(Start_Angle,End_Angle)
    return(Angle_pair)

for n in range(len(NSRs)):
    print(View_Finder(NSRs[n],Barrier_vertices))




