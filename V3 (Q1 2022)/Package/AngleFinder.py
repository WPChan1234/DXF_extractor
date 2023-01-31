from ezdxf import math
import math as m
Barrier_vertices=(math.Vec2(836961.3903, 822327.538),math.Vec2(836964.055, 822326.678),math.Vec2(836962.6729, 822322.3955),math.Vec2(836965.2234, 822321.5724),math.Vec2(836964.2167, 822318.5611),math.Vec2(836966.4838, 822317.7611),math.Vec2(836966.8571, 822318.9829),math.Vec2(836969.6736, 822318.0399),math.Vec2(836969.8179, 822318.4872),math.Vec2(836972.1597, 822317.8313),math.Vec2(836970.7791, 822313.5536),math.Vec2(836973.0965, 822312.8057),math.Vec2(836974.3961, 822317.1096),math.Vec2(836976.6509, 822316.2821),math.Vec2(836976.5563, 822315.7609),math.Vec2(836979.4184, 822315.0894),math.Vec2(836978.9801, 822313.7966),math.Vec2(836981.4735, 822312.9919),math.Vec2(836980.7825, 822310.8506),math.Vec2(836982.3051, 822310.3592),math.Vec2(836981.6156, 822308.0599),math.Vec2(836983.0201, 822307.5278),math.Vec2(836983.4193, 822308.7647),math.Vec2(836985.3597, 822310.6288),math.Vec2(836983.7491, 822312.3055),math.Vec2(836985.6905, 822314.0664),math.Vec2(836984.9426, 822314.845),math.Vec2(836987.0351, 822316.925),math.Vec2(836986.7095, 822317.2639),math.Vec2(836988.3961, 822319.0159),math.Vec2(836991.4488, 822315.7154),math.Vec2(836992.5426, 822316.8285),math.Vec2(836996.4498, 822312.7612),math.Vec2(836995.3861, 822311.7393),math.Vec2(836998.4689, 822308.5301),math.Vec2(836996.7788, 822306.7818),math.Vec2(836996.4532, 822307.1208),math.Vec2(836992.3498, 822303.1789),math.Vec2(836992.5256, 822302.9526),math.Vec2(836990.8606, 822301.2215),math.Vec2(836987.7777, 822304.4305),math.Vec2(836986.7862, 822303.4781),math.Vec2(836985.6435, 822304.6677),math.Vec2(836985.1202, 822303.0462),math.Vec2(836983.8116, 822303.4685),math.Vec2(836982.3758, 822299.0195),math.Vec2(836980.1165, 822299.7647),math.Vec2(836980.3045, 822300.611),math.Vec2(836977.5055, 822301.5107),math.Vec2(836977.6591, 822301.9865),math.Vec2(836975.4227, 822302.7082),math.Vec2(836975.2, 822302.0183),math.Vec2(836972.4021, 822302.9212),math.Vec2(836972.2255, 822302.374),math.Vec2(836969.8844, 822303.1295),math.Vec2(836971.2972, 822307.5072),math.Vec2(836969.0608, 822308.229),math.Vec2(836967.625, 822303.7799),math.Vec2(836965.3069, 822304.6068),math.Vec2(836965.5406, 822305.5591),math.Vec2(836962.8093, 822306.4405),math.Vec2(836963.8075, 822309.5334),math.Vec2(836961.3332, 822310.332),math.Vec2(836962.0294, 822312.4894),math.Vec2(836957.0522, 822314.0957),math.Vec2(836961.3903, 822327.538))



NSRs=[math.Vec2(836968.8, 822319.4),math.Vec2(836969.3, 822305.9),math.Vec2(836971.3, 822319),math.Vec2(836984.0,822301.1),math.Vec2(836990.5, 822318.3)]

## Function to generate a 300m  view line with Source and End Pt input
def line_ext300m(SourcePT,EndPT):
    Sx,Sy=float(SourcePT[0]),float(SourcePT[1])

    Ex,Ey=float(EndPT[0]),float(EndPT[1])

    Dist_SE= ((Sx-Ex)**2+(Sy-Ey)**2)**0.5
    Ext_x,Ext_y=round(Sx-(300/Dist_SE)*(Sx-Ex),1),round(Sy-(300/Dist_SE)*(Sy-Ey),1)

    # print("Sx, Sy, Ex, Ey, Ext_x, Ext_y")
    # print(Sx,Sy,Ex,Ey,Ext_x,Ext_y)
    return [math.Vec2(Sx,Sy),math.Vec2(Ext_x,Ext_y)]

