import bpy
from mathutils import Vector, noise
from mathutils.kdtree import KDTree
from random import random, randint, gauss, seed
from math import fabs
from time import time

'''
Template for a particle system
Includes efficient caching using duplication
'''

class Particle:
    
    
    def __init__(self, index, location=Vector()):
        targ_vel = 0.005
        self.MAX_VEL = gauss(targ_vel, targ_vel / 10)
        
        self.location = location.copy()
        self.velocity = noise.random_unit_vector() * self.MAX_VEL
        self.guide_index = index

        self.noise_seed = noise.random_unit_vector()
        
        self.active = True
        
        self.direction = randint(0,1)*2-1
        
#        if index > guide_len/2:
#            self.direction = -1
#        else:
#            self.direction = 1

        
        self.behaviour = 0.5 # 1 = guide ; 0 = turbulence

class Particle_system:
    
    GUIDE_STRENGTH = 1.0
    
    TURBULENCE_FREQUENCY = 10
    TURBULENCE_STRENGTH = 1.0
    
    AVOID_THRESHOLD = 0.05
    AVOID_STRENGTH = 0.2
    
    def __init__(self, guide, ground):
        self.frame = 0
        
        self.particles = []
        self.guide = guide
#        self.vertex_distance = (self.guide.data.vertices[0].co - self.guide.data.vertices[1].co).length_squared
        
        self.guide_tree = KDTree(len(self.guide.data.vertices))
        for v in self.guide.data.vertices:
            self.guide_tree.insert(v.co, v.index)
        self.guide_tree.balance()
        
        self.ground = ground
        
#        bpy.ops.mesh.primitive_ico_sphere_add(location=(0,0,0), size=0.01)
#        self.instance_obj = bpy.context.object
        self.instance_obj = bpy.data.objects['Fleche']
        self.instance_mesh = self.instance_obj.data
        self.instance_mesh.materials.append(bpy.data.materials['noir'])
        
        
    def add_particles(self, particles_number):
        '''Add a new particle to the system'''
        for p in range(particles_number):
            ind = randint(1, len(self.guide.data.vertices)-2)
            self.particles.append(Particle(ind, self.guide.data.vertices[ind].co))
    
    def kill_particle(self, part):
        self.particles.remove(part)
    
    def create_tree(self):
        self.parts_tree = KDTree(len(self.particles))
        for i, p in enumerate(self.particles):
            self.parts_tree.insert(p.location, i)
        self.parts_tree.balance()
        
    
    def step(self):
        '''Simulate next frame'''
        self.frame += 1
        self.create_tree()
        
        for part in self.particles:
            if part.active:
                
                previous_velocity = part.velocity.copy()
                
                #guide vector
                guide_vector = self.guide.data.vertices[part.guide_index].co - part.location
                guide_vector = guide_vector.normalized() * self.GUIDE_STRENGTH

                #turbulence vector
                turbulence = noise.turbulence_vector(part.noise_seed+part.location, 2, False, 1, self.TURBULENCE_STRENGTH, self.TURBULENCE_FREQUENCY)
#                part.noise_seed += turbulence / 50
#                if part.velocity.length_squared < 0.0001:
#                    part.noise_seed = noise.random_unit_vector()
                part.noise_seed.z += 0.01
                
                #boid-like vector
                too_close = self.parts_tree.find_range(part.location, self.AVOID_THRESHOLD)
                avoid_vector = Vector()
                for p in too_close:
                    
                    other_vec = part.location - p[0]
                    if other_vec.length_squared < 0.0001:
                        continue
                    other_vec /= other_vec.length
                    avoid_vector += other_vec
                    
#                avoid_vector.normalize()
#                avoid_vector -= part.velocity
                avoid_vector *= self.AVOID_STRENGTH
                
                #velocity change
                
                part.velocity += avoid_vector
                
                part.velocity += turbulence * (1.0-part.behaviour)
                part.velocity += guide_vector * part.behaviour
                    
                #limit velocity (drag and shit)
                if part.velocity.length > part.MAX_VEL:
                    part.velocity.length = part.MAX_VEL
                
                # limit rotation
                rotation_scalar = previous_velocity.dot(part.velocity) * 0.5 + 0.5 # normalized 0-1
