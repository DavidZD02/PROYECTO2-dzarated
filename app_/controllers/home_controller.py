from flask import Blueprint, render_template, request, flash, redirect, url_for
from app_.models.producto import Producto
from app_.models.base import Base
from app_.models.complemento import Complemento
from app_.models.heladeria import Heladeria
from app_.config.db import db
from app_.controllers.funciones import contar_calorias
from app_.controllers.funciones import calcular_costo_ingredientes
from app_.controllers.funciones import calcular_rentabilidad
from app_.controllers.funciones import realizar_venta


home_blueprint = Blueprint("home", __name__)


@home_blueprint.route("/")
def home():
    return render_template("index.html")


@home_blueprint.route("/vender", methods=["GET", "POST"])
def vender_producto():
    if request.method == "POST":
        producto_id = request.form.get("producto_id")
        producto = Producto.query.get(producto_id)
        heladeria = Heladeria.query.get(1)

        if producto:
            try:
                mensaje = realizar_venta(producto, heladeria)
                flash(mensaje, "success")
            except ValueError as e:
                ingrediente_faltante = str(e)
                flash(f"¡Oh no! Nos hemos quedado sin {ingrediente_faltante}", "danger")
        else:
            flash("Producto no encontrado.", "danger")

        return redirect(url_for("home.vender_producto"))

    productos = Producto.query.all()
    heladeria = Heladeria.query.get(1)
    return render_template("vender.html", productos=productos, heladeria=heladeria)


@home_blueprint.route("/abastecer", methods=["GET", "POST"])
def abastecer():
    if request.method == "POST":
        # Obtener datos del formulario
        base_id = request.form.get("base_id")
        complemento_id = request.form.get("complemento_id")
        complemento_reiniciar_id = request.form.get("complemento_reiniciar_id")
        base_reiniciar_id = request.form.get("base_reiniciar_id")

        # Abastecer base si existe
        if base_id:
            base = Base.query.get(base_id)
            if base:
                base.abastecer()
                flash(f"Base {base.nombre} abastecida correctamente.", "success")
            else:
                flash("La base seleccionada no existe.", "error")

        # Abastecer complemento si existe
        if complemento_id:
            complemento = Complemento.query.get(complemento_id)
            if complemento:
                complemento.abastecer()
                flash(
                    f"Complemento {complemento.nombre} abastecido correctamente.",
                    "success",
                )
            else:
                flash("El complemento seleccionado no existe.", "error")

        if complemento_reiniciar_id:
            complemento_reiniciar = Complemento.query.get(complemento_reiniciar_id)
            if complemento_reiniciar:
                complemento_reiniciar.renovar_inventario()
                flash("Inventario renovado.","success",)
            else:
                flash("El complemento seleccionado no existe.", "error")

        if base_reiniciar_id:
            base_reiniciar = Base.query.get(base_reiniciar_id)
            if base_reiniciar:
                base_reiniciar.renovar_inventario()
                flash("Inventario renovado.","success",)
            else:
                flash("El complemento seleccionado no existe.", "error")

        # Redirigir después de procesar ambos
        return redirect(url_for("home.abastecer"))

    # Obtener bases y complementos para mostrar en la página
    bases = Base.query.all()
    complementos = Complemento.query.all()
    return render_template("abastecer.html", bases=bases, complementos=complementos)

@home_blueprint.route("/info_productos", methods=["GET"])
def info_productos():
    productos = Producto.query.all()
    productos_info = []

    for producto in productos:
        # Obtener los ingredientes del producto
        ingredientes = producto.ingredientes

        # Calcular calorías totales
        calorias = contar_calorias(
            [Base.query.filter_by(nombre=ing.nombre).first().calorias if ing.tipo == "base"
             else Complemento.query.filter_by(nombre=ing.nombre).first().calorias
             for ing in ingredientes]
        )

        # Calcular costo de producción
        costo = calcular_costo_ingredientes(ingredientes)

        # Calcular rentabilidad
        rentabilidad = calcular_rentabilidad(producto.precio_publico, ingredientes)

        # Agregar la información del producto
        productos_info.append({
            "nombre": producto.nombre,
            "precio_publico": producto.precio_publico,
            "calorias_totales": calorias,
            "costo_produccion": costo,
            "rentabilidad": rentabilidad,
        })

    return render_template("info_productos.html", productos_info=productos_info)


