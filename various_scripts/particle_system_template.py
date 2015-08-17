'''
Template for a particle system
Includes efficient caching using duplication
'''

class Particle_system:
    
    def __init__(self):
        self.frame = 0
        
        self.particles = []
        
        bpy.ops.mesh.primitive_ico_sphere_add(location=(0,0,0))
        self.instance_obj = bpy.context.object
        self.instance_mesh = self.instance_obj.data
        
        
    def add_particle(self, particles_number):
        '''Add a new particle to the system'''
        pass
        
    
    def step(self):
        '''Simulate next frame'''
        self.frame += 1
        
        # SIMULATE STUFF HERE

        self.create_frame(self.frame)
    
    def create_frame(self, frame):
        '''
        For each frame:
            - create a new instance of the object to duplicate (eg. a sphere)
            - get a list of vertices from particles' positions
            - create a new generator objects, use the vertex list to generate mesh
                - this object will be used for duplication
            - parent the object to duplicate to the generator object
            - animate the visibility of both objects
            '''
        
        instance_obj_frame = bpy.data.objects.new('instance_{:05}'.format(frame), self.instance_mesh)
        bpy.context.scene.objects.link(instance_obj_frame)
        
    
        vertices = [p.location for p in self.particles]
        generator_mesh = bpy.data.meshes.new('generator_{:05}'.format(frame))
        
        generator_mesh.from_pydata(v
        cam = bpy.context.scene.camera
        for v in vertices:
            generator_mesh.vertices.add(1)
            generator_mesh.vertices[-1].co = v
            generator_mesh.vertices[-1].normal = cam.location - v
        
        generator_obj = bpy.data.objects.new('generator_{:05}'.format(frame), generator_mesh)
        bpy.context.scene.objects.link(generator_obj)
        
        instance_obj_frame.parent = generator_obj
        generator_obj.dupli_type = "VERTS"
        
        #anim
        generator_obj.keyframe_insert('hide', frame=frame)
        generator_obj.keyframe_insert('hide_render', frame=frame)
        generator_obj.hide = True
        generator_obj.hide_render = True
        generator_obj.keyframe_insert('hide', frame=frame+1)
        generator_obj.keyframe_insert('hide_render', frame=frame+1)
        generator_obj.keyframe_insert('hide', frame=frame-1)
        generator_obj.keyframe_insert('hide_render', frame=frame-1)
        
