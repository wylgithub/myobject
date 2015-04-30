define([
    'require',
    'jquery',
    'backbone'
], function (require, $, Backbone) {
    "use strict";

    var AppView = Backbone.View.extend({
        el:"body",
        role:$('#id_role'),
        btnRoleDisplay:$('#btnRoleDisplay'),
        in_syncing:false,  //防止两重提交标志位

        events:{
            'click #btnSave':'save',
            'click .dropdownItem':'dropdownItem_click',
            'click #btnReturn':'return_to_prev_page',
            'click #btnRegister': 'btn_register'
        },

        initialize:function () {

        },

        btn_register:function() {
            //if(!this.check_register(event)){
            //    return;
            //}
            if(this.in_syncing)
            {
                return;
            }
            this.in_syncing = true;
            $('#registerForm').submit();
        },

        //btn_register:function() {
        //    if(!this.check_register(event)){
        //        return;
        //    }
        //
        //    if (this.in_syncing) {
        //        return;
        //    }
        //
        //    var current_view = this;
        //    this.in_syncing = true;
        //    this.options.parentView.trigger('start_ajax_sync');
        //    var form = $('#registerForm');
        //    $.ajax({
        //        type: "POST",
        //        url: form.attr('action'),
        //        data: form.serialize(),
        //        success: function(data){
        //            if (data.error_code > 0) {
        //                window.alert(data.error_msg);
        //            }else {
        //                var validation = Boolean($('#id_validation').val());
        //                //var validation = data.validation;
        //                if (validation === false) {             // 此处有逻辑错误,待修正
        //                    window.alert("恭喜您注册成功！");
        //                }else {
        //                    window.alert("发生未知错误，请联系管理员！");
        //                }
        //            }
        //        },
        //        error: function(){
        //            window.alert('与服务器通讯发生错误，请稍后重试。');
        //        },
        //        complete: function(){
        //            //防止两重提交
        //            //恢复现场
        //            current_view.options.parentView.trigger('finish_ajax_sync');
        //            current_view.in_syncing = false;
        //        }
        //    });
        //    return true;
        //},

        check_register:function(event){
            var username = $('#txtUserName').val();
            var password = $('#txtPassword').val();
            var full_name = $('#txtFullName').val();
            var email = $('#txtEmail').val();
            var check_password = $("#txtPassword_check").val();
            var mobile = $('#txtMobile').val();
            var checkusername=/^[a-zA-Z0-9\u4e00-\u9fa5\_]+$/;

            // 检查用户名是否为空和是否重复
            if(!checkusername.test(username)){
                window.alert("用户名已经存在，或存在非法字符！");
                return false;
            }

            // 检查密码是否正确
            var regs = new RegExp("[u4E00-u9FFF]+","g");
            if (password.length < 6){
                window.alert("密码设置太简单,或者密码包含了汉子!");
                return false;
            }

            // 设置真是姓名的check
            if (full_name.length == 0){
                window.alert("请设置自己的真是姓名!")
            }

            // 检查邮箱的有效性
            if(email == ''){
                //var reg = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((\.[a-zA-Z0-9_-]{2,3}){1,2})$/;
                //var match = /^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/;
                //if(email == ""){
                window.alert("请填写正确的邮箱!");
                    return false;
                //}
            }

            // 检查手机号码的正确性
            if(mobile.length != 11){
                window.alert("请输入正确的手机号码!");
                return false;
            }

            return true;
        },

        save:function() {
            //防止两重提交
            if (this.in_syncing) {
                return;
            }
            this.in_syncing = true;
            $('#btnSave').prop('disabled', true);
            $('#frmAddUser').submit();
        },

        // 返回用户一览
        return_to_prev_page:function() {
            var ru = $('#redirect_url');
            var url;
            if (!ru || ru.length === 0 || !ru.val()) {
                url = '/user_account/login/action/';
            }else {
                url = ru.val();
            }
            window.location.href = url;
        },

        // 选择人员角色
        dropdownItem_click:function(event) {
            var element = $(event.target);
            var source = element.attr('for');
            if (source === 'id_role') {
                this.role.val(element.attr('value'));
                this.btnRoleDisplay.text(element.text());
            }
        }
    });
    return AppView;
});