from iden import Iden

for i in range(1, 1000):
    iden_avatar = Iden('text' + str(i), 'circle')
    iden_avatar.setBackgroundColor('#EEEEEE')
    iden_avatar.save('test/circle-'+str(i)+'.svg')

    iden_avatar = Iden('text' + str(i), 'pixel')
    iden_avatar.setBackgroundColor('#EEEEEE')
    iden_avatar.save('test/pixel-'+str(i)+'.svg')
