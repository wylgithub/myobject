define([
    'require',
    'jquery',
    'backbone',
    'validate'
], function (require, $, Backbone) {
    "use strict";

    return Backbone.View.extend({
        el: "body",
        in_syncing: false,  //防止两重提交标志位

        events: {
            'click #btnReg': 'register',
            'click #pactLink': 'pactShow',
            'click #changeCaptcha': 'changeCaptcha'
        },

        initValidator: function () {


            return $("#regForm").validate({
                //设置验证规则
                rules: {
                    "username": {
                        required: true,
                        userNameCheck: true
                    },
                    "password": {
                        required: true,
                        rangelength: [6, 22]
                    },
                    "passwordagain": {
                        required: true,
                        rangelength: [6, 22],
                        equalTo: "#txtPassword"
                    },
                    "mobile": {
                        required: true,
                        isMobile: true
                    },
                    "email": {
                        required: true,
                        isEmail: true
                    },
                    "captcha_1": {
                        required: true
                    }

                },
                //设置错误信息
                messages: {
                    "username": {
                        required: "请输入用户名",
                        userNameCheck: "请输入4-20位字母开头的数字、字母、下划线"
                    },
                    "password": {
                        required: "请输入密码",
                        rangelength: "密码长度为6-22位"
                    },
                    "passwordagain": {
                        required: "请再次输入密码",
                        rangelength: "密码长度为6-22位",
                        equalTo: "两次输入密码不相同"
                    },
                    "mobile": {
                        required: "请务必输入有效的手机号码",
                        isMobile: "请务必输入有效的手机号码"
                    },
                    "email": {
                        required: "请输入有效的邮箱地址",
                        isEmail: "请输入有效的邮箱地址"
                    },
                    "captcha_1": {
                        required: "请输入验证码"
                    }
                },
                tip: "tipinfo_reg"
            });
        },

        register: function () {

            $(".tipinfo_reg").html("");
            $(".error_reg").html("");

            if (!$("#checkbox").prop("checked")) {
                alert("请仔细阅读协议，并勾选同意选择框。");
                return;
            }

            $("#regForm").trimForm("regForm");

            if (!this.initValidator()) {
                return;
            }

            //防止两重提交
            if (this.in_syncing) {
                return;
            }
            this.in_syncing = true;

            $('#btnReg').prop('disabled', true);

            $('#regForm').submit();

        },

        pactShow: function () {

            if ($("#pactDiv").css("display") === "block") {

                $("#pactDiv").hide();

            } else {

                $("#pactDiv").show();
            }

        },
        changeCaptcha: function () {
            $.post('/account/register/captcha/'.auto_fix_root_url(), {
                old_key: $("#id_captcha_0").val()
            }, function (data) {
                $("#id_captcha_0").val(data.key);
                $(".captcha").attr("src", ("/captcha/image/" + data.key + "/").auto_fix_root_url());
            });
        }
    });
});