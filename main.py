import os
from tqdm import tqdm
import struct
from numpy import float32, ushort


def select_file():
    while True:
        Convert_existing_models_yn = input('Do you want to override existing obj files?(y/n): ')
        if Convert_existing_models_yn == 'y':
            Convert_existing_models = True
            break
        elif Convert_existing_models_yn == 'n':
            Convert_existing_models = False
            break
        else:
            print("Invalid input, please enter either 'y' or 'n'.")

    while True:
        one_or_multiple = int(input('Do u want to convert 1 file or multiple files? ( 1.one | 2.multiple ): '))
        if one_or_multiple == 1:
            ask_one_file(Convert_existing_models)
            break
        elif one_or_multiple == 2:
            ask_multiple_files(Convert_existing_models)
            break
        else:
            print("Invalid input, please enter either 1 or 2.")


def ask_one_file(Convert_existing_models):
    file_in = input("Please input the path of the file to be converted(Press Enter to exit): ")

    if file_in.endswith('.aem') or file_in.endswith('.obj'):
        if option == 1:
            file_out = file_in.replace(".aem", ".obj")
            if os.path.exists(file_out) and Convert_existing_models == True:
                os.remove(file_out)
            if file_in.endswith('.aem'):
                try:
                    print('Converting', os.path.basename(file_in))
                    convert_aem_to_obj(file_in)
                except Exception as e:
                    print("An unexpected error occurred:", e)
        elif option == 2:
            file_out = file_in.replace(".obj", ".aem")
            if os.path.exists(file_out) and Convert_existing_models == True:
                os.remove(file_out)
            if file_in.endswith('.obj'):
                try:
                    print('Converting', os.path.basename(file_in))
                    convert_obj_to_aem(file_in)
                except Exception as e:
                    print("An unexpected error occurred:", e)


def ask_multiple_files(Convert_existing_models):
    root_dir = input('Please input the root path (the location where all files below get converted): ')

    file_in_paths = []
    for dir_path, dir_names, file_names in os.walk(root_dir):
        for file_name in file_names:
            file_path = os.path.join(dir_path, file_name)
            file_in_paths.append(file_path)

    error_files = []
    for file_in in file_in_paths:
        if file_in.endswith('.aem') and option == 1:
            file_out = file_in.replace(".aem", ".obj")
            if os.path.exists(file_out) and Convert_existing_models == True:
                os.remove(file_out)
                try:
                    print('Converting', os.path.relpath(file_in, root_dir))
                    convert_aem_to_obj(file_in)
                except Exception as e:
                    error_files.append(os.path.relpath(file_in, root_dir))
                    print("An unexpected error occurred with file:", os.path.relpath(file_in, root_dir))
            # elif os.path.exists(file_out) and Convert_existing_models == False:
            #    print(file_in + 'alredy converted')
            elif not os.path.exists(file_out):
                try:
                    print('Converting', os.path.relpath(file_in, root_dir))
                    convert_aem_to_obj(file_in)
                except Exception as e:
                    error_files.append(os.path.relpath(file_in, root_dir))
                    print("An unexpected error occurred with file:", os.path.relpath(file_in, root_dir))

        if file_in.endswith('.obj') and option == 2:
            file_out = file_in.replace(".obj", ".aem")
            if os.path.exists(file_out) and Convert_existing_models == True:
                os.remove(file_out)
                try:
                    print('Converting', os.path.relpath(file_in, root_dir))
                    convert_obj_to_aem(file_in)
                except Exception as e:
                    error_files.append(os.path.relpath(file_in, root_dir))
                    print("An unexpected error occurred with file:", os.path.relpath(file_in, root_dir))
            # elif os.path.exists(file_out) and Convert_existing_models == False:
            #    print(file_in + 'alredy converted')
            elif not os.path.exists(file_out):
                try:
                    print('Converting', os.path.relpath(file_in, root_dir))
                    convert_obj_to_aem(file_in)
                except Exception as e:
                    error_files.append(os.path.relpath(file_in, root_dir))
                    print("An unexpected error occurred with file:", os.path.relpath(file_in, root_dir))

    print("Finished converting. Errors encountered in the following files:")
    for i in error_files:
        print(i)
    print('Error in list format:', error_files)


