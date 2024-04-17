xray_ext = ('ogf', 'dm', 'cform', 'details', 'hom', 'wallmarks', 'som')


def stalker_tools_main():
    import os, time
    from stalker_tools import xray_utils
    
    start_time = time.time()
    # в пути ставить двойные слеши
    path = 'X:\\import\\blender_import\\'
    print('\nRUN BATCH X-RAY IMPORT (DIR: {0})\n'.format(path.upper()))
    for file in os.listdir(path):
        ext = file.split('.')[-1]
        if ext in xray_ext:
            print('{: <32}'.format(file), end=' ')
            xray_utils.import_file(path + file)
    finish_time = time.time()
    print('\ntotal time: {:.6}s'.format(finish_time - start_time))


if __name__ == '__main__':
    stalker_tools_main()

