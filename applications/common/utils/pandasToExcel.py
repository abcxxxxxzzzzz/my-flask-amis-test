import pandas as pd



# 创建 EXCEL
def create_form(excel_header,excel_file_name):
    # pass
    form_header = excel_header
    df = pd.DataFrame(columns=form_header)
    df.to_excel(excel_file_name, index=False)

# 写入数据到 EXCEL
def add_info_to_form(excel_file_name, data=[]):
    df = pd.read_excel(excel_file_name)
    row_index = len(df) + 1  # 当前excel内容有几行
    df.loc[row_index] = data
    df.to_excel(excel_file_name,index=False)