import minium as mini

class RecognizeTest(mini.MiniTest):
    #发送正确的图片base64
    def test_recognize_success(self):
        self.page.call_method("postMyImg",{"myBase64Img":"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAEnQAABJ0Ad5mH3gAAAC2SURBVFhH7ZfLDYAgEETRprzagDVRlA14tSrNGImG4LK7fDzAS4yc2DcjJjpYaw/zI+N9/40u0I7Ati/X5VO1gXla79VDFQEkDw0HxQVCtb+p0sBXelBUgKreUUyAMxwUEeAOB1XOAEV2AUl6QArEXiEf6XBACmAzbCoVkRB9BC5RTEKTHrDOAFdCA/sQUum06QFbAGCI30JqKyIBEJLQpgfqr2InkTIciBvITf8v6AJdoHUBY059v0FeUOwe3gAAAABJRU5ErkJggg=="})
        self.page.wait_data_contains(["rescats","userimage"])
        page=self.app.get_current_page()
        self.assertIn("reply",page.path,"测试信息:识图成功后成功跳转到结果页")#检查是否跳转到reply页
    #测试给postMyImg发错误的base64字段，能否显示识别不到猫
    def test_postImg_request_fail(self):
        self.page.call_method("postMyImg",{"myBase64Img":"invalid token"})#调用postMyImg函数
        self.page.wait_data_contains(["loadingfail"])#检查page loadingfail字段是否置为1
        page=self.app.get_current_page()
        item=page.data.loadingText
        self.assertIn("识别出错",item,"测试信息:postImg函数请求失败测试成功")
    #测试识图成功但服务端返回无猫时能否正常显示
    def test_recognize_success_no_cat(self):
        mock_request={"statusCode":200,"data":{"code": 0,"msg": "","data":{"cats":[]}}}#mock请求让返回的猫咪数为0，但是是识图成功的状态
        self.app.mock_wx_method("request",result=mock_request,success=True)
        self.page.call_method("postMyImg",{"myBase64Img":"anything because mock"})
        self.page.wait_data_contains(["loadingfail"])#检查loadingfail是否置为1
        self.app.restore_wx_method("request")
        page=self.app.get_current_page()
        item=page.data.loadingText
        self.assertIn("识别出错",item,"测试信息:上传图片成功，获取到空的猫列表成功返回无猫")
