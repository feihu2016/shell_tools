#encoding=utf-8

''' 使用说明
    1) 按行处理文件字符替换的函数
      files.py con_line_replace /data/.../file.txt target_str replace_str 
    2)等字节文本替换函数(注意：target_str的字节数需要等于replace_str)
      files.py mmap_replace /data/.../file.txt target_str replace_str 
    3)特征字符查找,mod参数可以不写，默认为0，表示返回位置列表和匹配次数；为1表示只返回匹配次数
      file.py mmap_find /data/.../file.txt find_str mod
'''

import os,sys
import mmap

#按行处理文件字符替换的函数
def con_line_replace(filename, old_str, new_str):
    #文件不存在，直接返回
    if not os.path.exists(filename):
        return '%s  ,not find!' % filename
    
    #分解文件目录和文件名称
    path_split = list(os.path.split(filename))
    
    if not path_split[0] or '.' == path_split[0]:
        path_split[0] = os.getcwd()

    filename_tmp = filename + '.tmp'
    os.rename(filename, filename_tmp)
    
    #逐行读取内容并将replace结果，写入原文件
    n,m = 1,1
    with open(filename_tmp, 'r') as tmpfile:
        datafile = open(filename, 'w+')
        for oldline in tmpfile:
            newline = oldline.replace(old_str, new_str)
            datafile.write(newline)
            n += 1
            m += 1
            #每100行写入一次文件
            if n>100:
                datafile.flush()
                n = 1
        datafile.close()

    #清除临时文件
    os.remove(filename_tmp)
    return '合计处理：%s 行' % m

#等字节文本替换函数
def mmap_replace(filename, old_str, new_str):
    #文件不存在，直接返回
    if not os.path.exists(filename):
        return '%s  ,not find!' % filename

    #文件不存在，直接返回
    if len(old_str) != len(new_str):
        return '替换与被替换字符长度不等！'
    
    #使用mmap查找并替换字符
    open_file = open(filename,'r+')
    mmap_file = mmap.mmap(open_file.fileno(),0,access=mmap.ACCESS_WRITE)  
    replace_num = 0
    find_index = mmap_file.find(old_str)
    while find_index > 0:
        mmap_file[find_index:find_index+len(old_str)] = new_str
        mmap_file.flush()
        mmap_file.seek(find_index+len(old_str))
        find_index = mmap_file.find(old_str)
        replace_num += 1

    #关闭文件，并返回处理结果
    mmap_file.close()
    open_file.close()
    return '合计替换：%s 次' % replace_num

#查找特征文本函数
def mmap_find(filename, find_str, mod = 0):
    #文件不存在，直接返回
    if not os.path.exists(filename):
        return '%s  ,not find!' % filename
    
    #使用mmap查找并替换字符
    open_file = open(filename,'r+')
    mmap_file = mmap.mmap(open_file.fileno(),0,access=mmap.ACCESS_WRITE)  
    find_list = [0]
    find_index = mmap_file.find(find_str)
    while find_index > 0:
        if mod == 1:
            find_list[0] += 1
        else:
            find_list.append(find_index)
        mmap_file.seek(find_index+len(find_str))
        find_index = mmap_file.find(find_str)

    #关闭文件，并返回处理结果
    mmap_file.close()
    open_file.close()
    if mod == 1:
        return '合计找到匹配：%s 次' % find_list[0]
    else:
        return_str = '|'.join(map(lambda x:str(x),find_list))
        stat_str = '\n合计找到匹配：%s 次' % str(len(find_list)-1)
        return return_str + stat_str 

def help_str():
    help_str = '''
    1) 按行处理文件字符替换的函数
      files.py con_line_replace /data/.../file.txt target_str replace_str 
    2)等字节文本替换函数(注意：target_str的字节数需要等于replace_str)
      files.py mmap_replace /data/.../file.txt target_str replace_str 
    3)特征字符查找,mod参数可以不写，默认为0，表示返回位置列表和匹配次数；为1表示只返回匹配次数
      file.py mmap_find /data/.../file.txt find_str mod
     
    '''
    print(help_str)

if __name__ == '__main__':
    argv_list = sys.argv
    #至少两个参数
    if len(argv_list)<2:
        print '缺少参数！'
        exit()

    if argv_list[1] == 'help':
        help_str() 
    elif argv_list[1] == 'con_line_replace':
        if len(argv_list) == 5:
             print con_line_replace(argv_list[2], argv_list[3], argv_list[4])
        else:
             print 'con_line_replace 命令，参数不足！'
    elif argv_list[1] == 'mmap_replace':
        if len(argv_list) == 5:
             print mmap_replace(argv_list[2], argv_list[3], argv_list[4])
        else:
             print 'con_line_replace 命令，参数不足！'
    elif argv_list[1] == 'mmap_find':
        if len(argv_list) == 5:
             print mmap_find(argv_list[2], argv_list[3], int(argv_list[4]))
        else:
             print mmap_find(argv_list[2], argv_list[3])
    else:
        print '未知指令: %s' % argv_list[1]   
        print 'files.py help  查看命令列表' 

    #print argv_list


