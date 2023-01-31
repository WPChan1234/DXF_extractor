from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfile
import ezdxf
import math
from ezdxf import math as emath
import tkinter.messagebox
import collections
from decimal import Decimal




doc = ezdxf.new()
msp = doc.modelspace()


def ViewAngleCalv2(Rec_Coor,Segment_St_Coor,Segment_Ed_Coor):

    def dotproduct(Line1, Line2):
        return sum((a * b) for a, b in zip(Line1, Line2))

    def length(v):
        return math.sqrt(dotproduct(v, v))

    def angle_between_lines(v1, v2):
        return round(math.degrees(math.acos(dotproduct(v1, v2) / (length(v1) * length(v2)))),1)



    Seg_Ed_Coor=emath.Vec2(Segment_Ed_Coor[0],Segment_Ed_Coor[1])
    Seg_St_Coor=emath.Vec2(Segment_St_Coor[0],Segment_St_Coor[1])
    Rec_Coor=emath.Vec2(Rec_Coor[0],Rec_Coor[1])

    # Seg_St_Coor=emath.Vec2(2450.7,2259.0)
    # Seg_Ed_Coor=emath.Vec2(4149.9,1666.4)
    # Rec_Coor=emath.Vec2(2919.5,2387.7)
    #
    # Seg_Ed_Coor=emath.Vec2(2450.7,2259.0)
    # Seg_St_Coor=emath.Vec2(4149.9,1666.4)
    # Rec_Coor=emath.Vec2(2919.5,2387.7)

    Segment = Seg_St_Coor - Seg_Ed_Coor


    Rec_st_line=Rec_Coor-Seg_St_Coor
    # print("Stline", round(Rec_st_line.angle_deg,1))
    Rec_Ed_line=Rec_Coor-Seg_Ed_Coor
    # print("EDline", round(Rec_Ed_line.angle_deg,1))


    View_angle=angle_between_lines(Rec_st_line,Rec_Ed_line)
    # print("ViewAngle",View_angle)
    # print("ST_Angle",angle_between_lines(Rec_st_line,Segment))
    # print("End_Angle",angle_between_lines(Rec_Ed_line,Segment))

    Angle_Segment_STLine=angle_between_lines(Rec_st_line,Segment)
    Angle_Segment_STLine=min(180-Angle_Segment_STLine,Angle_Segment_STLine)

    Angle_Segment_EdLine=angle_between_lines(Rec_Ed_line,Segment)
    Angle_Segment_EdLine=min(180-Angle_Segment_EdLine,Angle_Segment_EdLine)

    Alpha =round(min(Angle_Segment_STLine+View_angle/2,Angle_Segment_EdLine+View_angle/2),1)

    print(Alpha)
    return ({"Viewangle":View_angle,"Alpha":Alpha})

# # Horizontal
# print(ViewAngleCalv2([818575.2,833249.3],[818530.6,833192.75],[818618,833194.7]))
#
# print(ViewAngleCalv2([818577.7,833138.25],[818530.6,833192.75],[818618,833194.7]))
#
# # Vertical
# print(ViewAngleCalv2([818514.2,832944.3],[818561.4,832998.7],[818575.9,832912.6]))
# print(ViewAngleCalv2([818514.2,832944.3],[818575.9,832912.6],[818561.4,832998.7]))
#
# print(ViewAngleCalv2([818623.8,832962.7],[818561.4,832998.7],[818575.9,832912.6]))
# print(ViewAngleCalv2([818623.8,832962.7],[818575.9,832912.6],[818561.4,832998.7]))
#
# #horizontal >90
# print(ViewAngleCalv2([818780.4,833189.2],[818735.6,833163.9],[818823.0,833165.5]))
# print(ViewAngleCalv2([818780.4,833189.2],[818823.0,833165.5],[818735.6,833163.9]))
#
# #vertical>90
# print(ViewAngleCalv2([818776.1,833055.9],[818822.5,833070.6],[818763.6,833005.1]))
# print(ViewAngleCalv2([818812.2,833023.0],[818822.5,833070.6],[818763.6,833005.1]))