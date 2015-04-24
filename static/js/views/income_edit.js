/**
 * Created by wyl on 15-4-23.
 */
define([
    'require',
    'jquery',
    'backbone',
    'datepicker',
    'datetimepicker',
    'datepicker',
    'datetimepickerCN',
], function (require, $, Backbone) {
    "use strict";

    return Backbone.View.extend({
        el:"body",
        in_syncing:false,  //防止两重提交标志位
        role:$('#id_role'),
        btnRoleDisplay:$('#btnRoleDisplay'),

        events:{
            'click .dropdownItem':'dropdownItem_click',
            'click #btnReturn':'return_to_prev_page',
            'click #btnAdd':'save'
        },

        initialize:function () {
            $('#red_date').datepicker().on('changeDate', function(event) {
                $(event.target).datepicker('hide');
            });
        },

        save:function() {
            //防止两重提交
            if (this.in_syncing) {
                return;
            }
            this.in_syncing = true;
            var txtPassword = $('#regName');
            if (txtPassword.val() === '') {
                txtPassword.prop('disabled', true);
            }
            $('#btnAdd').prop('disabled', true);

            $('#IncomeAdd').submit();
        },

        // 返回用户一览
        return_to_prev_page:function() {
            var ru = $('#redirect_url');
            var url;
            if (!ru || ru.length === 0 || !ru.val()) {
                url = '/income/list/';
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
});