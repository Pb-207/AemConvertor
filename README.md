# AemConvertor
A simple python script to convert .aem to .obj or .obj to .aem. Simply drag a file or path and press enter to start converting. <br><br>
Following features in latest version:<br><br>
Aem2obj: Convert aem file into obj file, including vertices, UVs, normals and faces information. All faces will be isolated due to the data structure of aem files.<br><br>
Obj2aem: Convert obj file into aem file. Vertices, UVs, normals and faces data must be included in obj files to be converted. Aem format doesn't allow more than 65535 vertices in one file. Make sure the obj file to be converted has enough data and not too large to convert before converting.<br>
Warning: There are some unknown bytes in aem file filled with '00' while converting from obj file. This may cause side effects, report if encounter errors.
