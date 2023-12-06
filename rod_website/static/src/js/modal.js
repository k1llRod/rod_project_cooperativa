odoo.define('rod_website.modal', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');
    console.log(publicWidget)
    console.log('FUNCIONA');

    publicWidget.registry.MyModal = publicWidget.Widget.extend({
        selector: '#wrapwrap',
        start: function () {
            this._super.apply(this, arguments);
            this.showModal();
        },
        showModal: function () {
            $('#miModal').modal('show');
        },
    });
});
