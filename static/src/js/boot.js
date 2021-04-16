odoo.define('totem_proyect.prueba', function (require) {
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');

    var QWeb = core.qweb;
    var _t = core._t;


    var banners = AbstractAction.extend({
        carrousel: null, // Carrousel de imagenes
        eventimeout: null, // Timeout del slider de eventos
        allevents: {}, // Todos los eventos que se van a mostrar
        i: 0, // Index que recorre allevents
        configuration: {}, // Datos de la configuración
        event: null, // Evento a mostrar
        modalBool: false, // Modal abierto o no
        modalTimer: null, // Timeout del modal abierto
        events:{
            "click #siguiente": _.debounce(function() { // Siguiente evento
                clearTimeout(this.carrousel);
                this.eventimeout.clearTimeout();
                this.next(); // Pasar al siguiente evento
            }, 200, true),

            "click #atras": _.debounce(function() { // Anterior evento
                clearTimeout(this.carrousel);
                this.eventimeout.clearTimeout();
                this.back(); // Volver al evento anterior
            }, 200, true),
            
            "click #banner": _.debounce(function() { // Abrir el modal
                var self = this;
                if((self.event.titlePopUp==false||self.event.titlePopUp=="")&&(self.event.descriptionPopUp==false||self.event.descriptionPopUp=="")){
                    return 
                }
                setTimeout(function(){self.modalBool = true;},0); // Requiere del setTimeout 0 para que no se ejecute a la vez que el evento de abajo
                self.eventimeout.pause(); // Pausar el slider de eventos mientras el modal esta abierto
                $("#mymodal").modal({show: true}); // Mostrar modal
                self.modalTimer = setTimeout(function(){ // Timeout para cerrar modal
                    if(self.modalBool){ // Si ya esta abierto
                        $("#mymodal").modal('hide'); // Se cierra el modal
                        $("#mymodal").on('hidden.bs.modal', function(e){ // Una vez acabe la animación
                            self.eventimeout.resume() // Renaudar timer de slider de eventos
                            self.modalBool = false;
                        });
                    }
                }, self.configuration.redirectionTime * 1000)
            }, 200, true),
            
            "click #bodyPage #mymodal": _.debounce(function() { // Cerrar el modal
                var self = this;
                if(self.modalBool){ // Si ya esta abierto
                    $("#mymodal").modal('hide'); // Se cierra el modal
                        $("#mymodal").on('hidden.bs.modal', function(e){ // Una vez acabe la animación
                        self.eventimeout.resume() // Renaudar timer de slider de eventos
                        clearTimeout(self.modalTimer); // Eliminar timer de modal
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

                const HORAS24 = 86400000
                var eventsInTime = []
                for(let iterator=0; iterator<res.length; iterator++){ // Recorrer eventos
                    let dentro=false;
                    res[iterator].fechas.forEach(fechas => { // Recorrer fechas dentro de eventos
                        var eventFecha = Date.parse(fechas.fecha);
                        if(eventFecha<=Date.now() && Date.now()<eventFecha+HORAS24){ // Entra dentro del dia actual
                            var todayTime = new Date(Date.now());
                            todayTime = (todayTime.getHours()*60*60*1000)+(todayTime.getMinutes()*60*1000); // Hora actual en milisegundos
                            for(let j=0; j<fechas.rangoHoras.length && dentro==false; j++){ // Recorrer rangos horarios dentro de las fechas
                                if(fechas.rangoHoras[j].horaInicial<=todayTime && todayTime<fechas.rangoHoras[j].horaFinal){ // Entra en el rango horario
                                    eventsInTime.push(res[iterator]);
                                    dentro=true;
                                }
                            }
                        }
                    });
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
            setTimeout(() => { // Cuando venza la tasa de refresco
                if(self.modalBool){ // Si el modal esta abierto
                    $("#mymodal").modal('hide'); // Se cierra el modal
                    $("#mymodal").on('hidden.bs.modal', function(e){ // Una vez acabe la animación
                        if(self.eventimeout!=null)
                            self.eventimeout.clearTimeout(); // Se elimina el timer del slider de eventos
                        clearTimeout(self.modalTimer); // Se elimina el timer del slider de imagenes
                        self.modalBool = false;
                        self.start(); // Reinicio
                    });
                }
                else {
                    if(self.eventimeout!=null)
                        self.eventimeout.clearTimeout(); // Se elimina el timer del slider de eventos
                    clearTimeout(self.modalTimer); // Se elimina el timer del slider de imagenes
                    self.modalBool = false;
                    self.start(); // Reinicio
                }
            }, tasa_refresco);
        },
    });

    function Timer(callback, delay) { // Función setTimeout pero con pausa
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