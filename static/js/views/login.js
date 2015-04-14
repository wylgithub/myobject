define([
    'require',
    'jquery',
    'backbone'
], function (require, $, Backbone) {
    "use strict";

    var AppView = Backbone.View.extend({
        el:"body",

        events:{
            'click #btnLogin':'login'
        },

        login:function() {
            $('#frmLogin').submit();
        }
    });
    return AppView;
});