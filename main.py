import os
from tqdm import tqdm
import struct
from numpy import float32


def select_file():
    option = int(input("Please choose the feature ( 1.aem2obj | 2.obj2aem ): "))
    # option = 1
    if option == 1:

        while True:
            Converete_existing_models_yn = input('do you want to override existing obj files?(override/n)')
            if Converete_existing_models_yn == 'override':
                Converete_existing_models = True
                break
            elif Converete_existing_models_yn == 'n':
                Converete_existing_models = False
                break
            else:
                print("Invalid input, please enter either 'override' or 'n'.")



        while True:
            one_or_multible = int(input('do u waant to convert 1 file or multible files? (1/2)'))
            if one_or_multible == 1:
                ask_one_file(Converete_existing_models)
                break
            elif one_or_multible == 2:
                ask_multible_files(Converete_existing_models)
                break
            else:
                print("Invalid input, please enter either 1 or 2.")


    if option == 2:
        print('Obj2aem is not supported yet, please wait...')
        input()




def ask_one_file(Converete_existing_models):

        file_in = input("Please input the path of the file to be converted(Press Enter to exit):")
            
        if file_in.endswith('.aem') or file_in.endswith('.obj'):
            file_out = file_in.replace(".aem", ".obj")
            if os.path.exists(file_out) and Converete_existing_models == True:
                os.remove(file_out)
            if file_in.endswith('.aem'):
                try:
                    print('converting'+file_in)
                    convert_aem_to_obj(file_in)
                except Exception as e:
                    print("An unexpected error occurred:", e)



def ask_multible_files(Converete_existing_models):
        root_dir = input('imput the root path (the location wher all files below get converted)')

        file_in_paths = []
        error_files = []
        for dir_path, dir_names, file_names in os.walk(root_dir):
            for file_name in file_names:
                file_path = os.path.join(dir_path, file_name)
                file_in_paths.append(file_path)

        for file_in in file_in_paths:
            if file_in.endswith('.aem'):
                file_out = file_in.replace(".aem", ".obj")
                if os.path.exists(file_out) and Converete_existing_models == True:
                    os.remove(file_out)
                    try:
                        print('converting'+file_in)
                        convert_aem_to_obj(file_in)
                    except Exception as e:
                        print("An unexpected error occurred:", e)
                        error_files.append(file_in)
                #elif os.path.exists(file_out) and Converete_existing_models == False:
                #    print(file_in + 'alredy converted')
                elif not os.path.exists(file_out):
                    try:
                        print('converting'+file_in)
                        convert_aem_to_obj(file_in)
                    except Exception as e:
                        print("An unexpected error occurred:", e)
                        error_files.append(file_in)

        print("The following files caused errors:", error_files)

    



def convert_aem_to_obj(file_in):
        file_out = file_in.replace(".aem", ".obj")
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




if __name__ == '__main__':
    select_file()
