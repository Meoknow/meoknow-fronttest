import minium as mini

class BookTest(mini.MiniTest):
    
    #测试图鉴能否正确路由到单只图鉴，图鉴信息是否正确渲染
    def test_navigate(self):
        self.app.switch_tab("/pages/book/book")
        self.page.wait_data_contains(["PageBook"])
        item=self.page.get_element(".neko-list")
        item.click()#点击单只猫图鉴
        self.page.wait_data_contains("activeIndex")#等待图鉴加载，用page.data的key判断
        page=self.app.get_current_page()
        item=page.path
        self.assertIn("detail",item,msg="测试信息:图鉴路由成功")
        item=self.page.get_elements(".text .list")
        self.assertEqual(5,len(item),msg="图鉴信息正确显示")

    #测试图鉴和评论区能否正确切换
    def test_tab_switch(self):
        self.app.switch_tab("/pages/book/book")
        self.page.wait_data_contains(["PageBook"])
        item=self.page.get_element(".neko-list")
        item.click()
        self.page.wait_data_contains("activeIndex")
        page=self.app.get_current_page()
        item1=self.page.get_element(".weui-navbar__item",inner_text="评论区")
        item1.click()
        self.assertEqual(1,page.data.activeIndex,"测试信息:切换到评论区成功")
        item0=self.page.get_element(".weui-navbar__item",inner_text="图鉴")
        item0.click()
        self.assertEqual(0,page.data.activeIndex,"测试信息:测试切换回图鉴成功")
    