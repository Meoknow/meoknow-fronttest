import minium as mini

class CommentTest(mini.MiniTest):
    #测试评论区加载失败时能否保留原有评论
    def test_comment_loadfail(self):
        self.app.switch_tab("/pages/book/book")
        self.page.wait_data_contains(["PageBook"])
        item=self.page.get_element(".neko-list")
        item.click()
        self.page.wait_data_contains("activeIndex")
        item=self.page.get_element(".weui-navbar__item",inner_text="评论区")
        item.click()

        page=self.app.get_current_page()
        last=len(page.data.commentInfo.list)#第一次评论数量
        mock_request={"data":{"code":1}}
        #加载更多页面失败
        self.app.mock_wx_method("request",result=mock_request,success=True)
        self.page.call_method("scrollToLower",{"check":"这个参数是没用的"})
        self.page.wait_data_contains(["KEYTHATSHOULDNOTBEUSED"],2)#因为这个key是不存在的，所以就是wait 2s
        page=self.app.get_current_page()#2s后评论数量
        self.assertEqual(last,len(page.data.commentInfo.list),"评论区loadfail测试成功")
        self.app.restore_wx_method("request")
    #测试评论区加载更多评论能否正常工作，这需要假设图鉴中第一只猫的评论至少有2页
    def test_comment_loadMore(self):
        self.app.switch_tab("/pages/book/book")
        self.page.wait_data_contains(["PageBook"])
        item=self.page.get_element(".neko-list")
        item.click()
        self.page.wait_data_contains("activeIndex")
        item=self.page.get_element(".weui-navbar__item",inner_text="评论区")
        item.click()

        page=self.app.get_current_page()
        last=len(page.data.commentInfo.list)#第一次评论数量
        self.page.call_method("scrollToLower",{"check":"这个参数是没用的"})
        self.page.wait_data_contains(["KEYTHATSHOULDNOTBEUSED"],2)#因为这个key是不存在的，所以就是wait 2s
        page=self.app.get_current_page()#2s后评论数量
        self.assertNotEqual(last,len(page.data.commentInfo.list),"评论区loadmore测试成功")
    #测试评论区加载不出更多时会不会正确设置noMore标志
    def test_comment_noMore(self):
        self.app.switch_tab("/pages/book/book")
        self.page.wait_data_contains(["PageBook"])
        item=self.page.get_element(".neko-list")
        item.click()
        self.page.wait_data_contains("activeIndex")
        item=self.page.get_element(".weui-navbar__item",inner_text="评论区")
        item.click()

        mock_request={"msg":"","data":{"code":0,"data":{"comments":[]}}}
        self.app.mock_wx_method("request",result=mock_request,success=True)#mock让评论区获取更多评论返回空，则判断评论读取完了
        self.page.call_method("scrollToLower",{"check":"这个参数是没用的"})
        self.page.wait_data_contains(["KEYTHATSHOULDNOTBEUSED"],2)
        self.app.restore_wx_method("request")

        page=self.app.get_current_page()#检查noMore字段是否成功设置为1
        self.assertEqual(1,page.data.noMore,"评论区noMore测试成功")
    #测试发布评论功能能否正常工作，评论区字数能否正常显示
    def test_comment_publish(self):
        self.app.switch_tab("/pages/book/book")
        self.page.wait_data_contains(["KEYTHATSHOULDNOTBEUSED"],10)
        self.page.wait_data_contains(["PageBook"])
        item=self.page.get_element(".neko-list")
        item.click()
        self.page.wait_data_contains("activeIndex")
        item=self.page.get_element(".weui-navbar__item",inner_text="评论区")
        item.click()

        #mock掉request，返回一个mock好的用户信息
        mock_request={"userInfo":{"nickName":"高脚","avatarUrl":"https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIp8hByeW0tsKw3sCYAGR0mRakxXbum45YgicZzGVw43ibb1Iib2FDZeXIF2Yib4qNjClRwM0VsPOcWuQ/132"}}
        self.app.mock_wx_method("getUserProfile",result=mock_request,success=True)
        #给一个虚假的授权
        self.page.call_method("getUserProfile",{"check":"这个参数没有用"})
        #授权成功并发出request给服务器后重置mock
        self.app.restore_wx_method("getUserProfile")

        #打开发布评论区域
        button_enter=self.page.get_element(".commentmut .top-title .write-comment",inner_text="写评论")
        button_enter.click()

        #写评论
        content="这是一条由自动化框架发出的评论"
        #由于无法直接对输入栏进行操作，这里直接调用inputs函数对后台数据进行表单操作
        self.page.call_method("inputs",{"detail":{"value":content}})
        self.page.wait_data_contains(["KEYTHATSHOULDNOTBEUSED"],2)
        #由于提交表单操作要利用视图层的表单单元进行传参，因此这里只是测试后台的数据对不对
        self.assertEqual(len(content),self.page.data.currentWordNumber,"评论长度测试正确")
        
        #记录当前评论区总评论数量
        last=self.page.data.commentInfo.num

        #发布评论
        #同样，由于提交表单要用视图层信息，这里直接调用我们的表单提交并提交我们的评论
        self.page.call_method("formSubmit",{"detail":{"value":{"pic":0,"content":content}}})
        self.page.wait_data_contains(["KEYTHATSHOULDNOTBEUSED"],2)
        now=self.page.data.commentInfo.num
        self.assertEqual(last+1,now,"评论区发布评论成功")
    