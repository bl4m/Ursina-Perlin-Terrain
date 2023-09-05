from ursina import *
from perlin_noise import PerlinNoise
from ursina.shaders import basic_lighting_shader

def scale(val, src, dst):
    """
    Scale the given value from the scale of src to the scale of dst.
    """
    return ((val - src[0]) / (src[1]-src[0])) * (dst[1]-dst[0]) + dst[0]


noise1 = PerlinNoise(1,random.randint(0,100000))
noise2 = PerlinNoise(1,random.randint(0,100000))
noise3 = PerlinNoise(1,random.randint(0,100000))

class TerrainChunk(Entity):
    def __init__(self,offset,**kwargs):
        self.xSize = 100
        self.zSise = 100
        self.height = 0
        self.depth = 0
        self.offset = offset

        self.vertices = []
        self.triangles = []
        self.uvs = []
        self.colors = []
        self.generate_terrain()
        super().__init__(
            model = Mesh(vertices=self.vertices,triangles=self.triangles,uvs=self.uvs,colors=self.colors),
            position=offset,
            **kwargs
        )
        self.model.generate_normals(False)
        self.model.colors = self.colors

    def generate_terrain(self):
        vert = 0
        for z in range(self.zSise+1):
            for x in range(self.xSize+1):
                
                y1 = noise1(((x+self.offset[0])*0.4,(z+self.offset[2])*0.4)) * 2
                y2 = noise2(((x+self.offset[0])*0.1,(z+self.offset[2])*0.1)) * 10
                y3 = noise3(((x+self.offset[0])*0.02,(z+self.offset[2])*0.02)) * 50
                y = y1+y2+y3

                if y > self.height:
                    self.height = y
                if y < self.depth:
                    self.depth = y

                self.vertices.append(Vec3(x,y,z))
                self.uvs.append(Vec2(x/self.xSize,z/self.zSise))
                #yScaled = scale(y,(-20,20),(0,255))
                #self.colors.append(color.rgb(yScaled,yScaled,yScaled,255))

                if x < self.xSize and z < self.zSise:
                    self.triangles.append([vert+0,vert+1,vert+self.xSize+2,vert+self.xSize+1])
                    vert += 1
            if x <= self.xSize and z <= self.zSise:
                vert += 1

app = Ursina()
terrain1 = TerrainChunk(offset=Vec3(0,0,0),shader=basic_lighting_shader,texture='grass')
terrain2 = TerrainChunk(offset=Vec3(100,0,0),shader=basic_lighting_shader,texture='grass')
terrain1 = TerrainChunk(offset=Vec3(100,0,100),shader=basic_lighting_shader,texture='grass')
terrain2 = TerrainChunk(offset=Vec3(0,0,100),shader=basic_lighting_shader,texture='grass')
EditorCamera()
e = Entity(model='cube',texture='white_cube',y=10,x=100,z=100)
Sky()
app.run()