import bpy
from bpy.props import StringProperty, IntProperty, CollectionProperty 
from bpy.types import PropertyGroup, UIList, Operator, Panel

# Addon information
bl_info = {
    "name" : "Texture Managemet",
    "author" : "Declan Richard Porter",
    "description" : "View all textures, change file paths etc...",
    "blender" : (2, 93, 0),
    "version" : (1, 0, 0),
    "location" : "N-pannel",
    "wiki_url": "",
    "tracker_url": "",
    "warning" : "",
    "support": "COMMUNITY",
    "category" : "System"
}

class ListItem(PropertyGroup):
    """Group of properties representing an item in the list."""

    path : StringProperty(           
           description="A name for this item",
           default="!?", 
           maxlen=1024,
            subtype="FILE_PATH")


class MY_UL_List(UIList):
    """Demo UIList."""

    def draw_item(self, context, layout, data, item, icon, active_data,
                  active_propname, index):

        # We could write some code to decide which icon to use here...
        custom_icon = 'OBJECT_DATAMODE'

        # Make sure your code supports all 3 layout types
        if self.layout_type in {'DEFAULT', 'COMPACT'}:            
            layout.prop(item, "path")
            #layout.label(text=item.path)

        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon = custom_icon)


class LIST_OT_Replace(Operator):
    """Add a new item to the list."""

    bl_idname = "my_list.replace"
    bl_label = "Applys the changes"

    def execute(self, context):
        find = context.scene.addon_Properties.find
        replace = context.scene.addon_Properties.replace
        for item in context.scene.my_list:
            item.path = item.path.replace(find, replace)                        

        return{'FINISHED'}


class LIST_OT_Update(Operator):
    """Add a new item to the list."""

    bl_idname = "my_list.update"
    bl_label = "Applys the changes"

    def execute(self, context):
        index = 0
        for image in bpy.data.images:
            if len(image.filepath) > 0:
                item = context.scene.my_list[index]                
                index += 1
                if image.filepath != item.path:
                    image.filepath = item.path
                    image.reload()                    


        return{'FINISHED'}


class LIST_OT_Refresh(Operator):
    """Add a new item to the list."""

    bl_idname = "my_list.refresh"
    bl_label = "Get all current images"

    def execute(self, context):
        bpy.ops.file.make_paths_absolute()
        context.scene.my_list.clear()
        for image in bpy.data.images:
            if len(image.filepath) > 0:
                item = context.scene.my_list.add()
                item.path = image.filepath

        return{'FINISHED'}

# Defintion of the UI properties
class Addon_Properties(bpy.types.PropertyGroup):
    s_input_seed : bpy.props.IntProperty(name="Seed", default = 2, description="Seed for RNG.")

    find : bpy.props.StringProperty(name="Find",
                                    description="Some elaborate description",
                                    default="",
                                    maxlen=1024)

    replace : bpy.props.StringProperty(name="Replace",
        description="Some elaborate description",
        default="",
        maxlen=1024)
    
    
# The panel UI
class Addon_Panel(bpy.types.Panel):
    bl_idname = "object_PT_Panel"
    bl_label = "Texture Management"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Texture Management"
    
    @classmethod
    def poll(cls, context):    
        return (context.object is not None)

    def draw(self, context):
        
        layout = self.layout
        scene = context.scene.addon_Properties

        # Create a box layout with the following properties
        row = layout.row()        
        row.prop(scene, "find")
        row.prop(scene, "replace")
        
        scene = context.scene

        row = layout.row()
        row.operator('my_list.replace', text = "Replace All")

        row = layout.row()
        row.operator('my_list.refresh', text = "Refresh Textures")

        row = layout.row()
        row.template_list("MY_UL_List", "The_List", scene,
                          "my_list", scene, "list_index")

        row = layout.row()
        row.operator('my_list.update', text = "Update Textures")




        

# Register operation and pannels with blender
def register():    
    bpy.utils.register_class(ListItem)
    bpy.utils.register_class(MY_UL_List)
    bpy.utils.register_class(Addon_Panel)    
    bpy.utils.register_class(Addon_Properties)
    bpy.utils.register_class(LIST_OT_Refresh)
    bpy.utils.register_class(LIST_OT_Update)
    bpy.utils.register_class(LIST_OT_Replace)
    bpy.types.Scene.my_list = CollectionProperty(type = ListItem)
    bpy.types.Scene.list_index = IntProperty(name = "Index for my_list", default = 0)    
    bpy.types.Scene.addon_Properties = bpy.props.PointerProperty(type=Addon_Properties)    

  
    
# Unregister operation and pannels with blender
def unregister():  

    del bpy.types.Scene.addon_Properties
    del bpy.types.Scene.my_list 
    del bpy.types.Scene.list_index

    bpy.utils.unregister_class(ListItem)
    bpy.utils.unregister_class(MY_UL_List)
    bpy.utils.unregister_class(Addon_Panel)
    bpy.utils.unregister_class(Addon_Properties)
    bpy.utils.unregister_class(LIST_OT_Refresh)
    bpy.utils.unregister_class(LIST_OT_Update)
    bpy.utils.unregister_class(LIST_OT_Replace)
    
    #auto_load.unregister()