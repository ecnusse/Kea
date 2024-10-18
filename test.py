import inspect
import random

def main_path():
    def accept(f):
        def mainpath_wrapper(*args, **kwargs):
            # 获取函数的源代码
            source_code = inspect.getsource(f)
            # 将源代码分割成行，并去掉空行和缩进
            code_lines = [line.strip() for line in source_code.splitlines() if line.strip()]
            # 将代码行转换为字符串形式
            code_lines = [line for line in code_lines if not line.startswith('def ') and not line.startswith('@') and not line.startswith('#')]
            # print(code_lines)
            # f(*args, **kwargs)
            return code_lines

        return mainpath_wrapper

    return accept

@main_path()
def test_main():
    count = 1
    print("count: " + str(count))
    index = random.randint(0, count - 1)
    print("index: " + str(index))
    # selected_file = d(resourceId="com.amaze.filemanager:id/firstline")[index]
    selected_file_name = 1
    print("selected file name: " + str(selected_file_name))

code_lines = test_main()
print(code_lines)
# # 计算当前要执行的行数
# lines_to_execute = len(code_lines)
# # 执行当前需要执行的行
# for i in range(lines_to_execute):
#     exec(code_lines[i])