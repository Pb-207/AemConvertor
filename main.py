import os
from tqdm import tqdm
import struct
from numpy import float32

if __name__ == '__main__':
    option = int(input("Please choose the feature ( 1.aem2obj | 2.obj2aem ): "))
    # option = 1
    if option == 1:
        file_in = input("Please input the path of the file to be converted: ")
        file_in = "test.aem"
        file_out = file_in.replace(".aem", ".obj")
        if os.path.exists(file_out):
            print('Warning:', file_out, 'already exists and will be covered! Press Enter to continue.')
            input()
            os.remove(file_out)
        file_aem = open(file_in, 'rb')
        file_obj = open(file_out, 'a')
        file_aem.seek(24)
        v_num = struct.unpack("h", file_aem.read(2))[0]
        s = '# Vertices ' + str(v_num) + '\n'
        file_obj.write(s)
        print('# Vertices', v_num)
        file_aem.seek(v_num * 2 + 2, 1)
        v_x = []
        v_y = []
        v_z = []
        i = 0
        for i in tqdm(range(v_num)):
            v_x.append(float32(struct.unpack("f", file_aem.read(4))[0]))
            v_y.append(float32(struct.unpack("f", file_aem.read(4))[0]))
            v_z.append(float32(struct.unpack("f", file_aem.read(4))[0]))
            s = 'v  ' + str(v_x[i]) + ' ' + str(v_y[i]) + ' ' + str(v_z[i]) + '\n'
            file_obj.write(s)
        s = '\n' + '# UVs ' + str(v_num) + '\n'
        file_obj.write(s)
        print('\n', '# UVs', v_num)
        vt_x = []
        vt_y = []
        i = 0
        for i in tqdm(range(v_num)):
            vt_x.append(float32(struct.unpack("f", file_aem.read(4))[0]))
            vt_y.append(float32(struct.unpack("f", file_aem.read(4))[0]))
            s = 'vt  ' + str(vt_x[i]) + ' ' + str(vt_y[i]) + '\n'
            file_obj.write(s)
        s = '\n' + '# Normals ' + str(v_num) + '\n'
        file_obj.write(s)
        print('\n', '# Normals', v_num)
        vn_x = []
        vn_y = []
        vn_z = []
        for i in tqdm(range(v_num)):
            vn_x.append(float32(struct.unpack("f", file_aem.read(4))[0]))
            vn_y.append(float32(struct.unpack("f", file_aem.read(4))[0]))
            vn_z.append(float32(struct.unpack("f", file_aem.read(4))[0]))
            s = 'vn  ' + str(vn_x[i]) + ' ' + str(vn_y[i]) + ' ' + str(vn_z[i]) + '\n'
            file_obj.write(s)
        s = '\n' + '# Faces ' + str(v_num // 3) + '\n'
        file_obj.write(s)
        print('\n', '# Faces', v_num // 3)
        for i in tqdm(range(v_num // 3)):
            file_obj.write('f  ')
            s = str(i * 3 + 1) + '/' + str(i * 3 + 1) + '/' + str(i * 3 + 1)
            file_obj.write(s)
            file_obj.write(' ')
            s = str(i * 3 + 2) + '/' + str(i * 3 + 2) + '/' + str(i * 3 + 2)
            file_obj.write(s)
            file_obj.write(' ')
            s = str(i * 3 + 3) + '/' + str(i * 3 + 3) + '/' + str(i * 3 + 3)
            file_obj.write(s)
            file_obj.write('\n')
        file_aem.close()
        file_obj.close()
        print('\n', 'Done')
    elif option == 2:
        print('Obj2aem is not supported yet, please wait...')
