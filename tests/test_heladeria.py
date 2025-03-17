import unittest
from app_.models.base import Base
from app_.models.complemento import Complemento
from app_.models.producto import Producto
from app_.controllers.funciones import (
    contar_calorias,
    calcular_costo_ingredientes,
    calcular_rentabilidad,
    realizar_venta
)
from app_.models.heladeria import Heladeria


class TestHeladeria(unittest.TestCase):
    def setUp(self):
        # Configuración inicial para las pruebas
        self.heladeria = Heladeria(nombre="Helados Ficticios", ventas_diarias=0)
        self.base = Base(nombre="Chocolate", calorias=100, costo=5, stock=10)
        self.complemento = Complemento(nombre="Chispas", calorias=50, costo=2, stock=10)
        self.producto = Producto(
            nombre="Malteada de Chocolate",
            precio_publico=20,
            ingredientes=[self.base, self.complemento],
        )

    def test_ingrediente_es_sano(self):
        # Probar si un ingrediente es sano (ejemplo: menos de 200 calorías)
        self.assertTrue(self.base.es_sano(), "La base debería ser sana.")
        self.assertTrue(self.complemento.es_sano(), "El complemento debería ser sano.")

    def test_abastecer_ingrediente(self):
        # Abastecer un ingrediente y verificar el stock
        stock_anterior = self.base.stock
        self.base.abastecer()
        self.assertGreater(self.base.stock, stock_anterior, "El stock debería aumentar.")

    def test_renovar_inventario_complementos(self):
        # Renovar inventario y verificar el stock
        stock_anterior = self.complemento.stock
        self.complemento.renovar_inventario()
        self.assertGreater(self.complemento.stock, stock_anterior, "El inventario debería renovarse.")

    def test_calcular_calorias(self):
        # Calcular calorías de copas y malteadas
        calorias = contar_calorias([self.base, self.complemento])
        self.assertEqual(calorias, 150, "Las calorías calculadas no son correctas.")

    def test_calcular_costo_produccion(self):
        # Calcular el costo de producción
        costo = calcular_costo_ingredientes(self.producto.ingredientes)
        self.assertEqual(costo, 7, "El costo de producción no es correcto.")

    def test_calcular_rentabilidad(self):
        # Calcular la rentabilidad
        rentabilidad = calcular_rentabilidad(self.producto.precio_publico, self.producto.ingredientes)
        self.assertEqual(rentabilidad, 13, "La rentabilidad calculada no es correcta.")

    def test_producto_mas_rentable(self):
        # Encontrar el producto más rentable
        producto2 = Producto(
            nombre="Copa de Fresa",
            precio_publico=25,
            ingredientes=[self.base],
        )
        productos = [self.producto, producto2]
        mas_rentable = max(productos, key=lambda p: calcular_rentabilidad(p.precio_publico, p.ingredientes))
        self.assertEqual(mas_rentable.nombre, "Copa de Fresa", "El producto más rentable no es correcto.")

    def test_vender_producto(self):
        # Probar la venta de un producto
        try:
            mensaje = realizar_venta(self.producto, self.heladeria)
            self.assertEqual(mensaje, "¡Vendido!", "El producto debería venderse correctamente.")
        except ValueError as e:
            self.fail(f"La venta falló inesperadamente: {str(e)}")

if __name__ == "__main__":
    unittest.main()
