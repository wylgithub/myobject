define([
    'require',
    'jquery',
    'backbone'
], function (require, $, Backbone) {
    "use strict";
    return Backbone.View.extend({
        el:"body",

        events:{
            'click #btnSearchTicketAndCard':'btnSearchTicketCardClick',
            'click #btnSearchCardSN':'btnSearchCardSnClick',
//            'click #btnDisableTicket': 'btn_change_ticket_status',
//            'keydown #txtCode2Disabled': 'txt_code_to_disabled_keydown'
            'click #btnDisableSerialNumber': 'clickDisableSerialNumber',
            'click #btnEnableSerialNumber': 'clickEnableSerialNumber',
            'click #btnDisableVolNo': 'clickDisableVolNo',
            'click #btnEnableVolNo': 'clickbtnEnableVolNo',
            'click #btnSearchCardSNCS': 'btnSearchCardSnCsClick'
        },

        initialize:function(parent) {
            this.parentView = parent;
        },

        clickbtnEnableVolNo: function() {
            var code = $('#txtVolNo').val();
             if (code === '') {
                return;
            }

            //防止两重提交
            if (this.in_syncing) {
                return;
            }
            this.in_syncing = true;
            this.options.parentView.trigger('start_ajax_sync');
            $('#btnEnableVolNo').prop('disabled', true);
            $('#txtVolNo').prop('disabled', true);
            var _view = this;
            var url = '/admin/vol_no/enable/';
            $.post(url,
                {
                    "parameter": code
                },
                function(data) {
                if (data) {
                    window.alert("共输入了" + data.total_vol_count + "个册号，共包含" +  data.total_card_count + "个序列号，启用了其中" + data.updated_count + "个无效序列号。");
                }
            })
            .error(function() {
                window.alert('与服务器通讯发生错误，请稍后重试。');
            })
            .complete(function() {
                //防止两重提交
                //恢复现场
                _view.options.parentView.trigger('finish_ajax_sync');
                _view.in_syncing = false;
                $('#btnEnableVolNo').prop('disabled', false);
                $('#txtVolNo').prop('disabled', false);
            });
        },

        clickDisableVolNo: function() {
            var code = $('#txtVolNo').val();
             if (code === '') {
                return;
            }

            //防止两重提交
            if (this.in_syncing) {
                return;
            }
            this.in_syncing = true;
            this.options.parentView.trigger('start_ajax_sync');
            $('#btnDisableVolNo').prop('disabled', true);
            $('#txtVolNo').prop('disabled', true);
            var _view = this;
            var url = '/admin/vol_no/disable/';
            $.post(url,
                {
                    "parameter": code
                },
                function(data) {
                if (data) {
                    window.alert("共输入了" + data.total_vol_count + "个册号，共包含" +  data.total_card_count + "个序列号，禁用了其中" + data.updated_count + "个有效序列号。");
                }
            })
            .error(function() {
                window.alert('与服务器通讯发生错误，请稍后重试。');
            })
            .complete(function() {
                //防止两重提交
                //恢复现场
                _view.options.parentView.trigger('finish_ajax_sync');
                _view.in_syncing = false;
                $('#btnDisableVolNo').prop('disabled', false);
                $('#txtVolNo').prop('disabled', false);
            });
        },

        clickEnableSerialNumber: function() {
            var code = $('#txtSerialNumber').val();
             if (code === '') {
                return;
            }

            //防止两重提交
            if (this.in_syncing) {
                return;
            }
            this.in_syncing = true;
            this.options.parentView.trigger('start_ajax_sync');
            $('#btnEnableSerialNumber').prop('disabled', true);
            $('#txtSerialNumber').prop('disabled', true);
            var _view = this;
            var url = '/admin/serial_number/enable/';
            $.post(url,
                {
                    "parameter": code
                },
                function(data) {
                if (data) {
                    window.alert("共输入了" + data.total_count + "个序列号，启用了其中" + data.updated_count + "个无效序列号。");
                }
            })
            .error(function() {
                window.alert('与服务器通讯发生错误，请稍后重试。');
            })
            .complete(function() {
                //防止两重提交
                //恢复现场
                _view.options.parentView.trigger('finish_ajax_sync');
                _view.in_syncing = false;
                $('#btnEnableSerialNumber').prop('disabled', false);
                $('#txtSerialNumber').prop('disabled', false);
            });
        },

        clickDisableSerialNumber: function() {
            var code = $('#txtSerialNumber').val();
             if (code === '') {
                return;
            }

            //防止两重提交
            if (this.in_syncing) {
                return;
            }
            this.in_syncing = true;
            this.options.parentView.trigger('start_ajax_sync');
            $('#btnDisableSerialNumber').prop('disabled', true);
            $('#txtSerialNumber').prop('disabled', true);
            var _view = this;
            var url = '/admin/serial_number/disable/';
            $.post(url,
                {
                    "parameter": code
                },
                function(data) {
                if (data) {
                    window.alert("共输入了" + data.total_count + "个序列号，禁用了其中" + data.updated_count + "个有效序列号。");
                }
            })
            .error(function() {
                window.alert('与服务器通讯发生错误，请稍后重试。');
            })
            .complete(function() {
                //防止两重提交
                //恢复现场
                _view.options.parentView.trigger('finish_ajax_sync');
                _view.in_syncing = false;
                $('#btnDisableSerialNumber').prop('disabled', false);
                $('#txtSerialNumber').prop('disabled', false);
            });
        },

        btnSearchCardSnClick:function() {
            var search_keyword = $("#queryKeyCardSN").val();
            search_keyword = $.trim(search_keyword);
            if (search_keyword === '') {
                return;
            }

            var url = '/report/search/sn/' + encodeURIComponent(search_keyword) + "/";
            url += "?" + this.options.parentView.get_next_link();
            window.location.href = url;
        },

        btnSearchTicketCardClick:function() {
            var search_keyword = $("#queryKeyTicketAndCard").val();
            search_keyword = $.trim(search_keyword);
            if (search_keyword === '') {
                return;
            }

            var url = '/report/search/qrcode/' + encodeURIComponent(search_keyword) + "/";
            url += "?" + this.options.parentView.get_next_link();
            window.location.href = url;
        },

        btnSearchCardSnCsClick:function() {
            var search_keyword = $("#queryKeyCardSN").val();
            search_keyword = $.trim(search_keyword);
            if (search_keyword === '') {
                return;
            }

            var url = '/customer_service/search/sn/' + encodeURIComponent(search_keyword) + "/";
            url += "?" + this.options.parentView.get_next_link();
            window.location.href = url;
        }
    });
});