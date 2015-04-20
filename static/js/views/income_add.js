define([
    'require',
    'jquery',
    'backbone',
    'datepicker',
    'datetimepicker',
    'datepicker',
    'datetimepickerCN',
    //'jqueryuiprogressbar'
], function (require, $, Backbone) {
    "use strict";

    var AppView = Backbone.View.extend({
        el:"body",
        in_syncing:false,  //防止两重提交标志位

        events:{
            //'click #btnAdd': 'btnAdd',
            'click #btnAdd': 'btnAdd'
        },

        initialize:function () {
            $('#red_date').datepicker().on('changeDate', function(event) {
                $(event.target).datepicker('hide');
            });

        },
        //表单的异步提交
        //addIncome:function() {
        //    //防止两重提交
        //    //if (this.in_syncing) {
        //    //    return;
        //    //}
        //    //this.in_syncing = true;
        //    //$('#btnSave').prop('disabled', true);
        //    //
        //    //$('#frmEditInfo').submit();
        //    //防止两重提交
        //    if (this.in_syncing) {
        //        return;
        //    }
        //    var current_view = this;
        //    this.in_syncing = true;
        //    this.options.parentView.trigger('start_ajax_sync');
        //    var form = $('#IncomeAdd');
        //    $.ajax({
        //        type: "POST",
        //        url: form.attr('action'),
        //        data: form.serialize(),
        //        success: function(data){
        //            if (data.error_code > 0) {
        //                window.alert(data.error_msg);
        //            }else {
        //                //var InfoForm = $("#frmEditInfo", data);
        //                //$('#ToInfoForm').html(InfoForm);
        //                var validation = $('#id_validation').val();
        //                //var validation = data.validation;
        //                if (validation === true) {
        //                    alert("编辑成功");
        //                    //var myDate = new Date();
        //                    //$('#id_update_datetime').val(myDate.toLocaleString());
        //                    ////日期格式待完善
        //                    //$('.tip').tooltip();
        //                }else {
        //                    alert("error");
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
        //

        //表单的同步提交
        btnAdd:function() {
            if(!this.validate(event)){
                return;
            }
            //防止两重提交
            if (this.in_syncing) {
                return;
            }
            this.in_syncing = true;
            $('#btnAdd').prop('disabled', true);
            $('#IncomeAdd').submit();
        },

        validate: function(event){
            var recode_user = $("#regName").val();    // 获取前端规格输入框的内容
            var income_type = $("#incomeType").val();   // 获取前端价格输入框的内容
            var income_amount = $("#incomeAmount").val(); //检查收入金额是否正确


            if(recode_user == ""){
                alert("请填上记录人姓名！");
                return false;
            }
            if(income_type == ""){
                alert("请填写收入类型！");
                return false;
            }
            if(income_amount == 0 || income_amount.search("^[0-9]*[1-9][0-9]*$") != 0){
                alert("价格不可以为空，而且必须为整数！");
                return false;
            }
            return true;
        },
        // 返回用户一览
        return_to_prev_page:function() {
            var ru = $('#redirect_url');
            var url;
            if (!ru || ru.length === 0 || !ru.val()) {
                url = '/user_account/list/';
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