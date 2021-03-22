odoo.define('totem_proyect.prueba', function (require) {
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');

    var banners = AbstractAction.extend({
        events:{},

        start: function(){
            var self = this;

            var def = this._rpc({
                model: 'event.totem',
                method: 'search_read',
                args: [[],['description']],
            })
            .then(res => {
                self.event = res[0];
                self.$el.html(QWeb.render("eventView", {widget: self}))
            });
        }
    });

    core.action_registry.add('eventview', banners);
    return banners;
});