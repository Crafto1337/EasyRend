bl_info = {
    "name": "EasyRend",
    "author": "Crafto 1337",
    "version": (0, 1, 2),
    "blender": (2, 80, 0),
    "description": "Easily change the render settings of your project",
    "warning": "",
    "wiki_url": "",
    "category": "Render",
}

import bpy
from bpy.types import PropertyGroup

#def LoadPreset(context):
    
    
    
def overwrite(context):
    scene = context.scene
    propies = scene.properties
    
    if propies.engine == 'OP1':
        bpy.context.scene.render.engine = 'BLENDER_EEVEE'
        bpy.context.scene.eevee.taa_render_samples = propies.samples
    elif propies.engine == 'OP2':
        bpy.context.scene.render.engine = 'BLENDER_WORKBENCH'
    else:
        bpy.context.scene.render.engine = 'CYCLES'
        bpy.context.scene.cycles.samples = propies.samples
        bpy.context.scene.cycles.max_bounces = propies.bounces
        bpy.context.scene.render.tile_x = propies.tileSize
        bpy.context.scene.render.tile_y = propies.tileSize
        
    if propies.device == 'OP1':
         bpy.context.scene.cycles.device = 'CPU'
    else:
        bpy.context.scene.cycles.device = 'GPU'

    bpy.context.scene.render.resolution_x = propies.resX
    bpy.context.scene.render.resolution_y = propies.resY
    bpy.context.scene.render.resolution_percentage = propies.resPercent

    if propies.output == 'OP1':
        bpy.context.scene.render.image_settings.file_format = 'PNG'
        if propies.transparent == True:
            bpy.context.scene.render.film_transparent = True
            bpy.context.scene.render.image_settings.color_mode = 'RGBA'
        else:
            bpy.context.scene.render.film_transparent = False
            bpy.context.scene.render.image_settings.color_mode = 'RGB'
    else:
        bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
        bpy.context.scene.render.ffmpeg.format = "MPEG4"
        bpy.context.scene.render.ffmpeg.codec = "H264"
        bpy.context.scene.render.ffmpeg.gopsize = 1
        bpy.context.scene.render.ffmpeg.video_bitrate = propies.bitrate
        bpy.context.scene.render.ffmpeg.minrate = propies.min_bitrate
        bpy.context.scene.render.ffmpeg.maxrate = propies.max_bitrate
        

    bpy.context.scene.render.fps = propies.fps
    bpy.context.scene.frame_step = propies.step
    
    if propies.quality == 'OP1':
        bpy.context.scene.render.ffmpeg.constant_rate_factor = 'LOWEST'
    elif propies.quality == 'OP2':
        bpy.context.scene.render.ffmpeg.constant_rate_factor = 'VERYLOW'
    elif propies.quality == 'OP3':
        bpy.context.scene.render.ffmpeg.constant_rate_factor = 'LOW'
    elif propies.quality == 'OP4':
        bpy.context.scene.render.ffmpeg.constant_rate_factor = 'MEDIUM'
    elif propies.quality == 'OP5':
        bpy.context.scene.render.ffmpeg.constant_rate_factor = 'HIGH'
    elif propies.quality == 'OP6':
        bpy.context.scene.render.ffmpeg.constant_rate_factor = 'PERC_LOSSLESS'
    elif propies.quality == 'OP7':
        bpy.context.scene.render.ffmpeg.constant_rate_factor = 'LOSSLESS'
    else:
        bpy.context.scene.render.ffmpeg.constant_rate_factor = 'NONE'
        
    bpy.context.scene.render.filepath = propies.path

class LoadPresetButton(bpy.types.Operator):
    bl_idname = "object.load_preset"
    bl_label = "Load Preset Button"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        LoadPreset(context)
        return {'FINISHED'}

class OverwriteButton(bpy.types.Operator):
    bl_idname = "object.overwrite"
    bl_label = "Overwrite Button"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        overwrite(context)
        return {'FINISHED'}

