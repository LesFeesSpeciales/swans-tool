import bpy
import os

def proxify(img):
    if 'is_proxy' in img:# and img['is_proxy'] == True:
        if img['is_proxy'] and img.size[0] != bpy.context.scene.proxy_destination:
#            print(img)
#            print(img['original'])
            original = bpy.data.images[img['original']]
            deproxify(img)
            
            proxify(img)
        else:
            return
        
    if img.source == 'FILE' and img.size[0] > bpy.context.scene.proxy_width_threshold:
        #ignore images which are already proxies
        img_orig = img.copy()
        img_orig.use_fake_user = True
        img_orig['is_proxy'] = False
        img_orig.name = img.name + "_orig"
        
        img['is_proxy'] = True
        img['original'] = img_orig.name
        img['use_alpha'] = img_orig.use_alpha
        img.use_alpha = True
        
        #SCALE
        dest = bpy.context.scene.proxy_destination
        w, h = img.size
        h *= dest/w
        w = dest
        img.scale(w,h)

        path, ext = os.path.splitext(bpy.path.abspath(img.filepath))
        path, filename = os.path.split(path)
        #path = os.path.join(path, 'proxy')
        filename += "_proxy" + ext
        path = os.path.join(path, 'proxy', filename)
        img.save_render(path, scene=bpy.context.scene)
        img.filepath = path
        
        img.reload()

    #        for obj in bpy.context.selected_objects:
    #            img = obj.active_material.active_texture.image
    #            img.reload()
    #            img_copy = img.copy()
    #            img_copy.name = img.name + "_orig"
    #            img.scale(img.size[0]*0.2, img.size[1]*0.2)
    #            path = bpy.path.abspath('//'+img.name.split(".")[0]+"_proxy.png")
    #            img.save_render(path)
    #         
    #            img.filepath = img.filepath.split(".")[0] + "_proxy.png"
    #            img.reload()

def get_selected_images():
    images_selected = set()
    for obj in bpy.context.selected_objects:
        for mat in obj.material_slots:
            for tex in mat.material.texture_slots:
                if tex is not None and tex.texture.type == 'IMAGE' and tex.texture.image is not None:
                    images_selected.add(tex.texture.image)
    return images_selected
    

class ImageProxify(bpy.types.Operator):
    """Resize large images for performance"""
    bl_idname = "image.proxify"
    bl_label = "Proxify Images"

#    @classmethod
#    def poll(cls, context):
#        return context.active_object is not None

    def execute(self, context):
        images_to_process = get_selected_images() if bpy.context.scene.proxy_only_selected else bpy.data.images
        
#        if bpy.context.scene.proxy_only_selected:
            
        
        number_imgs = len(images_to_process)
        
        for i, img in enumerate(images_to_process):
            print("Proxy: processing image {:03} of {:03} : {}".format(i+1, number_imgs, img.name))
            proxify(img)
        print("Proxy: done.")
        return {'FINISHED'}
    
def deproxify(img):
    if 'is_proxy' in img:
        if img['is_proxy']:
            #print(bpy.data.images[img.name+'_orig'].filepath)
            img.filepath = bpy.data.images[img.name+'_orig'].filepath
            img.reload()
            del img['is_proxy']
            del img['original']
            img.use_alpha = img['use_alpha']
            del img['use_alpha']
        else: #is an original image
            img.name += '_garbage'
            img.user_clear()
            bpy.data.images.remove(img)
    

class ImageDeProxify(bpy.types.Operator):
    """Reset proxy images to their original side"""
    bl_idname = "image.deproxify"
    bl_label = "Deproxify Images"

#    @classmethod
#    def poll(cls, context):
#        return context.active_object is not None

    def execute(self, context):
        #try to avoid crashing when an original image is visible in UI and deleted
        for area in bpy.context.screen.areas:
            if area.type == 'IMAGE_EDITOR':
                displayed_img = area.spaces.active.image
                if displayed_img is not None and 'is_proxy' in displayed_img and not displayed_img['is_proxy']:# and not displayed_img['is_proxy']:
                    area.spaces.active.image = None
        
        images_to_process = get_selected_images() if bpy.context.scene.proxy_only_selected else bpy.data.images
        for img in images_to_process:
            deproxify(img)
        return {'FINISHED'}
            
#        for obj in bpy.context.selected_objects:
#            tex = obj.active_material.active_texture
#            img = tex.image.name
#            print(img)
#            orig_img = bpy.data.images[img+"_orig"]
#            tex.image = orig_img

class ImageProxyPanel(bpy.types.Panel):
    """Image proxy panel"""
    bl_label = "Image proxy"
    bl_idname = "SCENE_PT_image_proxy"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'TOOLS'
    bl_context = "scene"
    bl_category = 'Tools'

    def draw(self, context):
        layout = self.layout

        scene = context.scene

        col = layout.column(align=True)
        col.prop(scene, "proxy_width_threshold")
        col.prop(scene, "proxy_destination")
        col.prop(scene, "proxy_only_selected")
        col.separator()
        
        col = layout.column(align=True)
        col.operator("image.proxify")
        col.operator("image.deproxify")
        img = context.area.spaces.active.image
        if img is None:
            return
        col.separator()
        if not 'is_proxy' in img:
            col.label("This image is not a proxy.")
        elif not img['is_proxy']:
            col.label("This image is an original one.")
        else:
            col.label("This image is a proxy.")
            col.label("Its width is %s pixels" % img.size[0])
            
#        col.label("This image is %sa proxy." % ("not " if (not 'is_proxy' in img or not img['is_proxy']) else ""))
#        col.label(str(context.area.spaces.active.image['is_proxy']))
        
def register():
    bpy.types.Scene.proxy_width_threshold = bpy.props.IntProperty(name='Width threshold', description='Resize images if wider than this size', min=1, soft_max=4096, default = 1024)
    bpy.types.Scene.proxy_destination = bpy.props.IntProperty(name='Destination size', description='Resize images to this size', min=1, soft_max=4096, default = 1024)
    bpy.types.Scene.proxy_only_selected = bpy.props.BoolProperty(name='Only selected objects', description='Resize textures only on selected objects', default=False)
    bpy.utils.register_class(ImageProxify)
    bpy.utils.register_class(ImageDeProxify)
    bpy.utils.register_class(ImageProxyPanel)


def unregister():
    bpy.utils.unregister_class(ImageProxify)
    bpy.utils.unregister_class(ImageDeProxify)
    bpy.utils.unregister_class(ImageProxyPanel)



if __name__ == "__main__":
    register()

