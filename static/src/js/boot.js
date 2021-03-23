odoo.define('totem_proyect.prueba', function (require) {
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');

    var QWeb = core.qweb;
    var _t = core._t;

    var carrousel

    var banners = AbstractAction.extend({
        events:{},

        start: function(){
            var self = this;

            var def = this._rpc({
                model: 'event.totem',
                method: 'search_read',
            })
            .then(function (res) {
                var i = 0;
                setInterval(function(){
                    self.event = res[i];
                    self.$el.html(QWeb.render("EventView", {widget: self}));
                    self.intervals();
                    i++;
                    if(i>=res.length)
                        i=0;
                    setTimeout(function(){
                        clearInterval(carrousel);
                    },  12000);
                },  12000);
            });

            return $.when(def, this._super.apply(this, arguments));
        },

        intervals: function(){
            setTimeout(function(){
                $("#slideshow img:gt(0)").hide();
            }, 0);
            carrousel = setInterval(function() {
                $('#slideshow :first-child')
                .fadeOut(0)
                .next('img')
                .fadeIn(1000)
                .end()
                .appendTo('#slideshow');
            }, 3000);
        }
    });

    core.action_registry.add('event_view', banners);
    return banners;
});