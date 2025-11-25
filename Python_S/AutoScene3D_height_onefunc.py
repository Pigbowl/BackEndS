def process_map_data(json_input, output_path='3DModels/3D_environment_output.glb', show_preview=False):
    import json
    import numpy as np
    from pyglet.window.key import _5, Z
    from trimesh import Trimesh, Scene
    from trimesh.creation import box, cylinder
    from trimesh.primitives import Sphere, Box, Cylinder
    from trimesh.transformations import rotation_matrix
    from trimesh.path.creation import circle
    import os
    import trimesh
    import trimesh.util  # 确保导入util模块
    import pygltflib
    # 添加凸包计算所需的库
    from scipy.spatial import ConvexHull
    import random
# 解析JSON输入

    # 修改文件加载逻辑：让用户手动选择文件并验证格式
    map_data = None
    if isinstance(json_input, str):
        map_data = json.loads(json_input)
    elif isinstance(json_input, dict):
        map_data = json_input
    else:
        raise TypeError("json_input必须是字典或JSON字符串")
    
    # 检查DataType字段
    if isinstance(map_data, dict) and map_data.get('DataType') != 'MapData':
        raise ValueError("JSON数据中的DataType字段不是'MapData'")
    
    # 处理Physical_env结构
    if 'Physical_env' in map_data:
        map_data = map_data['Physical_env']

    # 创建场景\
    scene = Scene()
    road_meshes = []
    intersection_meshes = []
    singleline_meshes=[]
    # 统一声明3DLibrary文件夹路径
    LIBRARY_PATH = 'Python_S/ModelLibrary'



    # 处理Physical_env结构（保留原有的处理逻辑）
    if 'Physical_env' in map_data:
        map_data = map_data['Physical_env']

    # 材质定义
    materials = {
        'road': {'color': [0.5, 0.5, 0.5, 1.0]},  # 灰色道路
        'lane_mark': {'color': [1.0, 1.0, 1.0, 0.8]},  # 白色车道线（带透明度）
        'yellow_line': {'color': [1.0, 1.0, 0.0, 0.8]},  # 黄色车道线
        'stop_line': {'color': [1.0, 1.0, 1.0, 1.0]},  # 白色停止线
        'landmark': {'color': [1.0, 1.0, 0.0, 1.0]},  # 黄色地标箭头
        'pole': {'color': [0.33, 0.33, 0.33, 1.0]},  # 灰色灯杆
        'traffic_box': {'color': [0.2, 0.2, 0.2, 1.0]},  # 深灰色灯箱
        'green_light': {'color': [0.0, 1.0, 0.0, 1.0]},  # 绿色交通灯
        'yellow_light': {'color': [1.0, 1.0, 0.0, 1.0]},  # 黄色交通灯
        'red_light': {'color': [1.0, 0.0, 0.0, 1.0]}  # 红色交通灯
    }

    # 创建一个函数来确保路径使用正斜杠
    def get_unified_path(*parts):
        """创建统一使用正斜杠的路径"""
        # 使用os.path.join组合路径，然后替换所有反斜杠为正斜杠
        return os.path.join(*parts).replace('\\', '/')

    # 从RoadTem.glb加载ROAD对象
    def load_road_template():

        """从模板文件加载ROAD对象"""
        # 正确使用LIBRARY_PATH和get_unified_path函数
        template_path = get_unified_path(LIBRARY_PATH, 'RoadTem.glb')
        # print(f"加载路径: {template_path}")
        
        # 检查文件是否存在
        if not os.path.exists(template_path):
            print(f"警告: 找不到模板文件 {template_path}")
            # 如果找不到模板，创建一个默认的道路网格作为备选
            default_road = box(extents=[10, 2, 27])
            default_road.visual.face_colors = materials['road']['color']
            return default_road
        
        try:
            # 使用trimesh加载GLB文件
            template_scene = trimesh.load(template_path)
            
            # 查找名为ROAD的对象
            if isinstance(template_scene, trimesh.Scene):
                for name, mesh in template_scene.geometry.items():
                    if 'GROUND' in name.upper():
                        print(f"成功加载道路对象: {name}")
                        return mesh.copy()
                
                # 如果没有找到名为ROAD的对象，尝试使用第一个网格
                if template_scene.geometry:
                    first_mesh = next(iter(template_scene.geometry.values()))
                    print(f"未找到名为ROAD的对象，使用第一个网格作为备选")
                    return first_mesh.copy()
                else:
                    print("模板文件中没有找到任何网格")
                    return None
            elif isinstance(template_scene, trimesh.Trimesh):
                print("直接加载到了单个网格")
                return template_scene.copy()
            else:
                print("加载的对象既不是场景也不是网格")
                return None
        except Exception as e:
            print(f"加载模板文件时出错: {e}")
            # 创建默认道路网格作为备选
            default_road = box(extents=[10, 2, 27])
            default_road.visual.face_colors = materials['road']['color']
            return default_road


    # 从RoadTem.glb加载ROAD对象
    def load_plat_template():

        """从模板文件加载ROAD对象"""
        # 正确使用LIBRARY_PATH和get_unified_path函数
        template_path = get_unified_path(LIBRARY_PATH, 'RoadTem.glb')
        # print(f"加载路径: {template_path}")
        
        # 检查文件是否存在
        if not os.path.exists(template_path):
            print(f"警告: 找不到模板文件 {template_path}")
            # 如果找不到模板，创建一个默认的平台网格作为备选
            default_plat = box(extents=[10, 2, 27])
            default_plat.visual.face_colors = materials['road']['color']
            return default_plat
        
        try:
            # 使用trimesh加载GLB文件
            template_scene = trimesh.load(template_path)
            # 查找名为PLATFORM的对象
            if isinstance(template_scene, trimesh.Scene):
                for name, mesh in template_scene.geometry.items():
                    if 'LEAFS' in name.upper():
                        print(f"成功加载平台对象: {name}")
                        return mesh.copy()
                    
                # 如果没有找到名为PLATFORM的对象，尝试使用第一个网格
                if template_scene.geometry:
                    first_mesh = next(iter(template_scene.geometry.values()))
                    print(f"未找到名为PLATFORM的对象，使用第一个网格作为备选")      
                    return first_mesh.copy()
                else:
                    print("模板文件中没有找到任何网格")
                    return None
            elif isinstance(template_scene, trimesh.Trimesh):
                print("直接加载到了单个网格")
                return template_scene.copy()
            else:
                print("加载的对象既不是场景也不是网格")
                return None
        except Exception as e:
            print(f"加载模板文件时出错: {e}")
            # 创建默认道路网格作为备选
            default_plat = box(extents=[10, 2, 27])
            default_plat.visual.face_colors = materials['road']['color']
            return default_plat

    def load_light_pole_template():
        """从模板文件加载LightPole对象作为路灯模板"""
        template_path = get_unified_path(LIBRARY_PATH, 'LightTem.glb')

        # 检查文件是否存在
        if not os.path.exists(template_path):
            print(f"警告: 找不到模板文件 {template_path}")
            # 如果找不到模板，创建一个默认的路灯网格作为备选
            pole_mesh = cylinder(radius=0.15, height=10)
            pole_mesh.visual.face_colors = materials['pole']['color']
            return pole_mesh
        
        try:
            # 使用trimesh加载GLB文件
            template_scene = trimesh.load(template_path)
            
            # 查找名为LightPole的对象
            if isinstance(template_scene, trimesh.Scene):
                # 遍历场景中的所有几何对象
                for name, mesh in template_scene.geometry.items():
                    if 'LIGHTPOLE' in name.upper():
                        print(f"成功加载路灯杆对象: {name}")
                        return mesh.copy()
                
                # 如果没有找到名为LightPole的对象，尝试使用第一个网格
                if template_scene.geometry:
                    first_mesh = next(iter(template_scene.geometry.values()))
                    print(f"未找到名为LightPole的对象，使用第一个网格作为备选")
                    return first_mesh.copy()
                else:
                    print("模板文件中没有找到任何网格")
                    return None
            elif isinstance(template_scene, trimesh.Trimesh):
                print("直接加载到了单个网格")
                return template_scene.copy()
            else:
                print("加载的对象既不是场景也不是网格")
                return None
        except Exception as e:
            print(f"加载模板文件时出错: {e}")
            # 创建默认路灯网格作为备选
            pole_mesh = cylinder(radius=0.15, height=10)
            pole_mesh.visual.face_colors = materials['pole']['color']
            return pole_mesh
            

    # 从LightTem.glb加载LightBoy对象
    def load_light_template():
        """从模板文件加载LightPole对象作为路灯模板"""
        template_path = get_unified_path(LIBRARY_PATH, 'LightTem.glb')
        # 检查文件是否存在
        if not os.path.exists(template_path):
            print(f"警告: 找不到模板文件 {template_path}light")
            # 如果找不到模板，创建一个默认的灯箱网格作为备选
            default_light_box = box(extents=[1, 2, 0.5])
            default_light_box.visual.face_colors = materials['traffic_box']['color']
            return default_light_box
        
        try:
            # 使用trimesh加载GLB文件
            template_scene = trimesh.load(template_path)
            
            # 查找名为LightBoy的对象
            if isinstance(template_scene, trimesh.Scene):
                # 遍历场景中的所有几何对象
                for name, mesh in template_scene.geometry.items():
                    if 'LIGHTBODY' in name.upper():
                        print(f"成功加载灯箱对象: {name}")
                        return mesh.copy()
                
                # 如果没有找到名为LightBoy的对象，尝试使用第一个网格
                if template_scene.geometry:
                    first_mesh = next(iter(template_scene.geometry.values()))
                    print(f"未找到名为LightBoy的对象，使用第一个网格作为备选")
                    return first_mesh.copy()
                else:
                    print("模板文件中没有找到任何网格")
                    return None
            elif isinstance(template_scene, trimesh.Trimesh):
                print("直接加载到了单个网格")
                return template_scene.copy()
            else:
                print("加载的对象既不是场景也不是网格")
                return None
        except Exception as e:
            print(f"加载模板文件时出错: {e}")
            # 创建默认灯箱网格作为备选
            default_light_box = box(extents=[1, 2, 0.5])
            default_light_box.visual.face_colors = materials['traffic_box']['color']
            return default_light_box

    # 添加一个函数来加载LIGHTBOB模型作为灯泡模板
    def load_light_bulb_template():
        """从模板文件加载LIGHTBOB对象作为路灯灯泡模板"""
        template_path = get_unified_path(LIBRARY_PATH, 'LightTem.glb')
        
        # 检查文件是否存在
        if not os.path.exists(template_path):
            print(f"警告: 找不到模板文件 {template_path}")
            # 如果找不到模板，创建一个默认的灯泡网格作为备选
            bulb_mesh = Sphere(radius=0.3)
            bulb_mesh.visual.face_colors = [1.0, 1.0, 0.8, 1.0]  # 淡黄色灯泡
            return bulb_mesh
        
        try:
            # 使用trimesh加载GLB文件
            template_scene = trimesh.load(template_path)
            
            # 查找名为LIGHTBOB的对象（优先使用白色或黄色的灯泡）
            if isinstance(template_scene, trimesh.Scene):
                # 遍历场景中的所有几何对象
                for name, mesh in template_scene.geometry.items():
                    if 'LIGHTPOW' in name.upper():
                        print(f"成功加载路灯泡对象: {name}")
                        return mesh.copy()
                
                # 如果没有找到名为LIGHTBOB的对象，尝试使用第一个网格
                if template_scene.geometry:
                    first_mesh = next(iter(template_scene.geometry.values()))
                    print(f"未找到名为LIGHTBOB的对象，使用第一个网格作为备选")
                    return first_mesh.copy()
                else:
                    print("模板文件中没有找到任何网格")
                    return None
            elif isinstance(template_scene, trimesh.Trimesh):
                print("直接加载到了单个网格")
                return template_scene.copy()
            else:
                print("加载的对象既不是场景也不是网格")
                return None
        except Exception as e:
            print(f"加载模板文件时出错: {e}")
            # 创建默认灯泡网格作为备选
            bulb_mesh = Sphere(radius=0.3)
            bulb_mesh.visual.face_colors = [1.0, 1.0, 0.8, 1.0]  # 淡黄色灯泡
            return bulb_mesh
            
    # 从LightTem.glb加载三种颜色的交通灯对象
    def load_traffic_light_templates():
        """从模板文件加载三种颜色的交通灯对象"""
        template_path = get_unified_path(LIBRARY_PATH, 'LightTem.glb')
        light_templates = {
            'green': None,
            'yellow': None,
            'red': None
        }
        
        # 检查文件是否存在
        if not os.path.exists(template_path):
            print(f"警告: 找不到模板文件 {template_path}")
            return light_templates
        
        try:
            # 使用trimesh加载GLB文件
            template_scene = trimesh.load(template_path)
            
            # 查找三种颜色的交通灯对象
            if isinstance(template_scene, trimesh.Scene):
                # 遍历场景中的所有几何对象
                for name, mesh in template_scene.geometry.items():
                    if 'LIGHTBOB_GREEN' in name.upper():
                        print(f"成功加载绿色灯对象: {name}")
                        light_templates['green'] = mesh.copy()
                    elif 'LIGHTBOB_YELLOW' in name.upper():
                        print(f"成功加载黄色灯对象: {name}")
                        light_templates['yellow'] = mesh.copy()
                    elif 'LIGHTBOB_RED' in name.upper():
                        print(f"成功加载红色灯对象: {name}")
                        light_templates['red'] = mesh.copy()
            elif isinstance(template_scene, trimesh.Trimesh):
                print("直接加载到了单个网格，无法区分三种颜色的灯")
        except Exception as e:
            print(f"加载模板文件时出错: {e}")
            
        return light_templates

    # 从LINETemp.glb加载车道线模板
    def load_line_templates():
        """从模板文件加载WHITELINE和YELLOWLINE对象"""
        template_path = get_unified_path(LIBRARY_PATH, 'LINETem.glb')
        line_templates = {
            'white': None,
            'yellow': None
        }
        
        # 检查文件是否存在
        if not os.path.exists(template_path):
            print(f"警告: 找不到模板文件 {template_path}")
            return line_templates
        
        try:
            # 使用trimesh加载GLB文件
            template_scene = trimesh.load(template_path)
            
            # 查找两种颜色的车道线对象
            if isinstance(template_scene, trimesh.Scene):
                # 遍历场景中的所有几何对象
                for name, mesh in template_scene.geometry.items():
                    if 'WHITELINE' in name.upper():
                        print(f"成功加载白色车道线对象: {name}")
                        line_templates['white'] = mesh.copy()
                    elif 'YELLOWLINE' in name.upper():
                        print(f"成功加载黄色车道线对象: {name}")
                        line_templates['yellow'] = mesh.copy()
            elif isinstance(template_scene, trimesh.Trimesh):
                print("直接加载到了单个网格，无法区分白色和黄色车道线")
        except Exception as e:
            print(f"加载模板文件时出错: {e}")
            
        return line_templates

    # 从ZEBRA.glb加载斑马线模板
    def load_zebra_template():
        """从模板文件加载ZEBRA_WALK物体作为斑马线模板"""
        template_path = get_unified_path(LIBRARY_PATH, 'ZEBRA.glb')
        try:
            if os.path.exists(template_path):
                scene = trimesh.load(template_path)
                # 查找名为ZEBRA_WALK的物体
                for name, mesh in scene.geometry.items():
                    if 'ZEBRA_WALK' in name.upper():
                        print(f"成功加载斑马线模板: {name}")
                        return mesh.copy()
                # 如果没有找到指定名称的物体，输出警告并返回None
                print(f"警告: 在{template_path}中未找到ZEBRA_WALK物体")
                return None
            else:
                print(f"警告: 未找到斑马线模板文件: {template_path}")
                return None
        except Exception as e:
            print(f"加载斑马线模板时出错: {e}")
            return None

    # 从模板文件加载箭头对象作为LandMark
    def load_landmark_templates():
        """从模板文件加载箭头对象作为LandMark"""
        template_path = get_unified_path(LIBRARY_PATH, 'LightTem.glb')
        landmark_templates = {
            'straight': None,  # 对应type 1
            'left': None,      # 对应type 5
            'right': None      # 对应type 7
        }
        
        # 检查文件是否存在
        if not os.path.exists(template_path):
            print(f"警告: 找不到模板文件 {template_path}landmark")
            return landmark_templates

        try:
            # 使用trimesh加载GLB文件
            template_scene = trimesh.load(template_path)
            # 查找三种箭头对象
            if isinstance(template_scene, trimesh.Scene):
                # 遍历场景中的所有几何对象
                for name, mesh in template_scene.geometry.items():
                    if 'STRAIGHTARROW' in name.upper():
                        print(f"成功加载直箭头对象: {name}")
                        landmark_templates['straight'] = mesh.copy()
                    elif 'LEFTARROW' in name.upper():
                        print(f"成功加载左箭头对象: {name}")
                        landmark_templates['left'] = mesh.copy()
                    elif 'RIGHTARROW' in name.upper():
                        print(f"成功加载右箭头对象: {name}")
                        landmark_templates['right'] = mesh.copy()
            elif isinstance(template_scene, trimesh.Trimesh):
                print("直接加载到了单个网格，无法区分三种箭头")
        except Exception as e:
            print(f"加载模板文件时出错: {e}")
            
        return landmark_templates

    # 新增：加载建筑模板
    def load_building_template(Name):
        """从模板文件加载CORNERBUILDING对象"""
        template_path = get_unified_path(LIBRARY_PATH, 'BUILDTem.glb')
        
        # 检查文件是否存在
        if not os.path.exists(template_path):
            print(f"警告: 找不到模板文件 {template_path}")
            # 如果找不到模板，创建一个默认的建筑网格作为备选
            default_building = box(extents=[10, 15, 10])
            default_building.visual.face_colors = [0.7, 0.7, 0.7, 1.0]  # 灰色建筑
            return default_building
        
        try:
            # 使用trimesh加载GLB文件
            template_scene = trimesh.load(template_path)
            
            # 查找名为CORNERBUILDING的对象
            if isinstance(template_scene, trimesh.Scene):
                # 遍历场景中的所有几何对象
                for name, mesh in template_scene.geometry.items():
                    if Name in name.upper():
                        print(f"成功加载建筑物对象: {name}")
                        return mesh.copy()
                
                # 如果没有找到名为CORNERBUILDING的对象，尝试使用第一个网格
                if template_scene.geometry:
                    first_mesh = next(iter(template_scene.geometry.values()))
                    print(f"未找到名为的对象，使用第一个网格作为备选",Name)
                    return first_mesh.copy()
                else:
                    print("模板文件中没有找到任何网格")
                    return None
            elif isinstance(template_scene, trimesh.Trimesh):
                print("直接加载到了单个网格")
                return template_scene.copy()
            else:
                print("加载的对象既不是场景也不是网格")
                return None
        except Exception as e:
            print(f"加载模板文件时出错: {e}")
            # 创建默认建筑网格作为备选
            default_building = box(extents=[10, 15, 10])
            default_building.visual.face_colors = [0.7, 0.7, 0.7, 1.0]  # 灰色建筑
            return default_building

    # 线段相交检测函数
    def line_intersection(line1_start, line1_end, line2_start, line2_end):
        """检测两条线段是否相交，如果相交返回交点坐标，否则返回None"""
        # 提取x和z坐标（忽略y轴，假设道路都在同一平面上）
        x1, z1 = line1_start[0], line1_start[2]
        x2, z2 = line1_end[0], line1_end[2]
        x3, z3 = line2_start[0], line2_start[2]
        x4, z4 = line2_end[0], line2_end[2]
        
        # 计算分母
        denominator = (x1 - x2) * (z3 - z4) - (z1 - z2) * (x3 - x4)
        
        # 如果分母为0，线段平行或共线
        if denominator == 0:
            return None
        
        # 计算分子
        numerator_t = (x1 - x3) * (z3 - z4) - (z1 - z3) * (x3 - x4)
        numerator_u = -((x1 - x2) * (z1 - z3) - (z1 - z2) * (x1 - x3))
        
        # 计算参数t和u
        t = numerator_t / denominator
        u = numerator_u / denominator
        
        # 检查交点是否在线段范围内
        if 0 <= t <= 1 and 0 <= u <= 1:
            # 计算交点坐标
            intersection_x = x1 + t * (x2 - x1)
            intersection_z = z1 + t * (z2 - z1)
            # 返回3D交点（y轴设为0）
            return np.array([intersection_x, 0, intersection_z])
        
        return None


    # 从RoadTem.glb加载ROADEDGE对象
    def load_road_edge_template():
        """从模板文件加载ROADEDGE对象"""
        template_path = get_unified_path(LIBRARY_PATH, 'RoadTem.glb')
        
        # 检查文件是否存在
        if not os.path.exists(template_path):
            print(f"警告: 找不到模板文件 {template_path}")
            # 如果找不到模板，创建一个默认的路沿网格作为备选
            default_road_edge = box(extents=[10, 0.5, 6])
            default_road_edge.visual.face_colors = materials['lane_mark']['color']
            return default_road_edge
        
        try:
            # 使用trimesh加载GLB文件
            template_scene = trimesh.load(template_path)
            
            # 查找名为ROADEDGE的对象
            if isinstance(template_scene, trimesh.Scene):
                # 遍历场景中的所有几何对象
                for name, mesh in template_scene.geometry.items():
                    if 'ROADEDGE' in name.upper():
                        print(f"成功加载路沿对象: {name}")
                        return mesh.copy()
                
                # 如果没有找到名为ROADEDGE的对象，尝试使用第一个网格
                if template_scene.geometry:
                    first_mesh = next(iter(template_scene.geometry.values()))
                    print(f"未找到名为路沿的对象，使用第一个网格作为备选")
                    return first_mesh.copy()
                else:
                    print("模板文件中没有找到任何网格")
                    return None
            elif isinstance(template_scene, trimesh.Trimesh):
                print("直接加载到了单个网格")
                return template_scene.copy()
            else:
                print("加载的对象既不是场景也不是网格")
                return None
        except Exception as e:
            print(f"加载模板文件时出错: {e}")
            # 创建默认路沿网格作为备选
            default_road_edge = box(extents=[10, 0.5, 6])
            default_road_edge.visual.face_colors = materials['lane_mark']['color']
            return default_road_edge

    # 新增：查找相交道路及交点
    def find_intersecting_roads(roads):
        """找出所有相交的道路对及其交点"""
        intersecting_pairs = []
        
        # 遍历所有道路对（避免重复比较）
        for i in range(len(roads)):
            for j in range(i + 1, len(roads)):
                road1 = roads[i]
                road2 = roads[j]
                
                # 获取道路的起点和终点
                line1_start = road1['start_point']
                line1_end = road1['end_point']
                line2_start = road2['start_point']
                line2_end = road2['end_point']
                
                # 检测线段相交
                intersection_point = line_intersection(
                    line1_start, line1_end,
                    line2_start, line2_end
                )
                
                # 如果相交，记录道路对和交点
                if intersection_point is not None:
                    intersecting_pairs.append({
                        'road1_id': road1['roadID'],
                        'road2_id': road2['roadID'],
                        'intersection_point': intersection_point,
                        'road1_start': line1_start,
                        'road1_end': line1_end,
                        'road2_start': line2_start,
                        'road2_end': line2_end
                    })
                    
        return intersecting_pairs

    # 新增：计算两条直线之间的锐角夹角
    def calculate_angle_between_lines(line1_start, line1_end, line2_start, line2_end):
        """计算两条直线之间的锐角夹角，返回角度值（弧度）"""
        # 计算第一条线的方向向量
        vec1 = np.array([line1_end[0] - line1_start[0], line1_end[2] - line1_start[2]])
        # 计算第二条线的方向向量
        vec2 = np.array([line2_end[0] - line2_start[0], line2_end[2] - line2_start[2]])
        
        # 计算向量的模长
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0  # 如果任一直线长度为0，返回0度
        
        # 计算点积
        dot_product = np.dot(vec1, vec2)
        
        # 计算夹角的余弦值
        cos_angle = dot_product / (norm1 * norm2)
        
        # 确保余弦值在有效范围内
        cos_angle = max(-1.0, min(1.0, cos_angle))
        
        # 计算夹角（弧度）
        angle = np.arccos(cos_angle)
        
        # 确保返回锐角（小于等于90度，即π/2弧度）
        return min(angle, np.pi - angle)

    # 新增：计算在夹角中心线上距离交点指定距离的点的坐标
    def calculate_centerline_point(intersection_point, line1_start, line1_end, line2_start, line2_end, distance=30):
        """计算在两条直线夹角的中心线上，距离交点指定距离的点的坐标"""

        if intersection_point[0] == float(line1_start[0]) and intersection_point[2] == float(line1_start[2]):
            awaywpoint1 = line1_end
            originpoint1 = line1_start
        else:
            awaywpoint1 = line1_start
            originpoint1 = line1_end

        if intersection_point[0] == float(line2_start[0]) and intersection_point[2] == float(line2_start[2]):
            awaywpoint2 = line2_end
            originepoint2 = line2_start
        else:
            awaywpoint2 = line2_start
            originepoint2 = line2_end



        # if intersection_point == line1_start:

        # 计算两条直线的方向向量
        vec1 = np.array([awaywpoint1[0] - originpoint1[0], awaywpoint1[2] - originpoint1[2]])
        vec2 = np.array([awaywpoint2[0] - originepoint2[0], awaywpoint2[2] - originepoint2[2]])
        
        # 归一化方向向量
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        if norm1 == 0 or norm2 == 0:
            return intersection_point  # 如果任一直线长度为0，返回交点
        
        unit_vec1 = vec1 / norm1
        unit_vec2 = vec2 / norm2
        print()
        # 计算中心线方向向量（两条方向向量的单位向量之和）
        centerline_vec = unit_vec1 + unit_vec2
        centerline_norm = np.linalg.norm(centerline_vec)
        
        if centerline_norm == 0:
            return intersection_point  # 如果方向向量相反，返回交点
        
        # 归一化中心线方向向量
        unit_centerline = centerline_vec / centerline_norm
        
        # 计算距离交点指定距离的点
        # 这里创建两个可能的点，分别在两条直线形成的两个夹角中
        point1 = np.array([
            intersection_point[0] + unit_centerline[0] * distance,
            intersection_point[1],
            intersection_point[2] + unit_centerline[1] * distance
        ])
        
        # # 另一个方向（反向）
        # point2 = np.array([
        #     intersection_point[0] - unit_centerline[0] * distance,
        #     intersection_point[1],
        #     intersection_point[2] - unit_centerline[1] * distance
        # ])
        
        # 计算两条直线之间的锐角，确定返回哪个点
        angle = calculate_angle_between_lines(line1_start, line1_end, line2_start, line2_end)
        
        # 我们需要选择在锐角一侧的点
        # 计算两个点分别与两条直线的夹角
        # 由于我们已经计算了锐角，只需要检查哪个点更靠近锐角方向
        # 这里简化处理，选择在两条直线之间的点
        # 实际应用中可能需要更复杂的判断逻辑
        return point1  # 或者根据实际需求返回point2

    # 加载路沿模板
    road_edge_template = load_road_edge_template()
    # 加载道路模板
    road_template = load_road_template()

    platform_template = load_plat_template()
    # 加载灯箱模板
    light_template = load_light_template()
    # 加载交通灯模板
    light_templates = load_traffic_light_templates()
    # 加载地标模板
    landmark_templates = load_landmark_templates()
    # 加载车道线模板
    line_templates = load_line_templates()
    # 加载斑马线模板
    zebra_template = load_zebra_template()
    # 新增：加载路灯模板
    light_pole_template = load_light_pole_template()
    # 新增：加载灯泡模板
    light_bulb_template = load_light_bulb_template()
    # 新增：加载建筑模板
    building_template = load_building_template("CORNERBUILDING")
    building_template_2 = load_building_template("SECONDBUILDING")
    building_template_3 = load_building_template("LONGBUILDING")
    building_templates = [building_template,building_template_2]
    road_info = []

    def add_tiled_texture(mesh, unit_length, unit_width):
                                # 2. 计算模型在映射方向的尺寸（假设沿X轴为U，Z轴为V）
        x_min, x_max = mesh.vertices[:, 0].min(), mesh.vertices[:, 0].max()
        z_min, z_max = mesh.vertices[:, 2].min(), mesh.vertices[:, 2].max()
        model_length = x_max - x_min  # 模型长度（U方向）
        model_width = z_max - z_min   # 模型宽度（V方向）
        tiles_u = model_length / unit_length  # U方向需要的平铺次数
        tiles_v = model_width / unit_width  # V方向需要的平铺次数
        u = (mesh.vertices[:, 0] - x_min) / model_length * tiles_u
        v = (mesh.vertices[:, 2] - z_min) / model_width * tiles_v
        uv = np.column_stack([u, v])  # 形状为 (n_vertices, 2)
        # 3. 组合成UV坐标（每个顶点对应一个(u, v)）
        uv = np.column_stack([u, v])  # 形状为 (n_vertices, 2)
        return uv

    def add_tiled_texture_side(mesh, unit_length, unit_width):
            # 2. 计算模型在映射方向的尺寸（假设沿X轴为U，Z轴为V）
        x_min, x_max = mesh.vertices[:, 0].min(), mesh.vertices[:, 0].max()
        z_min, z_max = mesh.vertices[:, 1].min(), mesh.vertices[:, 1].max()
        model_length = x_max - x_min  # 模型长度（U方向）
        model_width = z_max - z_min   # 模型宽度（V方向）
        tiles_u = model_length / unit_length  # U方向需要的平铺次数
        tiles_v = model_width / unit_width  # V方向需要的平铺次数
        u = (mesh.vertices[:, 0] - x_min) / model_length * tiles_u
        v = (mesh.vertices[:, 1] - z_min) / model_width * tiles_v
        uv = np.column_stack([u, v])  # 形状为 (n_vertices, 2)
        # 3. 组合成UV坐标（每个顶点对应一个(u, v)）
        uv = np.column_stack([u, v])  # 形状为 (n_vertices, 2)
        return uv


    def drawroad(map_data):
        # 绘制道路
        if 'Road' in map_data:
            for road in map_data['Road']:
                # 从road数据中获取roadshape
                if 'roadshape' not in road:
                    print(f"警告: 道路ID {road['roadID']} 缺少roadshape数据，跳过绘制")
                    continue
                
                id = road['roadID']
                roadshape_left = road['leftboundshape']
                roadshape_right = road['rightboundshape']
                roadshape = road['roadshape']
                
                # 检查roadshape_left中是否包含xpoints和ypoints
                if 'xpoints' not in roadshape_left or 'ypoints' not in roadshape_left:
                    print(f"警告: 道路ID {id} 的roadshape数据不完整，跳过绘制")
                    continue
                
                xpoints_left = roadshape_left['xpoints']
                ypoints_left = roadshape_left['ypoints']
                zpoints_left = roadshape_left['zpoints']

                xpoints = roadshape['xpoints']
                ypoints = roadshape['ypoints']
                zpoints = roadshape['zpoints']

                # 检查roadshape_left中是否包含xpoints和ypoints
                if 'xpoints' not in roadshape_right or 'ypoints' not in roadshape_right:
                    print(f"警告: 道路ID {id} 的roadshape数据不完整，跳过绘制")
                    continue
                
                xpoints_right = roadshape_right['xpoints']
                ypoints_right = roadshape_right['ypoints']
                zpoints_right = roadshape_right['zpoints']
                
                # 确保xpoints和ypoints长度相同
                if len(xpoints_left) != len(ypoints_left):
                    print(f"警告: 道路ID {id} 的roadshape中xpoints和ypoints长度不一致，跳过绘制")
                    continue
                
                # 创建道路底部多边形（z=-1）
                bottom_points_left = []
                for i in range(len(xpoints_left)):
                    x = xpoints_left[i]
                    y = ypoints_left[i]  # 坐标系转换
                    z = zpoints_left[i]
                    bottom_points_left.append([x, z-1, y])

                # 创建道路底部多边形（z=-1）
                bottom_points_right = []
                for i in range(len(xpoints_right)):
                    x = xpoints_right[i]
                    y = ypoints_right[i]  # 坐标系转换
                    z = zpoints_right[i]
                    bottom_points_right.append([x, z-1, y])
                
                # 创建道路顶部多边形（z=1）
                top_points_left = []
                for i in range(len(xpoints_left)):
                    x = xpoints_left[i]
                    y = ypoints_left[i]  # 坐标系转换
                    z = zpoints_left[i]
                    top_points_left.append([x, z+0.1, y])
                
                # 创建道路顶部多边形（z=1）
                top_points_right = []
                for i in range(len(xpoints_right)):
                    x = xpoints_right[i]
                    y = ypoints_right[i]  # 坐标系转换
                    z = zpoints_right[i]
                    top_points_right.append([x, z+0.1, y])
                
                # 创建顶点数组
                vertices = []
                vertices.extend(bottom_points_left)
                vertices.extend(bottom_points_right)
                vertices.extend(top_points_left)
                vertices.extend(top_points_right)
                vertices_top_left=[]
                vertices_top_right=[]
                vertices_bottom_left=[]
                vertices_bottom_right=[]
                vertices_bottom_left.extend(bottom_points_left)
                vertices_bottom_right.extend(bottom_points_right)
                vertices_top_left.extend(top_points_left)
                vertices_top_right.extend(top_points_right)
                
                # 创建面数组（索引）
                faces = []
                n= len(xpoints_left)
                # n_right = len(xpoints_right)
                
                # 创建底面
                for i in range(n-1):

                    next_i = (i + 1) % n
                    faces.append([i, next_i,n+next_i,n+i])
                    i=i+2
                
                for i in range(n-1):
                    next_i = (i + 1) % n
                    faces.append([i+2*n, next_i+2*n,n+next_i+2*n,n+i+2*n])
                    i=i+2
                
                # 创建侧面
                for i in range(n-1):
                    next_i = (i + 1) % n
                    # 侧面四边形拆分为两个三角形
                    faces.append([i, next_i,next_i+2*n,i+2*n])
                    i=i+2

                # 创建侧面
                for i in range(n-1):
                    next_i = (i + 1) % n
                    # 侧面四边形拆分为两个三角形
                    faces.append([i+n, next_i+n,next_i+n+2*n,i+n+2*n])
                    i=i+2

                faces.append([0, n+1,3*n+1,2*n+1])
                road_mesh = road_template.copy()
                road_mesh.vertices = vertices
                road_mesh.faces = faces

                uv = add_tiled_texture(road_mesh, 4, 4)


                road_mesh.visual.uv = uv
                # 添加到道路网格列表
                scene.add_geometry(road_mesh,"road"+str(id))
                road_meshes.append(road_mesh)
                
                # 计算道路中心点用于后续元素放置
                center_x = sum(xpoints) / len(xpoints)
                center_y = -sum(ypoints) / len(ypoints)  # 坐标系转换
                
                # 计算道路起点和终点（使用第一个和最后一个点）
                start_x = xpoints[0]
                start_y = -ypoints[0]
                end_x = xpoints[-1]
                end_y = -ypoints[-1]
                
                road_info.append({
                    'roadID': id,
                    'start_point': np.array([start_x, 0, start_y]),
                    'end_point': np.array([end_x, 0, end_y]),
                    'mesh': road_mesh
                })



    drawroad(map_data)

    if 'StreetLights' in map_data:
        for streetlight in map_data['StreetLights']:
            pos_x = streetlight['posx']
            pos_y = streetlight['posy']
            pos_z = streetlight['posz']
            id = streetlight['ID']
            # pos_z = 0  # StreetLight模型的高度
            angle = np.radians(-streetlight['rotation'])
            textrotation = str(streetlight['rotation'])
            streetlight_mesh = light_pole_template.copy()
            
            streetlight_mesh.apply_transform(rotation_matrix(angle, [0, 1, 0]))
            streetlight_mesh.apply_scale([3, 3, 3])  # 根据需要调整缩放因子
            streetlight_mesh.apply_translation([pos_x, pos_z, pos_y])
            
            
            bulb_mesh = light_bulb_template.copy()
            bulb_mesh.apply_scale([3, 3, 3])
            bulb_mesh.apply_transform(rotation_matrix(angle, [0, 1, 0]))
            bulb_mesh.apply_translation([pos_x, pos_z, pos_y])
            

            scene.add_geometry(streetlight_mesh,"roadlightpole"+str(id))
            scene.add_geometry(bulb_mesh,"roadlightbulb"+str(id))
            

    buildingnumber = 0
    if 'Intersection' in map_data:
        for intersection in map_data['Intersection']:
            pos_x = intersection['posx']
            pos_y = intersection['posy']  # 坐标系转换
            
            # 使用模板创建路口几何体
            if road_template is not None:
                intersection_mesh = road_template.copy()
                
                # 计算缩放因子 - 路口通常是正方形，边长为27
                current_size = np.max([
                    intersection_mesh.bounds[1][0] - intersection_mesh.bounds[0][0],
                    intersection_mesh.bounds[1][2] - intersection_mesh.bounds[0][2]
                ])
                intersection_size = intersection['size']
                # 如果能计算出当前大小，则进行缩放
                if current_size > 0:
                    scale_factor = intersection_size / current_size  # 路口边长为27
                    intersection_mesh.apply_scale([scale_factor, 1, scale_factor])
                else:
                    print(f"警告: 无法计算模板网格的大小，使用默认大小")
            else:
                # 如果没有模板，回退到原来的创建方式
                print("警告: 没有可用的道路模板，创建默认路口")
                intersection_mesh = box(extents=[27, 2, 27])
                intersection_mesh.visual.face_colors = materials['road']['color']
            
            # 设置路口位置
            intersection_mesh.apply_translation([pos_x, -1, pos_y])
            uv = add_tiled_texture(intersection_mesh, 4, 4)
            intersection_mesh.visual.uv = uv
            
            # 添加到路口网格列表
            # intersection_meshes.append(intersection_mesh)
            scene.add_geometry(intersection_mesh)
            building_length = np.floor(building_template.bounds[1][0]-building_template.bounds[0][0])
            distance = (27/2+building_length/2+5)/np.sin(45*np.pi/180)
            for i in range(4):
                # A =building_templates[random]
                building_mesh = random.choice([building_template.copy(),building_template_2.copy()])
                angle = (45+i*90)*np.pi/180
                point1 = np.array([
                    pos_x + np.sin(angle) * distance,
                    0,
                    pos_y + np.cos(angle) * distance
                ])
                building_mesh.apply_translation([point1[0], 0, point1[2]])
                scene.add_geometry(building_mesh)
                # buildingnumber += 1
                # print(buildingnumber)
            

    # 合并所有道路和路口网格
    # all_road_intersection_meshes = road_meshes + intersection_meshes
    # if all_road_intersection_meshes:
    #     # 使用trimesh.util.concatenate函数代替Trimesh.concatenate方法
    #     merged_mesh = trimesh.util.concatenate(all_road_intersection_meshes)
    #     merged_mesh.visual = road_template.visual

    # uv = trimesh.visual.texture.generate_uvs(mesh)
    # # merged_mesh.visual.uv = uv
    # print("是否有UV坐标：", hasattr(merged_mesh.visual, 'uv'))
    # scene.add_geometry(merged_mesh)

    def draw_zebra_crossings(scene, zebra_crossings_data):
        """绘制斑马线
        参数:
        - scene: 3D场景对象
        - zebra_crossings_data: 从JSON加载的斑马线数据
        """
        if not zebra_crossings_data:
            print("未找到斑马线数据，跳过绘制")
            return
        
        # 白色，与xy平面平行，高度1.5
        white_color = [1.0, 1.0, 1.0, 1.0]  # RGBA白色
        height = 0.15  # 高度为1.5
        
        for crossing in zebra_crossings_data:
            crossing_id = crossing.get('ID', 'Unknown')
            print(f"绘制斑马线ID: {crossing_id}")
            
            # 获取geo数据
            geo_data = crossing.get('geo', [])
            if not geo_data:
                continue
            
            # 处理每个方框
            for box_idx, box_points in enumerate(geo_data):
                if len(box_points) < 4:
                    print(f"警告: 斑马线ID:{crossing_id}的第{box_idx}个方框点数量不足4个")
                    continue
                
                # 创建四边形面的顶点
                vertices = []
                for point in box_points:
                    x = point.get('x', 0)
                    y = point.get('y', 0)
                    # 构造3D坐标，z轴固定为height
                    vertices.append([x, height, y])  # 注意这里的坐标顺序[x, z, y]
                
                # 创建面索引 - 四边形由两个三角形组成
                faces = [
                    [0, 1, 2],  # 第一个三角形
                    [0, 2, 3]   # 第二个三角形
                ]
                
                # 创建网格
                try:
                    zebra_mesh = Trimesh(vertices=vertices, faces=faces)
                    zebra_mesh.visual.face_colors = white_color
                    
                    # 添加到场景
                    scene.add_geometry(zebra_mesh)
                except Exception as e:
                    print(f"创建斑马线ID:{crossing_id}的第{box_idx}个方框时出错: {e}")

    # 添加新的斑马线绘制调用
    zebra_crossings_data = map_data.get('ZebraCrossings', [])
    draw_zebra_crossings(scene, zebra_crossings_data)

    def draw_single_line(scene, points, line_type, color):
        """绘制单实线或单虚线"""
        if line_type == 'solid_single':
            # 实线：整个线段作为完整的一条线
            lane_mesh = create_lane_line_plane(points, 0.2, color)
            # lane_final_mesh = line_templates['white'].copy()
            # lane_final_mesh.vertices = lane_mesh.vertices
            # lane_final_mesh.faces = lane_mesh.faces
            scene.add_geometry(lane_mesh)

        elif line_type == 'left_curb' or line_type == 'right_curb':
            border_mesh = create_lane_line_tube(points, 2, color,1.5)
            border_mesh_top = border_mesh[0]
            
            border_final_mesh_top = road_edge_template.copy()
            border_final_mesh_top.vertices = border_mesh_top.vertices
            border_final_mesh_top.faces = border_mesh_top.faces
            uv_top = add_tiled_texture(border_final_mesh_top, 3, 3)
            border_final_mesh_top.visual.uv = uv_top

            border_mesh_side = border_mesh[1]
            border_final_mesh_side = road_edge_template.copy()
            border_final_mesh_side.vertices = border_mesh_side.vertices
            border_final_mesh_side.faces = border_mesh_side.faces
            uv_side = add_tiled_texture_side(border_final_mesh_side, 3, 3)
            border_final_mesh_side.visual.uv = uv_side

            scene.add_geometry(border_final_mesh_top)
            scene.add_geometry(border_final_mesh_side)

        elif line_type in ['dashed_single']:
            # 虚线：4m线段 + 4m间隔
            segment_length = 4.0  # 线段长度
            gap_length = 4.0      # 间隔长度
            
            # 计算整条路径的总长度和所有点的累积距离
            total_distance = 0.0
            cumulative_distances = [0.0]
            
            for i in range(len(points) - 1):
                start_point = np.array(points[i])
                end_point = np.array(points[i+1])
                segment_distance = np.linalg.norm(end_point - start_point)
                total_distance += segment_distance
                cumulative_distances.append(total_distance)

            # 沿整个路径创建虚线
            current_position = 0.0
            while current_position < total_distance:
                # 找到当前位置所在的线段
                segment_idx = 0
                for i in range(len(cumulative_distances) - 1):
                    if cumulative_distances[i] <= current_position < cumulative_distances[i+1]:
                        segment_idx = i
                        break
                
                # 计算当前线段的参数
                start_point = np.array(points[segment_idx])
                end_point = np.array(points[segment_idx+1])
                segment_vector = end_point - start_point
                segment_length_on_path = cumulative_distances[segment_idx+1] - cumulative_distances[segment_idx] #计算当前线段（两点之间）的长度
                
                # 如果线段太短，跳过
                if segment_length_on_path < 0.1:
                    current_position += segment_length + gap_length
                    continue
                
                # 计算单位方向向量
                direction = segment_vector / segment_length_on_path
                
                # 计算当前线段在路径中的相对位置
                relative_pos = current_position - cumulative_distances[segment_idx] 

                
                # 计算当前虚线线段的起点和终点
                seg_start = start_point + direction * relative_pos
                seg_end = start_point + direction * max(relative_pos + segment_length, segment_length_on_path)
                
                # 创建当前虚线线段
                seg_points = [seg_start, seg_end]
                lane_mesh = create_lane_line_plane(seg_points, 0.2, color)
                scene.add_geometry(lane_mesh)
                
                # 移动到下一个间隔的起点
                current_position += segment_length + gap_length

    def draw_double_line(scene, points, left_line_type, right_line_type, color):
        """绘制双实线或双虚线"""
        # 计算每条线的偏移量（距离中心线各10cm）
        line_width = 0.15
        offset_distance = 0.15  # 每条线距离中心线的距离
        
        # 确保points是数组
        points = np.array(points)
        
        # 提取xy坐标用于计算
        if points.shape[1] == 3:
            xy_points = np.column_stack((points[:, 0], points[:, 2]))
        else:
            xy_points = points
        

        # 计算中心线的法线方向
        left_points = []
        right_points = []
        
        for i in range(len(xy_points)):
            if i == 0:
                # 第一个点，使用第二个点减去第一个点的方向
                direction = xy_points[1] - xy_points[0]
            elif i == len(xy_points) - 1:
                # 最后一个点，使用最后一个点减去倒数第二个点的方向
                direction = xy_points[-1] - xy_points[-2]
            else:
                # 中间点，使用前后点的平均方向
                direction_prev = xy_points[i] - xy_points[i-1]
                direction_next = xy_points[i+1] - xy_points[i]
                direction = direction_prev + direction_next
                
            # 计算法线（垂直于方向）
            normal = np.array([-direction[1], direction[0]])
            # 归一化法线
            normal = normal / np.linalg.norm(normal) if np.linalg.norm(normal) > 0 else np.array([0, 1])
            
            # 计算左右两条线的点
            if points.shape[1] == 3:
                # 3D点，保留z坐标
                z_value = points[i, 1]
                left_point = np.array([xy_points[i, 0] - normal[0] * offset_distance, 
                                    z_value, 
                                    xy_points[i, 1] - normal[1] * offset_distance])
                right_point = np.array([xy_points[i, 0] + normal[0] * offset_distance, 
                                    z_value, 
                                    xy_points[i, 1] + normal[1] * offset_distance])
            else:
                # 2D点，z坐标设为0
                left_point = np.array([xy_points[i, 0] - normal[0] * offset_distance, 
                                    xy_points[i, 1] - normal[1] * offset_distance, 0])
                right_point = np.array([xy_points[i, 0] + normal[0] * offset_distance, 
                                    xy_points[i, 1] + normal[1] * offset_distance, 0])
            
            left_points.append(left_point)
            right_points.append(right_point)
        
        # 绘制左右两条线
        draw_single_line(scene, left_points, left_line_type, color)
        draw_single_line(scene, right_points, right_line_type, color)

    def create_lane_line_plane(points, width, color):
        """创建平滑的车道线平面（平行于地面）"""
        # 确保points是数组
        points = np.array(points)
        
        # 检查并处理点的维度
        if len(points.shape) == 1:
            points = points.reshape(-1, 2)
        
        # 处理3D点，注意坐标顺序：x(0), z(1), y(2)
        is_3d = False
        z_values = None
        if points.shape[1] == 3:
            is_3d = True
            # 提取x和y坐标用于计算（y在第2项）
            xy_points = np.column_stack((points[:, 0], points[:, 2]))
            # 保存z坐标（z在第1项）
            z_values = points[:, 1]
        else:
            xy_points = points
        
        # 计算每个点的法线方向（使用xy坐标）
        normals = []
        for i in range(len(xy_points)):
            if i == 0:
                # 第一个点，使用第二个点减去第一个点的方向
                direction = xy_points[1] - xy_points[0]
            elif i == len(xy_points) - 1:
                # 最后一个点，使用最后一个点减去倒数第二个点的方向
                direction = xy_points[-1] - xy_points[-2]
            else:
                # 中间点，使用前后点的平均方向
                direction_prev = xy_points[i] - xy_points[i-1]
                direction_next = xy_points[i+1] - xy_points[i]
                direction = direction_prev + direction_next
            
            # 计算法线（垂直于方向，在xy平面内）
            normal = np.array([-direction[1], direction[0]])
            # 归一化法线
            normal = normal / np.linalg.norm(normal) if np.linalg.norm(normal) > 0 else np.array([0, 1])
            normals.append(normal)
        
        # 创建网格顶点
        vertices = []
        for i, point in enumerate(xy_points):
            # 向法线两侧偏移创建宽度（仅在xy平面）
            left_offset_xy = point - normals[i] * (width / 2)
            right_offset_xy = point + normals[i] * (width / 2)
            
            # 根据点的维度，创建完整的顶点坐标
            if is_3d and z_values is not None:
                # 使用正确的坐标顺序：x, z, y
                left_offset = np.array([left_offset_xy[0], z_values[i], left_offset_xy[1]])
                right_offset = np.array([right_offset_xy[0], z_values[i], right_offset_xy[1]])
            else:
                # 2D点，z坐标设为0
                left_offset = np.array([left_offset_xy[0], 0, left_offset_xy[1]])
                right_offset = np.array([right_offset_xy[0], 0, right_offset_xy[1]])
            
            vertices.append(left_offset)
            vertices.append(right_offset)
        
        # 创建面索引
        faces = []
        for i in range(len(xy_points) - 1):
            # 每个线段对应的四边形面
            v1 = i * 2
            v2 = i * 2 + 1
            v3 = (i + 1) * 2 + 1
            v4 = (i + 1) * 2
            faces.append([v1, v2, v3])
            faces.append([v1, v3, v4])
        
        if color == [1.0, 1.0, 1.0, 0.8]:
            lane_mesh = line_templates['white'].copy()
        elif color == [1.0, 1.0, 0.0, 0.8]:
            lane_mesh = line_templates['yellow'].copy()

        lane_mesh.vertices = vertices
        lane_mesh.faces = faces
        uv = add_tiled_texture(lane_mesh, 1.0, 1.0)
        lane_mesh.visual.uv = uv
        # 创建网格
        # lane_mesh = Trimesh(vertices=vertices, faces=faces)
        
        # 设置颜色
        # lane_mesh.visual.face_colors = color
        
        return lane_mesh

    def create_lane_line_tube(points, width, color,height):
        """创建平滑的车道线平面（平行于地面）"""
        # 确保points是数组
        points = np.array(points)
        
        # 检查并处理点的维度
        if len(points.shape) == 1:
            points = points.reshape(-1, 2)
        
        # 处理3D点，注意坐标顺序：x(0), z(1), y(2)  
        is_3d = False
        z_values = None
        if points.shape[1] == 3:
            is_3d = True
            # 提取x和y坐标用于计算（y在第2项）
            xy_points = np.column_stack((points[:, 0], points[:, 2]))
            # 保存z坐标（z在第1项）
            z_values = points[:, 1]-0.4
        else:
            xy_points = points
        
        # 计算每个点的法线方向（使用xy坐标）
        normals = []
        for i in range(len(xy_points)):
            if i == 0:
                # 第一个点，使用第二个点减去第一个点的方向
                direction = xy_points[1] - xy_points[0]
            elif i == len(xy_points) - 1:
                # 最后一个点，使用最后一个点减去倒数第二个点的方向
                direction = xy_points[-1] - xy_points[-2]
            else:
                # 中间点，使用前后点的平均方向
                direction_prev = xy_points[i] - xy_points[i-1]
                direction_next = xy_points[i+1] - xy_points[i]
                direction = direction_prev + direction_next
            
            # 计算法线（垂直于方向，在xy平面内）
            normal = np.array([-direction[1], direction[0]])
            # 归一化法线
            normal = normal / np.linalg.norm(normal) if np.linalg.norm(normal) > 0 else np.array([0, 1])
            normals.append(normal)
        
        # 创建网格顶点
        vertices = []
        vertices_buttom= []
        vertices_top= []

        for i, point in enumerate(xy_points):
            # 向法线两侧偏移创建宽度（仅在xy平面）
            left_offset_xy = point - normals[i] * (width / 2)
            right_offset_xy = point + normals[i] * (width / 2)
            
            # 根据点的维度，创建完整的顶点坐标
            if is_3d and z_values is not None:
                # 使用正确的坐标顺序：x, z, y
                left_offset = np.array([left_offset_xy[0], z_values[i], left_offset_xy[1]])
                right_offset = np.array([right_offset_xy[0], z_values[i], right_offset_xy[1]])
                left_offset_top = np.array([left_offset_xy[0], z_values[i]+height, left_offset_xy[1]])
                right_offset_top = np.array([right_offset_xy[0], z_values[i]+height, right_offset_xy[1]])


            else:
                # 2D点，z坐标设为0
                left_offset = np.array([left_offset_xy[0], 0, left_offset_xy[1]])
                right_offset = np.array([right_offset_xy[0], 0, right_offset_xy[1]])
                left_offset_top = np.array([left_offset_xy[0], height, left_offset_xy[1]])
                right_offset_top = np.array([right_offset_xy[0], height, right_offset_xy[1]])
            
            vertices_buttom.append(left_offset)
            vertices_buttom.append(right_offset)
            vertices_top.append(left_offset_top)
            vertices_top.append(right_offset_top)
        # 创建面索引
        vertices = vertices_buttom + vertices_top

        faces = []
        for i in range(len(xy_points) - 1):
            # 每个线段对应的四边形面
            v1 = i * 2
            v2 = i * 2 + 1
            v3 = (i + 1) * 2
            v4 = (i + 1) * 2 + 1
            v5 = i * 2 + len(xy_points)*2
            v6 = i * 2 + 1 + len(xy_points)*2
            v7 = (i + 1) * 2 + len(xy_points)*2
            v8 = (i + 1) * 2 + 1 +len(xy_points)*2

            faces.append([v1, v2, v4])
            faces.append([v1, v4, v3])

            faces.append([v5, v6, v8])
            faces.append([v5, v8, v7])
            # faces.append([v1, v3, v5])
            # faces.append([v3, v7, v5])
            # faces.append([v2, v4, v6])
            # faces.append([v4, v8, v6])
        # 创建网格
        border_mesh_top = Trimesh(vertices=vertices, faces=faces)
        faces = []
        for i in range(len(xy_points) - 1):
            # 每个线段对应的四边形面
            v1 = i * 2
            v2 = i * 2 + 1
            v3 = (i + 1) * 2
            v4 = (i + 1) * 2 + 1
            v5 = i * 2 + len(xy_points)*2
            v6 = i * 2 + 1 + len(xy_points)*2
            v7 = (i + 1) * 2 + len(xy_points)*2
            v8 = (i + 1) * 2 + 1 +len(xy_points)*2
            faces.append([v1, v3, v5])
            faces.append([v3, v7, v5])
            faces.append([v2, v4, v6])
            faces.append([v4, v8, v6])

                # 创建网格
        border_mesh_side = Trimesh(vertices=vertices, faces=faces)
        

            
        return [border_mesh_top,border_mesh_side]

    if 'Road' in map_data:
        for road in map_data['Road']:
            # 从road数据中获取中心线起点和终点
            start_x = road['startx']
            start_y = road['starty']  # 坐标系转换
            end_x = road['endx']
            end_y = road['endy']  # 坐标系转换
            # 计算道路方向向量
            directionarray = np.array([end_x - start_x, 0, end_y - start_y])    
            if 'roadborder' in road:
                for border in road['roadborder']:
                    
                    # 获取点坐标
                    points = []
                    for i in range(len(border['xpoints'])):
                        x = border['xpoints'][i]
                        y = border['ypoints'][i]
                        z = border['zpoints'][i]
                        points.append([x, z+0.15, y])  # 坐标系转换到3D空间，设置适当的高度
                    
                    # # 确定线类型和颜色
                    line_type = border['type']
                    
                    # 解析颜色（从16进制字符串转换为RGBA）
                    color_hex = '#000000'  # 默认白色
                    color = [0.0, 0.0, 0.0, 0.8]  # 默认白色
                    
                    if color_hex.startswith('#'):
                        # 解析16进制颜色字符串
                        color_hex = color_hex.lstrip('#')
                        if len(color_hex) == 6:
                            r = int(color_hex[0:2], 16) / 255.0
                            g = int(color_hex[2:4], 16) / 255.0
                            b = int(color_hex[4:6], 16) / 255.0
                            color = [r, g, b, 0.8]
                    
                    draw_single_line(scene, points, line_type, color)


    if 'Road' in map_data:
        for road in map_data['Road']:
            # 从road数据中获取中心线起点和终点
            start_x = road['startx']
            start_y = road['starty']  # 坐标系转换
            end_x = road['endx']
            end_y = road['endy']  # 坐标系转换
            # 计算道路方向向量
            directionarray = np.array([end_x - start_x, 0, end_y - start_y])    
            if 'markers' in road:
                for marker in road['markers']:
                    
                    # 获取点坐标
                    points = []
                    for i in range(len(marker['xpoints'])):
                        x = marker['xpoints'][i]
                        y = marker['ypoints'][i]
                        z = marker['zpoints'][i]
                        points.append([x, z+0.15, y])  # 坐标系转换到3D空间，设置适当的高度
                    
                    # 确定线类型和颜色
                    line_type = marker['type']
                    
                    # 解析颜色（从16进制字符串转换为RGBA）
                    color_hex = marker.get('color', '#FFFFFF')  # 默认白色
                    color = [1.0, 1.0, 1.0, 0.8]  # 默认白色
                    
                    if color_hex.startswith('#'):
                        # 解析16进制颜色字符串
                        color_hex = color_hex.lstrip('#')
                        if len(color_hex) == 6:
                            r = int(color_hex[0:2], 16) / 255.0
                            g = int(color_hex[2:4], 16) / 255.0
                            b = int(color_hex[4:6], 16) / 255.0
                            color = [r, g, b, 0.8]
                    
                    # 处理不同类型的车道线
                    if line_type == 'solid_single' or line_type == 'dashed_single':
                        # 单线车道线 - 宽度为20cm
                        draw_single_line(scene, points, line_type, color)
                    elif line_type == 'solid_double':
                        # 双实线
                        draw_double_line(scene, points, 'solid_single', 'solid_single', color)
                    elif line_type == 'dashed_double':
                        # 双虚线
                        draw_double_line(scene, points, 'dashed_single', 'dashed_single', color)
                    elif line_type == 'solid_dashed':
                        # 左实右虚
                        draw_double_line(scene, points, 'solid_single', 'dashed_single', color)
                    elif line_type == 'dashed_solid':
                        # 左虚右实
                        draw_double_line(scene, points, 'dashed_single', 'solid_single', color)


    # 绘制停止线
    if 'Stopline' in map_data:
        for stop_line in map_data['Stopline']:
            # 创建线段几何体
            start_point = [stop_line['startx'], 0.15, stop_line['starty']]  # 坐标系转换
            end_point = [stop_line['endx'], 0.15, stop_line['endy']]  # 坐标系转换
            
            # 计算方向和长度
            direction = np.array(end_point) - np.array(start_point)
            length = np.linalg.norm(direction)
            if length > 0:
                direction = direction / length
            
            # 使用模板创建停止线几何体
            line_mesh = None
            if line_templates['white'] is not None:
                # 使用白色车道线模板
                line_mesh = line_templates['white'].copy()
                
                # 计算缩放因子以匹配线段长度
                current_length = line_mesh.bounds[1][0] - line_mesh.bounds[0][0]
                if current_length > 0:
                    scale_factor = length / current_length
                    line_mesh.apply_scale([scale_factor, 1, 1])
                
                # 计算旋转
                if direction[0] != 0 or direction[2] != 0:
                    angle = np.arctan2(direction[2], direction[0])
                    line_mesh.apply_transform(rotation_matrix(angle, [0, 1, 0]))
                
                # 计算位置
                center_point = start_point + direction * (length / 2)
                line_mesh.apply_translation(center_point)
            else:
                # 如果没有模板，回退到原来的创建方式
                line_mesh = box(extents=[length, 0.01, 0.2])
                line_mesh.visual.face_colors = materials['stop_line']['color']
                
                # 计算旋转
                if direction[0] != 0 or direction[2] != 0:
                    angle = np.arctan2(direction[2], direction[0])
                    line_mesh.apply_transform(rotation_matrix(angle, [0, 1, 0]))
                
                # 计算位置
                center_point = start_point + direction * (length / 2)
                line_mesh.apply_translation(center_point)
            
            # 添加到场景
            scene.add_geometry(line_mesh)


    # 计算点到线段的最短距离
    def point_to_line_distance(point, line_start, line_end):
        # 向量AB
        line_vec = line_end - line_start
        # 向量AP
        point_vec = point - line_start
        # 向量AB的长度平方
        line_len_sq = np.dot(line_vec, line_vec)
        
        # 计算投影参数t
        if line_len_sq == 0:
            # 线段退化为点
            return np.linalg.norm(point - line_start)
        
        # 计算投影参数t
        t = max(0, min(1, np.dot(point_vec, line_vec) / line_len_sq))
        # 计算投影点
        projection = line_start + t * line_vec
        # 计算点到投影点的距离
        return np.linalg.norm(point - projection)

    # 找到离给定点最近的道路
    def find_nearest_road(point, roads):
        if not roads:
            return None
        
        min_distance = float('inf')
        nearest_road = None
        
        for road in roads:
            distance = point_to_line_distance(point, road['start_point'], road['end_point'])
            if distance < min_distance:
                min_distance = distance
                nearest_road = road
        
        return nearest_road


    # 绘制交通灯
    if 'TrafficLights' in map_data:
        for traffic_light in map_data['TrafficLights']:
            pos_x = traffic_light['posx']
            pos_y = traffic_light['posy']  # 坐标系转换
            id = traffic_light['ID']

            angle = traffic_light['rotation']

            # 确定交通灯位置（使用z坐标表示y，因为在3D空间中y通常是高度）
            traffic_light_pos = np.array([pos_x, 0, pos_y])
            id = str(traffic_light['ID'])

            # 创建交通灯箱
            if light_template is not None:
                light_box_mesh = light_template.copy()
                lightscale= 5
                # 将灯箱尺寸放大5倍
                light_box_mesh.apply_scale([lightscale, lightscale, lightscale])
                
                # 恢复灯箱名称设置
                light_box_mesh.name = "trafficlight"
            else:
                # 如果没有模板，回退到原来的创建方式
                print("警告: 没有可用的灯箱模板，创建默认灯箱")
                light_box_mesh = box(extents=[1, 2, 0.5])
                light_box_mesh.visual.face_colors = materials['traffic_box']['color']
                
                # 恢复灯箱名称设置
                light_box_mesh.name = "trafficlight"
            
            # 应用灯箱的旋转和平移变换
            transform_matrix = np.eye(4)
            # 先应用旋转
            angle_rad = np.radians(angle-90)
            rot_matrix = rotation_matrix(angle_rad, [0, 1, 0])
            transform_matrix = rot_matrix @ transform_matrix
            # 然后应用平移
            if light_template is not None:
                trans_matrix = np.eye(4)
                trans_matrix[:3, 3] = [pos_x, 10, pos_y]
            else:
                trans_matrix = np.eye(4)
                trans_matrix[:3, 3] = [pos_x, 6, pos_y]
            transform_matrix = trans_matrix @ transform_matrix
            
            # 直接应用变换到灯箱网格
            light_box_mesh.apply_transform(transform_matrix)
            
            # 添加灯箱到主场景
            scene.add_geometry(light_box_mesh,"TLR"+id)

            
            # 使用模板创建交通灯，并作为独立对象添加
            lightscale = 5
            
            # 处理绿色交通灯
            if light_templates['green'] is not None:
                green_mesh = light_templates['green'].copy()
                green_mesh.apply_scale([lightscale, lightscale, lightscale])
                if hasattr(green_mesh.visual, 'material'):
                    green_mesh.visual.material = green_mesh.visual.material.copy()
                    green_mesh.visual.material.name = green_mesh.visual.material.name + id
            else:
                # 如果没有模板，回退到原来的创建方式
                green_mesh = Sphere(radius=0.3)
                green_mesh.visual.face_colors = materials['green_light']['color']
                
            # 应用相对于灯箱的位置变换
            green_transform = np.eye(4)
            green_transform[:3, 3] = [0, 0.9, 0]  # 相对于灯箱的垂直偏移
            
            # 先应用相对于灯箱的变换，再应用灯箱的全局变换
            combined_green_transform = transform_matrix @ green_transform
            
            # 直接应用组合变换到绿色灯
            green_mesh.apply_transform(combined_green_transform)
            
            # 设置绿色灯名称
            # green_mesh.name = "green_light"
            
            # 添加绿色灯到主场景
            scene.add_geometry(green_mesh,id+"_BULB_GREEN")

            
            # 处理黄色交通灯 (类似绿色灯的方式)
            if light_templates['yellow'] is not None:
                yellow_mesh = light_templates['yellow'].copy()
                yellow_mesh.apply_scale([lightscale, lightscale, lightscale])
                if hasattr(yellow_mesh.visual, 'material'):
                    yellow_mesh.visual.material = yellow_mesh.visual.material.copy()
                    yellow_mesh.visual.material.name = yellow_mesh.visual.material.name + id
            else:
                yellow_mesh = Sphere(radius=0.3)
                yellow_mesh.visual.face_colors = materials['yellow_light']['color']
            
            # 应用相对于灯箱的位置变换
            yellow_transform = np.eye(4)
            yellow_transform[:3, 3] = [0, -0.1, 0]  # 相对于灯箱的垂直偏移
            
            # 先应用相对于灯箱的变换，再应用灯箱的全局变换
            combined_yellow_transform = transform_matrix @ yellow_transform
            
            # 直接应用组合变换到黄色灯
            yellow_mesh.apply_transform(combined_yellow_transform)
            
            # 设置黄色灯名称
            yellow_mesh.name = "yellow_light"
            
            # 添加黄色灯到主场景
            scene.add_geometry(yellow_mesh,id+"_BULB_YELLOW")
            
            # 处理红色交通灯 (类似绿色灯的方式)
            if light_templates['red'] is not None:
                red_mesh = light_templates['red'].copy()
                red_mesh.apply_scale([lightscale, lightscale, lightscale])
                if hasattr(red_mesh.visual, 'material'):
                    red_mesh.visual.material = red_mesh.visual.material.copy()
                    red_mesh.visual.material.name = red_mesh.visual.material.name + id
            else:
                red_mesh = Sphere(radius=0.3)
                red_mesh.visual.face_colors = materials['red_light']['color']
            
            # 应用相对于灯箱的位置变换
            red_transform = np.eye(4)
            red_transform[:3, 3] = [0, -1.1, 0]  # 相对于灯箱的垂直偏移
            
            # 先应用相对于灯箱的变换，再应用灯箱的全局变换
            combined_red_transform = transform_matrix @ red_transform
            
            # 直接应用组合变换到红色灯
            red_mesh.apply_transform(combined_red_transform)
            
            # 设置红色灯名称
            red_mesh.name = "red_light"
            
            # 添加红色灯到主场景
            scene.add_geometry(red_mesh,id+"_BULB_RED")

            
        # 移除原来的子场景处理代码
        # 不需要再遍历几何体添加到主场景

    # 绘制LandMark
    if 'LandMarks' in map_data:
        for landmark in map_data['LandMarks']:
            pos_x = landmark['posx']
            pos_y = landmark['posy']  # 坐标系转换
            pos_z = landmark['posz']
            landmark_type = landmark['type']
            landmark_angle = landmark['angle']

            # 确定LandMark位置
            landmark_pos = np.array([pos_x, pos_z, pos_y])
            
            arrow_mesh = None
            landmark_scale = 10  # 放大倍数
            
            if landmark_type == "straight" and landmark_templates['straight'] is not None:
                # 直箭头
                arrow_mesh = landmark_templates['straight'].copy()
            elif landmark_type == "left" and landmark_templates['left'] is not None:
                # 左箭头
                arrow_mesh = landmark_templates['left'].copy()
            elif landmark_type == "right" and landmark_templates['right'] is not None:
                # 右箭头
                arrow_mesh = landmark_templates['right'].copy()
            
            if arrow_mesh is not None:
                # 放大模型
                arrow_mesh.apply_scale([landmark_scale, landmark_scale, landmark_scale])
                landmark_angle = np.radians(landmark_angle+90)
                landmark_row = np.radians(10)

                # 应用旋转，使其与道路方向一致
                arrow_mesh.apply_transform(rotation_matrix(landmark_angle, [0, -1, 0]))
                
                # 设置位置，稍微抬高一点避免与地面重合
                arrow_mesh.apply_translation([pos_x, pos_z+0.15, pos_y])
                
                # 添加到场景
                scene.add_geometry(arrow_mesh)
            else:
                # 如果没有对应类型的模板或模板加载失败，创建默认箭头
                print(f"警告: 没有可用的{landmark_type}类型箭头模板，创建默认箭头")
                # 默认使用一个简单的三角形来表示箭头
                # 这里简化处理，可以根据需要调整
                arrow_points = np.array([
                    [pos_x, 0.1, pos_y],
                    [pos_x + 0.5, 0.1, pos_y + 1],
                    [pos_x - 0.5, 0.1, pos_y + 1]
                ])
                # 创建三角形网格
                arrow_triangle = Trimesh(vertices=arrow_points, faces=[[0, 1, 2]])
                arrow_triangle.visual.face_colors = materials['landmark']['color']
                
                # 应用旋转
                arrow_triangle.apply_transform(rotation_matrix(landmark_orientation_angle, [0, 1, 0]))
                
                # 添加到场景
                scene.add_geometry(arrow_triangle)

    groundcenter_size_x = scene.bounds[1][0]-scene.bounds[0][0]
    groundcenter_size_y = scene.bounds[1][2]-scene.bounds[0][2]
    scale = max(groundcenter_size_x,groundcenter_size_y)/(platform_template.bounds[1][0]-platform_template.bounds[0][0])
    groundmesh = platform_template.copy()
    groundcenter_posx = (scene.bounds[1][0]+scene.bounds[0][0])/2
    groundcenter_posy = (scene.bounds[1][2]+scene.bounds[0][2])/2
    groundmesh.apply_scale([scale*1.1,1,scale*1.1])
    groundmesh.apply_translation([groundcenter_posx, -2, groundcenter_posy])
    uv = add_tiled_texture(groundmesh,20,20)
    groundmesh.visual.uv = uv
    print(uv)
    scene.add_geometry(groundmesh,"ground")

            # 显示3D预览（可选）
    if show_preview:
        try:
            print("正在显示3D模型...")
            scene.show()
        except Exception as e:
            print(f"可视化过程中出错: {e}")
    
    # 导出为GLB文件
    try:
        scene.export(
            output_path,
            file_type='glb',
            include_normals=True
        )
        print(f"地图已成功导出为: {output_path}")
        export_success = True
    except Exception as e:
        print(f"导出GLB文件时出错: {e}")
        # 如果上述参数失败，尝试不带额外参数导出
        try:
            scene.export(output_path, file_type='glb')
            print(f"使用基本参数成功导出GLB文件: {output_path}")
            export_success = True
        except Exception as e2:
            print(f"基本参数导出也失败: {e2}")
            export_success = False
    
    # 返回结果
    return {
        'success': True,
        'exported': export_success,
        'output_path': output_path,
        'scene_info': {
            'bounds': scene.bounds.tolist() if hasattr(scene, 'bounds') else None,
            'geometry_count': len(scene.geometry) if hasattr(scene, 'geometry') else 0
        }
    }
