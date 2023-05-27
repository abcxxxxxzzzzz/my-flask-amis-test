
def fHideMid(str,count=4,fix='*'):
    """
       #隐藏/脱敏 中间几位
       str 字符串
       count 隐藏位数
       fix 替换符号
    """
    if not str:return ''
    count =int(count)
    str_len=len(str)
    ret_str=''
    if str_len ==1 :
        return str
    elif str_len ==2:
        ret_str = str[0] + '*'
    elif count ==1:
        mid_pos = int(str_len/2)
        ret_str = str[:mid_pos] +fix +str[mid_pos+1:]
    else:
        if str_len-2 > count:
            if count%2 ==0:
                if str_len%2 == 0:
                    ret_str = str[:int(str_len/2- count/2)] + count*fix + str[int(str_len/2 + count/2):]
                else:
                    ret_str = str[:int((str_len+1)/2- count/2)] + count*fix + str[int((str_len+1)/2 + count/2):]
            else:
                if str_len%2 == 0:
                   ret_str = str[:int(str_len/2- (count-1)/2)] + count*fix + str[int(str_len/2 + (count+1)/2):]
                else:
                   ret_str = str[:int((str_len+1)/2- (count+1)/2)] + count*fix + str[int((str_len+1)/2 + (count-1)/2):]
        else:
            ret_str = str[0] +fix*(str_len-2) +str[-1]
 
    return ret_str







# fHideMid(str,count=11,fix='*')   银行卡隐藏: 6222***********7790
# fHideMid(str,count=3,fix='*'):   手机号码： 1857***6508