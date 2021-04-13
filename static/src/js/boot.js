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
        event: null,
        modalBool: false,
        modalTimer: null,
        events:{
            "click #siguiente": _.debounce(function() {
                clearTimeout(this.carrousel);
                this.eventimeout.clearTimeout();
                this.next();
            }, 200, true),

            "click #atras": _.debounce(function() {
                clearTimeout(this.carrousel);
                this.eventimeout.clearTimeout();
                this.back();
            }, 200, true),
            
            "click #content": _.debounce(function() {
                var self = this;
                setTimeout(function(){self.modalBool = true;},0);
                self.eventimeout.pause();
                $("#mymodal").modal({show: true});
                self.modalTimer = setTimeout(function(){
                    if(self.modalBool){
                        $("#mymodal").modal('hide');
                        $("#mymodal").on('hidden.bs.modal', function(e){
                            self.eventimeout.resume()
                            self.modalBool = false;
                        });
                    }
                }, self.configuration.redirectionTime * 1000)
            }, 200, true),
            
            "click #bodyPage #mymodal": _.debounce(function() {
                var self = this;
                if(self.modalBool){
                    $("#mymodal").modal('hide');
                        $("#mymodal").on('hidden.bs.modal', function(e){
                        self.eventimeout.resume()
                        clearTimeout(self.modalTimer);
                        self.modalBool = false;
                    });
                }
            }, 200, true),
        },

        start: function(){
            var self = this;

            // Traer de la base de datos los eventos

            var def = this._rpc({
                model: 'event.totem',
                method: 'get_events',
                args: [this.getSession().uid, ],
            })
            .then(function (res) {
                
                // Limpiar slider de imagenes cada tasa de refresco

                clearTimeout(self.carrousel);

                // Controlar que anuncios guardar dependiendo de los margenes de tiempo

                var eventsInTime = []
                for(let iterator=0; iterator<res.length; iterator++)
                    if(Date.parse(res[iterator].fechaInicio)<=Date.now() && Date.now()<Date.parse(res[iterator].fechaFin)){
                        let todayTime = new Date(Date.now());
                        todayTime = todayTime.getHours()*60*60*1000+todayTime.getMinutes()*60*1000;
                        if(res[iterator].horaInicio<=todayTime && todayTime<res[iterator].horaFin)
                            eventsInTime.push(res[iterator]);
                    }
                
                self.allevents = eventsInTime;

                /////////////////////////////////////////////////////////////////////////

                if(self.i > self.allevents.length-1) // i = 0 si sobrepasa el numero de anuncios por eliminación
                    self.i = 0;

                self.event = self.allevents[self.i]; // Seleccionar el evento a mostrar
                console.log(self.event);

                // Traer de la base de datos la configuración del administrador

                var dur = self._rpc({
                    model: 'res.company',
                    method: 'search_read',
                    args: [[],['mainSlider', 'secundarySlider', 'description', 'companyQr', 'refreshTime', 'redirectionTime']],
                })
                if(eventsInTime.length == 0) // Handler cuando NO hay eventos
                    return "No hay eventos, dele a \"aceptar\" y vuelva atrás";
                else                         // Handler cuando SI hay eventos
                    return dur
            })
            .then(function (res){
                if(res != "No hay eventos, dele a \"aceptar\" y vuelva atrás"){ // Handler cuando SI hay eventos
                    self.configuration = res[0]; // Guardar la configuración en una variable
                    self.$el.html(QWeb.render("EventView", {widget: self})); // Renderizar la vista en el xml
                    setTimeout(() => {self.showslider();},0); // Iniciar el slider de imagenes
                    self.eventimeout = new Timer(function(){ // Llamar al siguiente evento  en un lapso de tiempo
                        clearTimeout(self.carrousel);
                        self.next();
                    },  Number(self.configuration.mainSlider*1000));
                    self.backup(Number(self.configuration.refreshTime*60*1000)) // Llamar a la tasa de refresco
                }
                else{ // Handler cuando NO hay eventos
                    alert(res);
                }

            });
        },

        showslider: function(){
            var self = this;
            let car = $(".mySlides") // Guardar el contenedor de las imagenes
            if(car.length > 1){ // Siempre que sea mayor que uno, se hace el carrousel
                for( let iterator=1; iterator<car.length; iterator++) // Recorrer todas las imagenes
                    car[iterator].classList.remove("active"); // Dejar solo una imagen activa
                self.carrousel = $(".slideshow-container").carousel({ //Iniciar la animación del carrousel de imagenes
                    interval:Number(self.configuration.secundarySlider*1000)
                });
            }
        },

        next: function(){
            var self = this;
            self.i++; // incrementar el iterador del array de eventos
            if(self.i >= self.allevents.length) // Controlar que no salga del rango
                self.i=0;
            self.event = self.allevents[self.i]; // Incrementar el evento
            self.comprobarEvento(true) // Comprobar si el evento no ha sido borrado
            self.$el.html(QWeb.render("EventView", {widget: self})); // Renderizar la vista en el xml
            setTimeout(() => {self.showslider();},0); // Iniciar el slider de imagenes
            self.eventimeout = new Timer(function(){ // Recursividad, llamar al siguiente evento en un lapso de tiempo
                clearTimeout(self.carrousel);
                self.next();
            },  Number(self.configuration.mainSlider*1000));
        },

        back: function(){
            var self = this;
            self.i--; // Decrementar el iterador del array de eventos
            if(self.i < 0) // Controlar que no salga del rango
               self.i=self.allevents.length-1;
            self.event = self.allevents[self.i]; // Incrementar el evento
            self.comprobarEvento(false) // Comprobar si el evento no ha sido borrado
            self.$el.html(QWeb.render("EventView", {widget: self})); // Renderizar la vista en el xml
            setTimeout(() => {self.showslider();},0); // Iniciar el slider de imagenes
            self.eventimeout = new Timer(function(){ // Recursividad, llamar al siguiente evento en un lapso de tiempo
                clearTimeout(self.carrousel);
                self.next();
            },  Number(self.configuration.mainSlider*1000));
        },

        comprobarEvento: function(nb){ // Elimina evento del array allevents
            var self = this;
            fetch(`/web/image/event.totem/${self.event.id}/bannerImg`)
                .then(response => { // Comprobar que existe la imagen (El evento no haya sido borrado)
                    if(!response.ok){ // Si el evento fue eliminado
                        if(nb){ // Cuando es llamado del next()
                            self.allevents.splice(self.allevents.indexOf(self.event), 1); // Eliminar el evento del array
                            self.next(); // Siguiente evento
                        }
                        else{ // Cuando es llamado del back()
                            self.allevents.splice(self.allevents.indexOf(self.event), 1); // Eliminar el evento del array
                            self.back(); // Anterior evento
                        }
                    }
                });
        },

        backup: function(tasa_refresco){
            var self = this;
            setTimeout(() => {
                if(self.modalBool){
                    $("#mymodal").modal('hide');
                    $("#mymodal").on('hidden.bs.modal', function(e){
                        console.log("Refresco");
                        if(self.eventimeout!=null)
                            self.eventimeout.clearTimeout();
                        clearTimeout(self.modalTimer);
                        self.modalBool = false;
                        self.start();
                    });
                }
                else {
                    console.log("Refresco");
                    if(self.eventimeout!=null)
                        self.eventimeout.clearTimeout();
                    clearTimeout(self.modalTimer);
                    self.modalBool = false;
                    self.start();
                }
            }, tasa_refresco);
        },
    });

    function Timer(callback, delay) {
        var timerId, start, remaining = delay;
    
        this.pause = function() {
            window.clearTimeout(timerId);
            remaining -= new Date() - start;
        };
    
        this.resume = function() {
            start = new Date();
            window.clearTimeout(timerId);
            timerId = window.setTimeout(callback, remaining);
        };

        this.clearTimeout = function() {
            window.clearTimeout(timerId);
        }
    
        this.resume();
    }

    core.action_registry.add('event_view', banners);
    return banners;
});