import minium as mini

class RecognizeTest(mini.MiniTest):
    def test_postImg_request_fail(self):
        self.page.call_method("postMyImg",{"myBase64Img":"invalid token"})
        self.page.wait_data_contains(["loadingfail"])
        page=self.app.get_current_page()
        item=page.data.loadingText
        self.assertIn("识别出错",item,"测试信息:postImg函数请求失败测试成功")


    def test_recognize_success(self):
        self.page.call_method("postMyImg",{"myBase64Img":"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAEnQAABJ0Ad5mH3gAAAC2SURBVFhH7ZfLDYAgEETRprzagDVRlA14tSrNGImG4LK7fDzAS4yc2DcjJjpYaw/zI+N9/40u0I7Ati/X5VO1gXla79VDFQEkDw0HxQVCtb+p0sBXelBUgKreUUyAMxwUEeAOB1XOAEV2AUl6QArEXiEf6XBACmAzbCoVkRB9BC5RTEKTHrDOAFdCA/sQUum06QFbAGCI30JqKyIBEJLQpgfqr2InkTIciBvITf8v6AJdoHUBY059v0FeUOwe3gAAAABJRU5ErkJggg=="})
        self.page.wait_data_contains(["rescats","userimage"])
        page=self.app.get_current_page()
        self.assertIn("reply",page.path,"测试信息:识图成功后成功跳转到结果页")

    def test_recognize_success_no_cat(self):
        mock_request={"code": 0,"msg": "","data":{}}
        self.app.mock_wx_method("request",mock_request)
        self.page.call_method("postMyImg",{"myBase64Img":"anything because mock"})
        self.page.wait_data_contains(["loadingfail"])
        self.app.restore_wx_method("request")
        page=self.app.get_current_page()
        item=page.data.loadingText
        self.assertIn("识别出错",item,"测试信息:上传图片成功，获取到空的猫列表成功返回无猫")

