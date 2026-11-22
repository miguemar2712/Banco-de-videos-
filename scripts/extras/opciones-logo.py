import sys, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
S=sys.argv[1]; base=Image.open(f'{S}/fondo4.png').convert('RGBA'); W=1080
PF='fuentes/PlayfairDisplayBlackItalic.ttf'; MB='fuentes/Montserrat-Black.ttf'; GV='fuentes/GreatVibes.ttf'
F=lambda p,s: ImageFont.truetype(p,s)
RED=(214,30,40,255); GOLD=(236,196,90,255); WHITE=(255,255,255,255)
def sombra(im,dib):
    c=Image.new('RGBA',im.size,(0,0,0,0)); dib(ImageDraw.Draw(c)); im.alpha_composite(c.filter(ImageFilter.GaussianBlur(14)))
def estrella(d,cx,cy,r,fill):
    v=[(cx+(r if i%2==0 else r*.4)*math.cos(math.radians(-90+i*36)),cy+(r if i%2==0 else r*.4)*math.sin(math.radians(-90+i*36))) for i in range(10)]; d.polygon(v,fill=fill)
L1,L2='Importa','desde China'
def op1(im):
    sombra(im,lambda d:d.rounded_rectangle((90,170,990,470),40,fill=(0,0,0,150)))
    d=ImageDraw.Draw(im); d.rounded_rectangle((90,160,990,460),40,fill=RED)
    for x in (150,930): estrella(d,x,310,34,GOLD)
    d.text((540,255),L1,font=F(PF,120),fill=WHITE,anchor='mm'); d.text((540,375),L2,font=F(PF,96),fill=GOLD,anchor='mm')
def op2(im):
    d=ImageDraw.Draw(im); sombra(im,lambda d:d.rounded_rectangle((310,110,770,570),30,fill=(0,0,0,140)))
    d.rounded_rectangle((300,100,760,560),30,fill=RED); d.rounded_rectangle((325,125,735,535),20,outline=GOLD,width=8)
    d.text((530,235),'IMPORTA',font=F(MB,72),fill=GOLD,anchor='mm'); d.text((530,345),'desde',font=F(GV,110),fill=WHITE,anchor='mm'); d.text((530,460),'CHINA',font=F(MB,96),fill=GOLD,anchor='mm')
def op3(im):
    d=ImageDraw.Draw(im); sombra(im,lambda d:d.ellipse((90,190,330,430),fill=(0,0,0,150)))
    d.ellipse((80,180,320,420),fill=RED,outline=WHITE,width=8); estrella(d,170,270,46,GOLD)
    for dx,dy in ((70,-55),(100,-15),(100,30),(70,70)): estrella(d,170+dx,270+dy,15,GOLD)
    sombra(im,lambda d:(d.text((660,250),L1,font=F(PF,130),fill=(0,0,0,220),anchor='mm'),d.text((660,370),L2,font=F(PF,90),fill=(0,0,0,220),anchor='mm')))
    d.text((655,245),L1,font=F(PF,130),fill=WHITE,anchor='mm'); d.text((655,365),L2,font=F(PF,90),fill=WHITE,anchor='mm')
def op4(im):
    sombra(im,lambda d:d.rounded_rectangle((150,180,930,470),150,fill=(0,0,0,130)))
    d=ImageDraw.Draw(im); d.rounded_rectangle((140,170,920,460),150,fill=WHITE)
    d.text((530,265),L1,font=F(PF,120),fill=RED,anchor='mm'); d.text((530,380),'— desde China —',font=F(MB,52),fill=(40,40,40,255),anchor='mm')
def op5(im):
    c=Image.new('RGBA',(700,420),(0,0,0,0)); d=ImageDraw.Draw(c)
    d.rounded_rectangle((10,10,690,410),40,outline=RED,width=14); d.rounded_rectangle((34,34,666,386),28,outline=RED,width=5)
    d.text((350,130),'IMPORTADO',font=F(MB,92),fill=RED,anchor='mm'); d.text((350,250),'desde China',font=F(PF,90),fill=RED,anchor='mm')
    d.text((350,345),'DIRECTO DE FÁBRICA',font=F(MB,38),fill=RED,anchor='mm')
    c=c.rotate(-6,expand=True,resample=Image.BICUBIC); im.alpha_composite(c,((W-c.width)//2,100))
def op6(im):
    d=ImageDraw.Draw(im); sombra(im,lambda d:d.rectangle((0,200,1080,470),fill=(0,0,0,140)))
    for y in range(190,460):
        t=(y-190)/270; d.line((0,y,1080,y),fill=(int(250-40*t),int(215-50*t),int(120-50*t),255))
    d.text((540,280),L1,font=F(PF,130),fill=(30,20,10,255),anchor='mm'); d.text((540,400),'DESDE CHINA',font=F(MB,64),fill=(150,20,20,255),anchor='mm')
ops=[('1 · Cinta roja',op1),('2 · Sello chino',op2),('3 · Bandera en círculo',op3),('4 · Etiqueta boutique',op4),('5 · Sello de aduana',op5),('6 · Banda dorada',op6)]
tiles=[]
for n,fn in ops:
    im=base.copy(); fn(im); d=ImageDraw.Draw(im); d.rectangle((0,690,1080,760),fill=(0,0,0,220)); d.text((540,725),n,font=F(MB,50),fill=(255,230,0,255),anchor='mm'); tiles.append(im.resize((360,253)))
o=Image.new('RGB',(1080,506)); [o.paste(t,((i%3)*360,(i//3)*253)) for i,t in enumerate(tiles)]; o.save('out/opciones-logo-sin-mapa.jpg',quality=92)
