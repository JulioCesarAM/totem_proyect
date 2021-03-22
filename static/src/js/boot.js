odoo.define('totem_proyect.prueba', function (require) {
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');

    var QWeb = core.qweb;
    var _t = core._t;

    var banners = AbstractAction.extend({
        events:{},

        start: function(){
            var self = this;

            var def = this._rpc({
                model: 'event.totem',
                method: 'search_read',
            })
            .then(function (res) {
                self.event = res[0];
                console.log("objeto", self.event)
                self.$el.html(QWeb.render("EventView", {widget: self}));
            });

            return $.when(def, this._super.apply(this, arguments));
        },
    });

    console.log("Fuera");

    core.action_registry.add('event_view', banners);
    return banners;
});