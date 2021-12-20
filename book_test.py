import minium as mini

class BookTest(mini.MiniTest):
    def test_navigate(self):
        self.app.switch_tab("/pages/book/book")
        item=self.page.get_element(".neko-list")
        item.click()
        self.page.wait_data_contains("activeIndex")
        page=self.app.get_current_page()
        item=page.path
        self.assertIn("detail",item,msg="测试信息:图鉴路由成功")

    def test_tab_switch(self):
        self.app.switch_tab("/pages/book/book")
        item=self.page.get_element(".neko-list")
        item.click()
        self.page.wait_data_contains("activeIndex")
        page=self.app.get_current_page()
        item=page.path
        self.assertIn("detail",item)
        item1=self.page.get_element(".weui-navbar__item",inner_text="评论区")
        item1.click()
        self.assertEqual(1,page.data.activeIndex,"测试信息:切换到评论区成功")
        item0=self.page.get_element(".weui-navbar__item",inner_text="图鉴")
        item0.click()
        self.assertEqual(0,page.data.activeIndex,"测试信息:测试切换回图鉴成功")
        
    