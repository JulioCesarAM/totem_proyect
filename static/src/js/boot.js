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
        configuration: {},
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
                clearTimeout(self.carrousel);
                clearTimeout(self.eventimeout);
                self.allevents = res;
                if(self.i > res.length-1) // i = 0 si sobrepasa el numero de anuncios por eliminación
                    self.i = 0;
                self.event = res[self.i];
                console.log(self.event);
                var dur = self._rpc({
                    model: 'res.company',
                    method: 'search_read',
                    args: [[],['mainSlider', 'secundarySlider', 'description', 'companyQr', 'refreshTime']],
                })
                if(res.length == 0)
                    return "No hay eventos";
                else
                    return dur
            })
            .then(function (res){
                if(res != "No hay eventos"){
                    self.configuration = res[0];
                    self.$el.html(QWeb.render("EventView", {widget: self}));
                    setTimeout(() => {self.showslider();},0);
                    self.eventimeout = setTimeout(function(){
                        clearTimeout(self.carrousel);
                        self.next();
                    },  Number(self.configuration.mainSlider*1000));
                }
                else{
                    alert(res);
                }
                self.backup(Number(self.configuration.refreshTime*60*1000))
            });
        },

        showslider: function(){
            var self = this;
            let car = $(".mySlides")
            if(car.length > 1){
                for( let iterator=1; iterator<car.length; iterator++)
                    car[iterator].classList.remove("active");
                self.carrousel = $(".slideshow-container").carousel({
                    interval:Number(self.configuration.secundarySlider*1000)
                });
            }
        },

        next: function(){
            var self = this;
            self.i++;
            if(self.i >= self.allevents.length)
                self.i=0;
            self.event = self.allevents[self.i];
            self.comprobarEvento(true)
            self.$el.html(QWeb.render("EventView", {widget: self}));
            setTimeout(() => {self.showslider();},0);
            self.eventimeout = setTimeout(function(){
                clearTimeout(self.carrousel);
                self.next();
            },  Number(self.configuration.mainSlider*1000));
        },

        back: function(){
            var self = this;
            self.i--;
            if(self.i < 0)
               self.i=self.allevents.length-1;
            self.event = self.allevents[self.i];
            self.comprobarEvento(false)
            self.$el.html(QWeb.render("EventView", {widget: self}));
            setTimeout(() => {self.showslider();},0);
            self.eventimeout = setTimeout(function(){
                clearTimeout(self.carrousel);
                self.next();
            },  Number(self.configuration.mainSlider*1000))
        },

        comprobarEvento: function(nb){ // Elimina evento del array allevents
            var self = this;
            fetch(`/web/image/event.totem/${self.event.id}/bannerImg`)
                .then(response => {
                    if(!response.ok){
                        if(nb){
                            self.allevents.splice(self.allevents.indexOf(self.event), 1);
                            self.next();
                        }
                        else{
                            self.allevents.splice(self.allevents.indexOf(self.event), 1);
                            self.back();
                        }
                    }
                });
        },

        backup: function(tasa_refresco){
            var self = this;
            setTimeout(() => {self.start()}, tasa_refresco);
        },
    });

    core.action_registry.add('event_view', banners);
    return banners;
});