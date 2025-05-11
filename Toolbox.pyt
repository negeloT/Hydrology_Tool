import arcpy
from arcpy.sa import *


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Hydrology"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [Hydrology]


class Hydrology(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Hydrology"
        self.description = "Description"
        self.canRunInBackground = True

    def getParameterInfo(self):
        """Define parameter definitions"""

        in_dem = arcpy.Parameter( #Тут мы принимаем ЦМР
            displayName="Input projected DEM",
            name="in_features",
            datatype="GPRasterLayer",
            parameterType="Required",
            direction="Input")

        out_dem = arcpy.Parameter( #Выбор места сохранения гидрологически-корректной ЦМР
            displayName="Output hydrologically correct DEM",
            name="out_features",
            datatype="GPRasterLayer",
            parameterType="Optional",
            direction="Output")
        out_dem.category = "0.Fill DEM"

        out_flow_dir = arcpy.Parameter( #Выбор места сохранения растра направления стока
            displayName="Output Flow Direction",
            name="out_flow_dir",
            datatype="GPRasterLayer",
            parameterType="Optional",
            direction="Output")
        out_flow_dir.category = "1.Flow Direction"

        out_flow_accum = arcpy.Parameter( #Выбор места сохранения растра аккумуляции стока
            displayName="Output Flow Accumulation",
            name="out_flow_accum",
            datatype="GPRasterLayer",
            parameterType="Optional",
            direction="Output")
        out_flow_accum.category = "2.Flow Accumulation"

        out_stream_network = arcpy.Parameter( #Выбор места сохранения растра сети водотоков
            displayName="Output Stream Network Raster",
            name="out_stream_network",
            datatype="DERasterDataset",
            parameterType="Optional",
            direction="Output")
        out_stream_network.category = "3.Stream Group"

        in_threshold_stream_network = arcpy.Parameter( #Тут мы задаем порог для выделения водотоков
            displayName="Threshold For Stream Network Raster",
            name="in_threshold_stream_network",
            datatype="GPLong",
            parameterType="Optional",
            direction="Input")
        in_threshold_stream_network.value = 2000
        in_threshold_stream_network.category = "3.Stream Group"

        out_stream_order = arcpy.Parameter( #Тут мы сохраняем сеть водотоков в виде растра
            displayName="Output Stream Order Raster",
            name="out_stream_order",
            datatype="GPRasterLayer",
            parameterType="Optional",
            direction="Output")
        out_stream_order.category = "3.Stream Group"

        out_stream_feature = arcpy.Parameter( #Выбор места сохранения водотоков в виде вектора (линии)
            displayName="Output Stream Feature",
            name="out_stream_feature",
            datatype="DEFeatureClass",
            parameterType="Optional",
            direction="Output")
        out_stream_feature.category = "3.Stream Group"

        out_basin_raster = arcpy.Parameter( #Тут мы сохраняем растр бассейнов
            displayName="Output Basin Raster",
            name="out_basin_raster",
            datatype="GPRasterLayer",
            parameterType="Optional",
            direction="Output")
        out_basin_raster.category = "4.Basin Group"

        out_basin_feature = arcpy.Parameter( #Выбор места сохранения бассейнов в виде векторов (полигоны)
            displayName="Output Basin Feature",
            name="out_basin_feature",
            datatype="DEFeatureClass",
            parameterType="Optional",
            direction="Output")
        out_basin_feature.category = "4.Basin Group"

        in_force_flow = arcpy.Parameter(
            displayName="Select Force Flow Direction",
            name="in_force_flow",
            datatype="GPString",
            parameterType="Optional",
            direction="Input")
        in_force_flow.filter.type = "ValueList"
        in_force_flow.filter.list = ["NORMAL", "FORCE"]
        in_force_flow.value = "NORMAL"
        in_force_flow.category = "1.Flow Direction"

        in_flow_direction_type = arcpy.Parameter(
            displayName="Select Flow Direction Type",
            name="in_flow_direction_type",
            datatype="GPString",
            parameterType="Optional",
            direction="Input")
        in_flow_direction_type.filter.type = "ValueList"
        in_flow_direction_type.filter.list = ["D8", "MFD", "DINF"]
        in_flow_direction_type.value = "D8"
        in_flow_direction_type.category = "1.Flow Direction"

        in_flow_accum_data_type = arcpy.Parameter(
            displayName="Select Flow Accumulation Data Type",
            name="in_flow_accum_data_type",
            datatype="GPString",
            parameterType="Optional",
            direction="Input")
        in_flow_accum_data_type.filter.type = "ValueList"
        in_flow_accum_data_type.filter.list = ["FLOAT", "INTEGER", "DOUBLE"]
        in_flow_accum_data_type.value = "FLOAT"
        in_flow_accum_data_type.category = "2.Flow Accumulation"

        in_flow_accum_direction_type = arcpy.Parameter(
            displayName="Select Flow Direction Type",
            name="flow_accum_direction_type",
            datatype="GPString",
            parameterType="Optional",
            direction="Input")
        in_flow_accum_direction_type.filter.type = "ValueList"
        in_flow_accum_direction_type.filter.list = ["D8", "MFD", "DINF"]
        in_flow_accum_direction_type.value = "D8"
        in_flow_accum_direction_type.category = "2.Flow Accumulation"

        in_stream_order_method = arcpy.Parameter(
            displayName="Select Stream Order Method",
            name="in_stream_order_method",
            datatype="GPString",
            parameterType="Optional",
            direction="Input")
        in_stream_order_method.filter.type = "ValueList"
        in_stream_order_method.filter.list = ["STRAHLER", "SHREVE"]
        in_stream_order_method.value = "STRAHLER"
        in_stream_order_method.category = "3.Stream Group"

        in_stream_feature_simplify = arcpy.Parameter(
            displayName="Select Simplify Method For Stream To Feature",
            name="in_stream_feature_simplify",
            datatype="GPString",
            parameterType="Optional",
            direction="Input")
        in_stream_feature_simplify.filter.type = "ValueList"
        in_stream_feature_simplify.filter.list = ["SIMPLIFY", "NO_SIMPLIFY"]
        in_stream_feature_simplify.value = "NO_SIMPLIFY"
        in_stream_feature_simplify.category = "3.Stream Group"

        in_basin_feature_simplify = arcpy.Parameter(
            displayName="Select Simplify Method For Basin To Feature",
            name="in_basin_feature_simplify",
            datatype="GPString",
            parameterType="Optional",
            direction="Input")
        in_basin_feature_simplify.filter.type = "ValueList"
        in_basin_feature_simplify.filter.list = ["SIMPLIFY", "NO_SIMPLIFY"]
        in_basin_feature_simplify.value = "NO_SIMPLIFY"
        in_basin_feature_simplify.category = "4.Basin Group"

        in_fill_method = arcpy.Parameter(
            displayName="Select Fill Method",
            name="in_fill_method",
            datatype="GPString",
            parameterType="Optional",
            direction="Input")
        in_fill_method.filter.type = "ValueList"
        in_fill_method.filter.list = ["PRATIK MUCHKARNI", "VLADIMIR S. DEKHNICH"]
        in_fill_method.value = "PRATIK MUCHKARNI"
        in_fill_method.category = "0.Fill DEM"

        in_area_of_lakes = arcpy.Parameter( #Тут мы задаем порог для выделения озер
            displayName="Minimum area of lakes only for 'VLADIMIR S. DEKHNICH' method in square kilometers",
            name="in_area_of_lakes",
            datatype="GPDouble",
            parameterType="Optional",
            direction="Input")
        in_area_of_lakes.value = 1
        in_area_of_lakes.category = "0.Fill DEM"

        params = [in_dem, out_dem, out_flow_dir, out_flow_accum, out_stream_network, in_threshold_stream_network, out_stream_order, out_stream_feature, out_basin_raster, out_basin_feature,
            in_force_flow, in_flow_direction_type, in_flow_accum_data_type, in_flow_accum_direction_type, in_stream_order_method, in_stream_feature_simplify, in_basin_feature_simplify,
            in_fill_method, in_area_of_lakes]

        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        in_dem = parameters[0].valueAsText
        out_dem = parameters[1].valueAsText
        out_flow_dir = parameters[2].valueAsText
        out_flow_accum = parameters[3].valueAsText
        out_stream_network = parameters[4].valueAsText
        in_threshold_stream_network = int(parameters[5].valueAsText)
        out_stream_order = parameters[6].valueAsText
        out_stream_feature = parameters[7].valueAsText
        out_basin_raster = parameters[8].valueAsText
        out_basin_feature = parameters[9].valueAsText
        in_force_flow = parameters[10].valueAsText
        in_flow_direction_type = parameters[11].valueAsText
        in_flow_accum_data_type = parameters[12].valueAsText
        in_flow_accum_direction_type = parameters[13].valueAsText
        in_stream_order_method = parameters[14].valueAsText
        in_stream_feature_simplify = parameters[15].valueAsText
        in_basin_feature_simplify = parameters[16].valueAsText
        in_fill_method = parameters[17].valueAsText
        in_area_of_lakes = parameters[18].valueAsText.replace(",", ".")

        # 1. Fill DEM
        if in_fill_method == "PRATIK MUCHKARNI":
            outFill = Fill(Float(in_dem))
            if out_dem:
                outFill.save(out_dem)

        elif in_fill_method == "VLADIMIR S. DEKHNICH":
            outFlowDirection_alternative = FlowDirection(in_dem)
            outSink_alternative = Sink(outFlowDirection_alternative)
            outSinkFeature = "in_memory/outSinkFeature"
            arcpy.RasterToPolygon_conversion(outSink_alternative, outSinkFeature, "NO_SIMPLIFY")
            arcpy.management.AddField(outSinkFeature, "Area", "DOUBLE")
            arcpy.CalculateField_management(outSinkFeature, "Area", "!SHAPE.area@SQUAREKILOMETERS!", "PYTHON_9.3")
            sink_filtered = "in_memory/outSinkFeature_filtered"
            arcpy.analysis.Select(outSinkFeature, sink_filtered, '"Area" > {0}'.format(in_area_of_lakes))
            outZonalStatistics = ZonalStatistics(sink_filtered, 'OBJECTID', in_dem,"MEAN", "NODATA")
            outFill = Fill(Float(in_dem))
            arcpy.Mosaic_management(Int(outZonalStatistics), outFill,"LAST")
            if out_dem:
                outFill.save(out_dem)

        # 2. Flow Direction
        outFlowDirection = FlowDirection(outFill, in_force_flow, '', in_flow_direction_type)
        if out_flow_dir:
            outFlowDirection.save(out_flow_dir)

        # 3. Flow Accumulation
        outFlowAccumulation = FlowAccumulation(outFlowDirection, '', in_flow_accum_data_type, in_flow_accum_direction_type)
        if out_flow_accum:
            outFlowAccumulation.save(out_flow_accum)

        # 4.  Stream Network
        if out_stream_network:
            outStreamNetwork = Con(outFlowAccumulation > in_threshold_stream_network, 1)
            outStreamNetwork.save(out_stream_network)

        # 4. Stream Order Raster
        if out_stream_order:
            outStreamNetwork = Con(outFlowAccumulation > in_threshold_stream_network, 1)
            outStreamOrder = StreamOrder(outStreamNetwork, outFlowDirection, in_stream_order_method)
            outStreamOrder.save(out_stream_order)

        # 5. Stream to Feature
        if out_stream_feature:
            outStreamNetwork = Con(outFlowAccumulation > in_threshold_stream_network, 1)
            outStreamOrder = StreamOrder(outStreamNetwork, outFlowDirection, in_stream_order_method)
            StreamToFeature(outStreamOrder, outFlowDirection, out_stream_feature, in_stream_feature_simplify)

        # 6. Basin raster
        if out_basin_raster:
            outBasin = Basin(outFlowDirection)
            outBasin.save(out_basin_raster)

        # 7. Basin out_stream_feature
        if out_basin_feature:
            outBasin = Basin(outFlowDirection)
            outBasinFeature = arcpy.RasterToPolygon_conversion(outBasin, out_basin_feature, in_basin_feature_simplify)

        return