#                rotation_scalar **= 3
                if rotation_scalar > 0.1:
                    rotation_scalar = 0.1
#                rotation_scalar = 0
                part.velocity *= (rotation_scalar)
                part.velocity += previous_velocity * (1-rotation_scalar)
                
                # put that shit on the ground
                closest = self.ground.closest_point_on_mesh(part.location)
                part.location = closest[0]
                # velocity parallel to the ground
                vel_norm = part.velocity.length
                inter = part.velocity.cross(closest[1])
                part.velocity = closest[1].cross(inter)
                part.velocity.length = vel_norm
#                print(part.velocity)
                
                # SET NEW LOCATION
                part.location += part.velocity
                    
                # behaviour change
                part.behaviour += random()*0.1-0.05
                if part.behaviour < 0.1:
                    part.behaviour = 0.1
                if part.behaviour > 0.9:
                    part.behaviour = 0.9
                    
#                # set goal to next vertex if close enough
                pt, ind, dist = self.guide_tree.find(part.location)
                if fabs(ind - part.guide_index) < 2:
                    part.guide_index += part.direction
#                if self.frame % 20 == 0:
#                    part.guide_index += part.direction
                
#                if next_point_distance.length_squared < self.vertex_distance:
#                    part.guide_index += 1
                    
                # switch direction if end reached
                if part.guide_index >= len(self.guide.data.vertices)-1 or part.guide_index == 1:
#                    part.active = False
#                    self.kill_particle(part)
                    part.direction = -part.direction
                    part.guide_index += part.direction

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
        
    
        vertices = [(p.location, p.velocity) for p in self.particles]
        generator_mesh = bpy.data.meshes.new('generator_{:05}'.format(frame))
        
#        generator_mesh.from_pydata(vertices, [], [])
        
        ## Track to camera
#        cam = bpy.context.scene.camera
        for v in vertices:
            generator_mesh.vertices.add(1)
            generator_mesh.vertices[-1].co = v[0]
            generator_mesh.vertices[-1].normal = v[1]
#            generator_mesh.vertices[-1].normal = cam.location - v
        
        generator_obj = bpy.data.objects.new('generator_{:05}'.format(frame), generator_mesh)
        bpy.context.scene.objects.link(generator_obj)
        
        instance_obj_frame.parent = generator_obj
        generator_obj.dupli_type = "VERTS"
        generator_obj.use_dupli_vertices_rotation = True
        
        #anim
        generator_obj.keyframe_insert('hide', frame=frame)
        generator_obj.keyframe_insert('hide_render', frame=frame)
        generator_obj.hide = True
        generator_obj.hide_render = True
        generator_obj.keyframe_insert('hide', frame=frame+1)
        generator_obj.keyframe_insert('hide_render', frame=frame+1)
        generator_obj.keyframe_insert('hide', frame=frame-1)
        generator_obj.keyframe_insert('hide_render', frame=frame-1)
        

if __name__ == '__main__':
    
    for o in bpy.data.objects:
        if o.name.startswith('generator') or o.name.startswith('Ico') or o.name.startswith('instance'):
            o.user_clear()
            bpy.context.scene.objects.unlink(o)
            bpy.data.objects.remove(o)
    
#    guide = bpy.data.objects['Chemin']
#    ground = bpy.data.objects['Sol']
    guide = bpy.context.object
    ground = bpy.context.selected_objects[-1]
    a_ps = Particle_system(guide, ground)
    a_ps.add_particles(100)
    
    print('\n---')
    start = time()
    seed(0)
    noise.seed_set(0)
    for f in range(1000):
#        a_ps.add_particles(1)
        if f%10 == 0:
            print('frame: {:04}'.format(f))
        a_ps.step()
    print('Simulated in {:05.5f} seconds'.format(time() - start))