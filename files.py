#encoding=utf-8

import os,sys


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


def help_str():
    help_str = '''
    1) 按行处理文件字符替换的函数
    files.py con_line_replace /data/.../file.txt target_str replace_str 
    2)

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
    else:
        print '未知指令: %s' % argv_list[1]   
        print 'files.py help  查看命令列表' 

    #print argv_list


