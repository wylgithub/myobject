define([
    'require',
    'jquery',
    'backbone'
], function (require, $, Backbone) {
    "use strict";
    return Backbone.View.extend({
        el:"body",

        events:{
        },

        initialize:function(parent) {
            this.parentView = parent;
        }
    });
});