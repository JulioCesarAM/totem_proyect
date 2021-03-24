odoo.define('totem_proyect.prueba', function (require) {
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');

    var QWeb = core.qweb;
    var _t = core._t;


    var banners = AbstractAction.extend({
        carrousel: null,
        eventimeout: null,
        i: 0,
        allevents: {},
        slideIndex: 0,
        events:{
            "click #siguiente": _.debounce(function() {
                clearTimeout(this.carrousel);
                clearTimeout(this.eventimeout);
                this.next();
            }, 200, true),

            "click #atras": _.debounce(function() {
                clearTimeout(this.carrousel);
                clearTimeout(this.eventimeout);
                this.back();
            }, 200, true),
        },

        start: function(){
            var self = this;

            var def = this._rpc({
                model: 'event.totem',
                method: 'search_read',
            })
            .then(function (res) {
                self.i = 0;
                self.allevents = res;
                self.event = res[self.i];
                self.$el.html(QWeb.render("EventView", {widget: self}));
                setTimeout(() => {self.showslider();},0);
                self.eventimeout = setTimeout(function(){
                    clearTimeout(self.carrousel);
                    self.next();
                },  10000);
            });

            return $.when(def, this._super.apply(this, arguments));
        },

        showslider: function(){
            var self = this;
            var slides = $(".mySlides");
            for (let iterator = 0; iterator < slides.length; iterator++)
                slides[iterator].style.display = "none";
            if (self.slideIndex >= slides.length) 
                self.slideIndex = 0;
            slides[self.slideIndex].style.display = "block";
            self.slideIndex++;
            self.carrousel = setTimeout(() => {self.showslider()}, 2000);
        },

        next: function(){
            var self = this;
            self.i++;
            if(self.i >= self.allevents.length)
                self.i=0;
            self.event = self.allevents[self.i];
            self.$el.html(QWeb.render("EventView", {widget: self}));
            setTimeout(() => {self.showslider();},0);
            self.eventimeout = setTimeout(function(){
                clearTimeout(self.carrousel);
                self.next();
            },  10000);
        },

        back: function(){
            var self = this;
            self.i--;
            if(self.i < 0)
               self.i=self.allevents.length-1;
            self.event = self.allevents[self.i];
            self.$el.html(QWeb.render("EventView", {widget: self}));
            setTimeout(() => {self.showslider();},0);
            self.eventimeout = setTimeout(function(){
                clearTimeout(self.carrousel);
                self.next();
            },  10000);
        },
    });

    core.action_registry.add('event_view', banners);
    return banners;
});