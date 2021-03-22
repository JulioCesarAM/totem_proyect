odoo.define('totem_proyect.prueba', function (require) {
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');

    var MyAttendances = AbstractAction.extend({
        events:{},

        start: function(){
            var self = this;

            var def = this._rpc({
                model: 'event.totem',
                method: 'search_read',
                args: ['description'],
            })
        }
});