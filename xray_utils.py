import struct, os, time
from stalker_tools import xray_import


def unpack_data(format, data, position=0):
    data_size = struct.calcsize(format)
    unpack_data = struct.unpack(format, data[position : position + data_size])
    if len(unpack_data) == 1:
        unpack_data = unpack_data[0]
    position += data_size
    return unpack_data, position


def read_bin_file(file_name, file_ext='', file_path=''):
    '''
    Возвращает данные (bytes) из бинарного файла.
    Использование: read_bin_file(file_name, file_ext, file_path)
      file_name - имя файла (str)
      file_ext - расширение файла (str, default='')
      file_path - путь к файлу (str, default='')
    '''
    # проверка на наличие слеша в конце пути
    if len(file_path) != 0:
        if file_path[-1] != '\\':
            file_path = file_path + '\\'
    # проверка на наличие точки в расширении
    if len(file_ext) != 0:
        if file_ext[0] != '.':
            file_ext = '.' + file_ext
        _absolute_path = file_path + file_name + file_ext
    else:
        _absolute_path = file_path + file_name
    try:
        _file = open(_absolute_path, 'rb')
        file_data = _file.read()
        _file.close()
    except:
        print(' ! CANNOT OPEN FILE: {}'.format(_absolute_path))
        file_data = b''
    return file_data


def read_block(position, data):
    '''
    Возвращает позицию считывания из данных, идентификатор блока, размер блока.
    Использование: read_block(position, data)
      position - позиция начала считывания (int)
      data - данные (bytes)
    '''
    block_id = struct.unpack('I', data[position : position + 4])[0]
    position += 4
    
    block_size = struct.unpack('I', data[position : position + 4])[0]
    position += 4
    
    return position, block_id, block_size


def parse_string_nul(data, position):
    '''
    Возвращает распакованную из данных строку и индекс конца строки.
    Использование: parse_string_nul(data, position)
      data - данные (bytes)
      position - индекс начала строки (int)
    '''
    string = ''
    _char = struct.unpack('B', data[position : position + 1])[0]
    position += 1
    while _char != 0:
        string = string + chr(_char)
        _char = struct.unpack('B', data[position : position + 1])[0]
        position += 1
    return string, position


def parse_date(data, position):
    date, position = unpack_data('I', data, position)
    return time.ctime(date), position


def print_bytes(data, column_count=16):
    '''
    Печатает байты в консоль в удобочитаемом виде.
    Использование: print_bytes(data, column_count)
      data - данные (bytes)
      column_count - количество печатаемых столбцов (default=16, int(1-16))
    '''
    _data_bytes = struct.unpack('%dB' % len(data), data)
    _column = 1
    if column_count < 1 or column_count > 16:
        column_count = 16
    for _byte in _data_bytes:
        if _column % column_count != 0:
            print('{0: ^4}'.format(hex(_byte)), end=' ')
            _column += 1
        else:
            print(hex(_byte))
            _column += 1
    print()
    return 'FINISHED'


def copy_files(path, files, ext, new_path, copy_bump):
    '''
    Копирует файлы
    Использование: copy_files(path, files, ext, new_path, copy_bump)
    '''


    def _copy_file(_path, _file_name, _ext, _new_path):
        _file = open(_path + _file_name + _ext, 'rb')
        _file_data = _file.read()
        _file.close()
        _new_file = open(_new_path + _file_name + _ext, 'wb')
        _new_file.write(_file_data)
        _new_file.close()


    _list_dir = {}
    for _file_name in files:
        _list_dir[new_path + _file_name.split('\\')[0]] = True
    _list_dir = list(_list_dir.keys())
    _list_dir.sort()
    if not os.access(new_path, os.F_OK):
        os.makedirs(new_path)
    for _dir in _list_dir:
        try:
            os.mkdir(_dir)
        except:
            print(' ! CANNOT CREATE DIRECTORY:', _dir)
    for _file_name in files:
        try:
            _copy_file(path, _file_name, ext, new_path)
            if os.access(path+_file_name+'_bump'+ext, os.F_OK) and copy_bump:
                _copy_file(path, _file_name+'_bump', ext, new_path)
            if os.access(path+_file_name+'_bump#'+ext, os.F_OK) and copy_bump:
                _copy_file(path, _file_name+'_bump#', ext, new_path)
        except:
            print(' ! CANNOT COPY FILE:', path+_file_name+ext)


def parse_file(file_data, ext):
    if ext == 'cform':
        from stalker_tools import parse_cform
        mesh_data = parse_cform.parse_cform(file_data)
        return mesh_data
    elif ext == 'details':
        from stalker_tools import parse_details
        mesh_data = parse_details.details_data_parse(file_data)
        return None
    elif ext == 'dm':
        from stalker_tools import parse_dm
        mesh_data = parse_dm.parse_main(file_data)
        return mesh_data
    elif ext == 'hom':
        from stalker_tools import parse_hom
        mesh_data = parse_hom.hom_data_parse(file_data)
        return mesh_data
    elif ext == 'wallmarks':
        from stalker_tools import parse_wallmarks
        mesh_data = parse_wallmarks.parse_main(file_data)
        return None
    elif ext == 'ogf':
        from stalker_tools import parse_ogf
        mesh_data = parse_ogf.ogf_data_parse(file_data)
        return None
    elif ext == 'som':
        from stalker_tools import parse_som
        mesh_data = parse_som.parse_main(file_data)
        return mesh_data


def import_file(absolute_path):
    start_time = time.time()
    ext = absolute_path.split('.')[-1]
    name = absolute_path.split('\\')[-1][0 : -(len(ext)+1)]
    path = absolute_path[:-(len(name) + len(ext) + 1)]
    file_data = read_bin_file(name, ext, path)
    mesh_data = parse_file(file_data, ext)
    if mesh_data:
        xray_import.crete_mesh(mesh_data)
    finish_time = time.time()
    print('{:.6}s'.format(finish_time-start_time))