#Generate list of 3600 angles from -180 to 180 with 0.1 degree intervals
def Angle_list(n):
    List=[i for i in range(-1800, n + 1)]
    new_list=[x/ 10 for x in List]
    return new_list

# Change angle to Noisemap format (0 - 360 degree, North as 0 degree, clockwise)
def convert_angle_to_NoiseMap(Ang):
    Ang_noisemap= round(- Ang+90,1)
    if (Ang_noisemap<0):
        Ang_noisemap=Ang_noisemap+360
    else:
        Ang_noisemap = Ang_noisemap
    return(Ang_noisemap)

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
                    Ed_Left_Angle = n-0.5
                else:
                    St_Right_Angle=n+0.5

        Previous_state = With_intersect



    return(convert_angle_to_NoiseMap(St_Right_Angle ),convert_angle_to_NoiseMap(Ed_Left_Angle)) #output noisemap angle

# print(View_Finder(NSRs[0],Barrier_vertices))



def building_block_barrier(Tower,docPath):

    from tkinter import Tk
    import tkinter as tk
    import tkinter.messagebox
    from tkinter.filedialog import askopenfilename
    from tkinter.filedialog import asksaveasfile
    import ezdxf

    root = Tk()
    root.withdraw()
    tk.messagebox.showinfo('Select file & polyline containing layers for Tower - '+ Tower,message='Select file &  layers for Tower - ' + Tower)

    filedocPath = docPath

    doc = ezdxf.readfile(filedocPath)
    print(filedocPath)
    root.destroy()

    # iterate over all entities in modelspace
    msp = doc.modelspace()

    List_Output = ["layer,Xs,Ys,Zs,Xe,Ye,Ze"]
    CRTN_Output = ["Text", "Barrier File", ""]

    CRTN_Output =[]
    #
    # BarID = 9000
    Pline = msp.query('LWPOLYLINE')
    no_of_pline = len(Pline)
    print(no_of_pline)

    # All layers
    All_Layers = []
    for Layer in doc.layers:
        All_Layers.append(Layer.dxf.name)
    print(All_Layers)


    root = Tk()
    root.withdraw()

    app = tk.Tk()
    app.geometry("500x600")
    app.title('Select Polyline layer to be extracted for Tower - ' + Tower)

    # Tinker interface for layer selection
    Layer_for_extract = []

    def clicked():
        print("clicked")
        selected = box.curselection()  # returns a tuple
        for idx in selected:
            Layer_for_extract.append(box.get(idx))

    box = tk.Listbox(app, selectmode=tk.MULTIPLE, height=30)
    values = All_Layers
    for val in values:
        box.insert(tk.END, val)
    box.pack()

    button = tk.Button(app, text='Select layer to be extracted', width=50, command=clicked)
    button.pack()

    exit_button = tk.Button(app, text='Excute', width=50, command=app.destroy)
    exit_button.pack()
    root.destroy()

    app.mainloop()

    print(Layer_for_extract)

    # function for Line segment extraction
    def print_entity(e):
        layer = e.dxf.layer
        st = e.dxf.start
        end = e.dxf.end

        st_x = round(st[0], 1)
        st_y = round(st[1], 1)
        # st_z = str(round(st[2], 1))
        #
        # End_x = str(round(end[0], 1))
        # End_y = str(round(end[1], 1))
        # # End_z = str(round(end[2], 1))
        #
        # info = [BarID, layer, st, end]
        # List_Output.append(info)

        CRTN_Output.append(math.Vec2(st_x, st_y))
        # print(CRTN_Output)


    # Layer filtering and polyline explode

    for e in msp.query("LWPOLYLINE"):
        if e.dxf.layer in Layer_for_extract:
            # print(e)
            e.explode()
    for line in msp.query("LINE"):
        if line.dxf.layer in Layer_for_extract:
            # print(line)
            print_entity(line)

    print(CRTN_Output)

    return(CRTN_Output)
#
# building_block_barrier()


# 1    CRTN_Output.append("RETN     0.0")
#     print(CRTN_Output)

    # f = asksaveasfile(mode='w', defaultextension=".bar", title='Save Noisemap barrier file as', initialfile="Barrier")
    # for item in CRTN_Output:
    #     f.write("%s\n" % item)
    # f.close()
#
# Barrier=building_block_barrier('Test Tower')
# for n in range(len(NSRs)):
#     print(View_Finder(NSRs[n],Barrier))