class Properties(bpy.types.PropertyGroup):
    
    preset : bpy.props.EnumProperty(
        name = "Presets",
        description = "",
        items = [
            ('OP1', "Fastest", "Fastest, but with the worst quality"),
            ('OP2', "Fast", "Fast, but with a low quality"),
            ('OP3', "Blanced", "A balance out of speed and quality"),
            ('OP4', "Good", "Slow, but with a good quality"),
            ('OP4', "Best", "Slowest, but with the best quality"),
        ]
    )
    
    engine : bpy.props.EnumProperty(
        name = "Render Engine",
        description = "",
        items = [
            ('OP1', "EEVEE", "Use the EEVEE render engine"),
            ('OP2', "Workbench", "Use the Workbench render engine"),
            ('OP3', "Cycles", "Use the Cycles render engine")
        ]
    )
    
    device : bpy.props.EnumProperty(
        name = "Render Device",
        description = "",
        items = [
            ('OP1', "CPU", "Use CPU for rendering"),
            ('OP2', "GPU", "Use GPU for rendering")
        ]
    )
    
    samples : bpy.props.IntProperty(
        name = "Samples",
        #description = "",
        soft_min = 1,
        default = 64
    )
    
    bounces : bpy.props.IntProperty(
        name = "Light Bounces",
        #description = ""
        soft_min = 1,
        default = 12
    )

    resX : bpy.props.IntProperty(
        name = "Resolution X",
        #description = "",
        soft_min = 4,
        soft_max = 65536,
        default = 1920
    )
    
    resY : bpy.props.IntProperty(
        name = "Resolution Y",
        #description = "",
        soft_min = 4,
        soft_max = 65536,
        default = 1080
    )
    
    resPercent : bpy.props.IntProperty(
        name = "Resolution %",
        #description = "",
        soft_min = 1,
        soft_max = 100,
        default = 100
    )
    
    tileSize : bpy.props.IntProperty(
        name = "Tile Size",
        #description = "",
        soft_min = 8,
        soft_max = 512,
        default = 32
    )

    output : bpy.props.EnumProperty(
        name = "Output Type",
        description = "",
        items = [
            ('OP1', "Image", "Give an still image as output"),
            ('OP2', "Video", "Give an video as output")
        ]
    )
    
    transparent : bpy.props.BoolProperty(
        name = "Transparent"
    )
    
    animation : bpy.props.BoolProperty(
        name = "Animation"
    )
    
    fps : bpy.props.IntProperty(
        name = "Frame Rate",
        #description = "",
        soft_min = 1,
        soft_max = 120,
        default = 24
    )
    
    step : bpy.props.IntProperty(
        name = "Frame Step",
        #description = "",
        soft_min = 1,
        soft_max = 100,
        default = 1
    )

    quality : bpy.props.EnumProperty(
        name = "Output Quality",
        description = "",
        items = [
            ('OP1', "Lowest quality", "worst quality"),
            ('OP2', "Very low quality", "better, but still bad"),
            ('OP3', "Low quality", "low quality"),
            ('OP4', "medium quality", "normal quality"),
            ('OP5', "High quality", "high quality"),
            ('OP6', "Perceptually lossless", "nearly lossless quality"),
            ('OP7', "Lossless", "lossless quality"),
            ('OP8', "Constant Bitrate", "the best quality")
        ],
        default = 'OP4'
    )
    
    bitrate : bpy.props.IntProperty(
        name = "Bitrate",
        #description = "",
        soft_min = 1,
        soft_max = 10000,
        default = 6000
    )
    
    min_bitrate : bpy.props.IntProperty(
        name = "Minumum",
        #description = "",
        soft_min = 1,
        soft_max = 10000,
        default = 1
    )
    
    max_bitrate : bpy.props.IntProperty(
        name = "Maximum",
        #description = "",
        soft_min = 1,
        soft_max = 10000,
        default = 9000
    )
    
    speed : bpy.props.EnumProperty(
        name = "Encoding Speed",
        description = "",
        items = [
            ('OP1', "Slowest", "Very slow, but highest Quality"),
            ('OP2', "Good", "Average speed. Not too slow and no big quality lossage"),
            ('OP3', "Realtime", "If you need it really fast, then this is your option, but the quality isn´t the best")
        ],
        default = 'OP2'
    )
    
    path : bpy.props.StringProperty(
        name = "Output Path",
        #description = "My description",
	subtype='FILE_PATH'
    )

class uiPanel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "EasyRend"
    bl_label = 'EasyRend'
    
    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        scene = context.scene
        propies = scene.properties
        
        row = col.row()
        
        col.separator()
        col.prop(propies, "engine")
        
        
        
        if propies.engine == 'OP3':
            col.separator()
            col.prop(propies, "device")
            col.separator()
            col.prop(propies, "tileSize")
            col.separator()
        else:
            col.separator()
        
        col.prop(propies, "samples")
        
        if propies.engine == 'OP3':
            col.separator()
            col.prop(propies, "bounces")
            col.separator()
        else:
            col.separator()
        
        col.prop(propies, "resX")
        col.prop(propies, "resY")
        col.prop(propies, "resPercent", slider=True)
        
        col.separator()
        col.prop(propies, "output")
        
        if propies.output == 'OP1':
            col.separator()
            col.prop(propies, "transparent")
            col.separator()
            col.prop(propies, "animation")
            col.separator()
        else:
            col.separator()
        
        if propies.animation == True:
            col.prop(propies, "fps")
            
            col.separator()
            col.prop(propies, "step")
            col.separator()
        else:
            col.separator()
        
        if propies.output == 'OP2':
            col.prop(propies, "quality")
            
            if propies.quality == 'OP8':
                col.separator()
                col.prop(propies, "bitrate")
                col.prop(propies, "min_bitrate")
                col.prop(propies, "max_bitrate")
                col.separator()
            else:
                col.separator()
            
            col.prop(propies, "speed")
            col.separator()
        else:
            col.separator()
        
        col.prop(propies, "path")

        col.separator()
        row = col.row()
        row.operator("object.overwrite", text="Overwrite")
        
        col.separator()
        row = col.row()
        if propies.animation == True or propies.output == 'OP2':
            row.operator("render.render", text="Render", icon='RENDER_ANIMATION').animation = True
        else:
            row.operator("render.render", text="Render", icon='RENDER_STILL')

def register():
    bpy.utils.register_class(LoadPresetButton)
    bpy.utils.register_class(OverwriteButton)
    bpy.utils.register_class(Properties)
    
    bpy.types.Scene.properties = bpy.props.PointerProperty(type= Properties)

    bpy.utils.register_class(uiPanel)

def unregister():
    bpy.utils.unregister_class(LoadPresetButton)
    bpy.utils.unregister_class(OverwriteButton)
    bpy.utils.unregister_class(Properties)
        
    del bpy.types.Scene.properties

    bpy.utils.unregister_class(uiPanel)


if __name__ == "__main__":
    register()