def convert_aem_to_obj(file_in):
    file_out = file_in.replace(".aem", ".obj")
    file_aem = open(file_in, 'rb')
    file_obj = open(file_out, 'a')
    file_aem.seek(24)
    v_num = struct.unpack("H", file_aem.read(2))[0]
    s = '# Vertices ' + str(v_num) + '\n'
    file_obj.write(s)
    print('\n', '# Vertices', v_num)
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
    print('\n', 'Done', '\n')


def convert_obj_to_aem(file_in):
    file_out = file_in.replace(".obj", ".aem")
    file_header = open('header.bin', 'rb')
    header = file_header.read(24)
    file_obj = open(file_in, 'r')
    file_aem = open(file_out, 'ab')
    file_aem.write(header)
    file_read = file_obj.readlines()
    v_x = []
    v_y = []
    v_z = []
    vt_x = []
    vt_y = []
    vn_x = []
    vn_y = []
    vn_z = []
    v_id = []
    vt_id = []
    vn_id = []
    print('\n', 'Analyzing obj file...')
    for i in tqdm(range(len(file_read))):
        if file_read[i][0] == 'v' and file_read[i][1] == ' ':
            v_x.append(float32(file_read[i].split()[1]))
            v_y.append(float32(file_read[i].split()[2]))
            v_z.append(float32(file_read[i].split()[3]))
        elif file_read[i][0] == 'v' and file_read[i][1] == 't':
            vt_x.append(float32(file_read[i].split()[1]))
            vt_y.append(float32(file_read[i].split()[2]))
        elif file_read[i][0] == 'v' and file_read[i][1] == 'n':
            vn_x.append(float32(file_read[i].split()[1]))
            vn_y.append(float32(file_read[i].split()[2]))
            vn_z.append(float32(file_read[i].split()[3]))
        elif file_read[i][0] == 'f':
            for j in range(3):
                v_id.append(ushort(file_read[i].split()[j + 1].split('/')[0]) - 1)
                vt_id.append(ushort(file_read[i].split()[j + 1].split('/')[1]) - 1)
                vn_id.append(ushort(file_read[i].split()[j + 1].split('/')[2]) - 1)
    if v_x and vt_x and vn_x and v_id and len(vt_id) == len(v_id) and len(vn_id) == len(v_id) and len(v_id) < 65536:
        v_num = ushort(len(v_id))
        file_aem.write(struct.pack("H", v_num))
        print('\n', '# Faces', v_num // 3)
        for i in tqdm(range(v_num)):
            file_aem.write(struct.pack("H", ushort(i)))
        file_aem.write(struct.pack("H", v_num))
        print('\n', '# Vertices', v_num)
        for i in tqdm(range(v_num)):
            file_aem.write(struct.pack("f", v_x[v_id[i]]))
            file_aem.write(struct.pack("f", v_y[v_id[i]]))
            file_aem.write(struct.pack("f", v_z[v_id[i]]))
        print('\n', '# UVs', v_num)
        for i in tqdm(range(v_num)):
            file_aem.write(struct.pack("f", vt_x[vt_id[i]]))
            file_aem.write(struct.pack("f", vt_y[vt_id[i]]))
        print('\n', '# Normals', v_num)
        for i in tqdm(range(v_num)):
            file_aem.write(struct.pack("f", vn_x[vn_id[i]]))
            file_aem.write(struct.pack("f", vn_y[vn_id[i]]))
            file_aem.write(struct.pack("f", vn_z[vn_id[i]]))
    elif len(v_id) > 65535:
        print('\n', 'Error: Too many vertices to convert, please use low-poly model')
    else:
        print('\n', 'Error: UVs or Normals data lost. Please check obj file')

    header = file_header.read(56)
    file_aem.write(header)
    file_header.close()
    file_aem.close()
    file_obj.close()
    print('\n', 'Done', '\n')


if __name__ == '__main__':
    global option
    while True:
        option = int(input("Please choose the feature ( 0.exit | 1.aem2obj | 2.obj2aem ): "))
        if not option:
            break
        select_file()