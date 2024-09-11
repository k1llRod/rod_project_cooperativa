odoo.define('rod_dynamic_report.contact_report', function(require) {
  'use strict';

  var AbstractAction = require('web.AbstractAction');
  var core = require('web.core');
  var rpc = require('web.rpc');
  var QWeb = core.qweb;
  var _t = core._t;
  var datepicker = require('web.datepicker');
  var time = require('web.time');
  var framework = require('web.framework');
  var session = require('web.session');
  console.log('FUNCIONA')

  var ContactReport = AbstractAction.extend({
    template: 'ContactReport',  // Cambia esto a tu plantilla para el reporte de contactos
    events: {
      'click #apply_filter': 'apply_filter',
      'click #pdf': 'print_pdf',
      'click #xlsx': 'print_xlsx',
      'click .view_contact': 'button_view_contact', // Adaptado para contactos
      'click .cr-line': 'show_drop_down', // Cambiar a lo que corresponda en contactos
    },

    init: function(parent, action) {
      this._super(parent, action);
      this.report_lines = action.report_lines;
      this.wizard_id = action.context.wizard || null;
    },

    start: function() {
      var self = this;
      self.initial_render = true;
      rpc.query({
        model: 'dynamic.contact.report', // Cambiado al modelo de reporte de contactos
        method: 'create',
        args: [{}]
      }).then(function(res) {
        self.wizard_id = res;
        self.load_data(self.initial_render);
      });
    },

    load_data: function(initial_render = true) {
      var self = this;
      self._rpc({
        model: 'dynamic.contact.report',  // Cambiado al modelo de reporte de contactos
        method: 'contact_report',  // Cambiado al método de reporte de contactos
        args: [
          [this.wizard_id]
        ],
      }).then(function(datas) {
        if (initial_render) {
          self.$('.filter_view_cr').html(QWeb.render('ContactFilterView', {  // Plantilla adaptada para contactos
            filter_data: datas['filters'],
          }));
          self.$el.find('.report_type').select2({
            placeholder: 'Report Type...',
          });
        }
        console.log('datas["contacts"]',datas['contacts'])
        if (datas['contacts'])  // Adaptar a contactos
          self.$('.table_view_cr').html(QWeb.render('ContactTable', {  // Plantilla adaptada para contactos
            filter: datas['filters'],
            contacts: datas['contacts'],
            report_lines: datas['report_lines'],
            main_lines: datas['report_main_line']
          }));
      });
    },

    apply_filter: function() {
      // Implementación de filtros
    },

    print_pdf: function() {
      // Implementación para imprimir PDF
    },

    print_xlsx: function() {
      // Implementación para imprimir XLSX
    },

    button_view_contact: function() {
      // Implementación para ver el contacto específico
    },

    show_drop_down: function() {
      // Implementación para mostrar el dropdown
    },
  });

  core.action_registry.add('c_r', ContactReport);  // Registra la acción para contactos
  return ContactReport;
});