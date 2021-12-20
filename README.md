利用minitest -s config.py -g来运行测试用例并生成报告，测试用例命名规则在config中说明，首先用pkg匹配包名，再用case_list匹配测试类名，采用的是通配符匹配，因此包名需要以test结尾，测试类需要以test_开头

生成报告之后，在对应的目录下面有index.html文件，但是我们不能直接用浏览器打开这个 文件，需要把这个目录放到一个静态服务器上。以下方式都是可行的:

    本地执行python3 -m http.server 8080 -d /path/to/dir/of/report，然后浏览器输入:http://localhost:8080/

    PS: 其中/path/to/dir/of/report为上文的output_path