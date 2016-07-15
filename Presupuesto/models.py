from __future__ import unicode_literals

from django.db import models

@python_2_unicode_compatible
class Cliente (models.Model):
	empresa = models.CharField(max_length=100)
	contacto = models.CharField('Contacto (apellido, nombre)', max_length=200)
	funcion = models.CharField(max_length=100, blank='true')
	domicilio = models.CharField(max_length=100, blank='true')
	localidad = models.CharField(max_length=200, blank='true')
	telefono_fijo = models.CharField(max_length=100, blank='true')
	telefono_movil = models.CharField(max_length=100, blank='true')
	email = models.CharField(max_length=100, blank='true')
	cuit = models.CharField(max_length=13, blank='true')
	nota = models.CharField(max_length=200, blank='true')
	estado = models.CharField(max_length=200, blank='true')
	nota_comercial = models.CharField(max_length=200, blank='true')
	
	def __str__(self):
		return self.contacto+', '+self.empresa
	
	def delete(self, *args, **kwargs):
		if Presupuesto.objects.filter(cliente__pk= self.pk).exists():
			raise ValidationError('EL cliente esta relacionado al menos a un Presupuesto.')
		super(Cliente, self).delete(*args, **kwargs)

@python_2_unicode_compatible
class Presupuesto (models.Model):
	cliente = models.ForeignKey(Cliente, on_delete= models.PROTECT)
	referencia_clave = models.CharField(max_length=100, blank='true',default='SP16-')
	referencia = models.CharField(max_length=20,blank='true') #autoincremental
	fecha_solicitud = models.DateField('fecha de solicitud', default=date.today)
	fecha_vencimiento = models.DateField('fecha de vencimiento', blank='true', null='true')
	descripcion = models.CharField(max_length=100)
	estado = models.ForeignKey(Estado,on_delete= models.PROTECT)
	nota = models.CharField(max_length=200, blank='true')
	
	def __str__(self):
		return self.referencia

	def referencia_completa(self):
		return self.referencia_clave + self.referencia

@python_2_unicode_compatible
class Estado (models.Model):
	estado_actual = models.CharField(max_length=100)
	def __str__(self):
		return self.estado_actual
		
@python_2_unicode_compatible
class PresupuestoItem (models.Model):
	nombre = models.CharField(max_length=100)
	tipo = models.ForeignKey(Tipo, on_delete=models.PROTECT)
	valor_total = models.DecimalField(max_digits=8, decimal_places=2)
	coordinacion_proyectos = models.ForeignKey(Temp, on_delete=models.PROTECT)
	relevamiento = models.ForeignKey(Temp, on_delete=models.PROTECT)
	elaboracion_proyectos = models.ForeignKey(Temp, on_delete=models.PROTECT)
	elaboracion_proyectosExt = models.ForeignKey(Temp, on_delete=models.PROTECT)
	elaboracion_GIS = models.ForeignKey(Temp, on_delete=models.PROTECT)
	control_calidad = models.ForeignKey(Temp, on_delete=models.PROTECT)
	analisis_mestra = models.CharField(max_length=200, blank='true')
	otros = models.CharField(max_length=200, blank='true')
	nota = models.CharField(max_length=200, blank='true')
	
@python_2_unicode_compatible
class Proyecto (models.Model):
	presupuesto = models.ForeignKey(Presupuesto, on_delete=models.PROTECT)
	referencia_clave = models.CharField(max_length=100, blank='true',default='SP16-')
	referencia = models.CharField(max_length=20,blank='true') #autoincremental
	nombre = models.CharField(max_length=100)
	empresa_cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
	solicitante = models.CharField(max_length=200, blank='true')
	fecha_alta = models.DateField('fecha de alta', default=date.today)
	estado_general = models.ForeignKey(EstadoGeneral, on_delete=models.PROTECT)
	estado = models.ForeignKey(Estado, on_delete=models.PROTECT)
	
@python_2_unicode_compatible
class Personal (models.Model):
	persona = models.ForeignKey(Persona, on_delete=models.PROTECT)
	proyecto = models.ForeignKey(Proyecto, on_delete=models.PROTECT)
	funcion = models.ForeignKey(Funcion, on_delete=models.PROTECT)
	fecha = models.DateField('fecha del personal', default=date.today)
	cant_horas = models.DecimalField(max_digits=8, decimal_places=2)
	
@python_2_unicode_compatible
class Certificacion (models.Model):
	nombre_proyecto = models.ForeignKey(Proyecto, on_delete=models.PROTECT)
	impor_presupuesto = models.ForeignKey(Presupuesto, on_delete=models.PROTECT)
	estado_general = 	models.ForeignKey(Proyecto, on_delete=models.PROTECT)
	ultimo_estado = models.ForeignKey(Proyecto, on_delete=models.PROTECT)
	ultima_fecha = models.ForeignKey(Proyecto, on_delete=models.PROTECT)
	
@python_2_unicode_compatible
class Facturacion (models.Model):
	estado = models.CharField(max_length=200, blank='true')
	numero_factura = models.DecimalField(max_digits=100, decimal_places=2)
	fecha_factura = models.DateField('fecha de factura', default=date.today)
	dias = models.DecimalField(max_digits=8, decimal_places=2)
	fecha_cobro = models.DateField('fecha de cobro', default=date.today)
	
	