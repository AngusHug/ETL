import os
import re
class Add_fo:
    def traverse_sh(self, current_dir):
        file_list = os.listdir(current_dir)
        for file in file_list:
            file_path = os.path.join(current_dir, file)
            print(file_path)
        #file_path = "D:\python_Course\doc/traffic_sh\ETC.bash"
            if os.path.isfile(file_path):
                f = open(file_path, "r+", encoding='utf-8')
                content = re.sub("f_no	string	'文件号分区'", "f_no	string	comment'文件号分区'", f.read())
                '''
                file_new = re.sub('from', '\t ,f_no \nfrom', f.read())
                content = re.sub("the_date\s+string\s+comment\s?'业务日期分区yyyyMMdd'",
                        "the_date string comment'业务日期分区yyyyMMdd',\r\t f_no	string	'文件号分区'",
                                file_new)
                content = re.sub("the_date string	comment'数据处理时间'",
                             "\n\tthe_date string comment'业务日期分区yyyyMMdd'\n\t f_no	string	'文件号分区'",content)
                content = re.sub("the_date\)", "the_date,f_no)", content)
                '''
                f.seek(0)
                f.truncate()
                f.write(content)
                print(file_path, "Done")
            else:
                print("Check It")
res = Add_fo()
res.traverse_sh("D:\python_Course\doc/traffic_sh")