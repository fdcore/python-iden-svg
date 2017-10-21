from iden import Iden
import hashlib

m = hashlib.md5()
bg_colors = ['#FFFFFF', '#EEEEEE', False]

for i in range(0, 2):
    for bg in bg_colors:
        name = (str(i) + "test")
        m.update(name.encode('UTF-8'))
        iden_avatar = Iden(m.hexdigest(), 'circle')
        iden_avatar.setBackgroundColor(bg)
        iden_avatar.save('example/circle-'+m.hexdigest()+'.svg')

        iden_avatar = Iden(m.hexdigest(), 'pixel')
        iden_avatar.setBackgroundColor(bg)
        iden_avatar.save('example/pixel-'+m.hexdigest()+'.svg')
